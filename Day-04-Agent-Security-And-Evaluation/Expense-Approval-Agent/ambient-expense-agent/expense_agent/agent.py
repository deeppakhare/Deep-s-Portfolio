import json
import base64
import re
from pydantic import BaseModel, Field
from typing import Any, List, Optional
from google.adk.workflow import Workflow, node
from google.adk.agents import LlmAgent
from google.adk.agents.context import Context
from google.adk.events.event import Event
from google.adk.events.request_input import RequestInput
from google.genai import types
from . import config

# --- Pydantic Schemas ---

class Expense(BaseModel):
    amount: float
    submitter: str
    category: str
    description: str
    date: str

class RiskReviewResult(BaseModel):
    risk_score: int = Field(description="Risk score from 1 to 10 (10 being highest risk).")
    risk_factors: List[str] = Field(description="List of risk factors identified.")
    alert_raised: bool = Field(description="Whether a risk alert is raised.")
    reasoning: str = Field(description="Explanation of the risk evaluation and why it was flagged.")

# --- Extraction Helper ---

def parse_plain_text_expense(text: str) -> dict:
    """Helper to parse raw text prompts (e.g. from eval datasets)."""
    # Extract amount
    amount_match = re.search(r'(?:expense of|\$)?\s*([0-9]+(?:\.[0-9]+)?)\s*(?:USD)?', text, re.IGNORECASE)
    amount = float(amount_match.group(1)) if amount_match else 0.0
    
    # Extract description
    desc_match = re.search(r"for ['\"]([^'\"]+)['\"]", text, re.IGNORECASE)
    description = desc_match.group(1) if desc_match else "No description"
    
    # Extract category
    cat_match = re.search(r"category ['\"]([^'\"]+)['\"]", text, re.IGNORECASE)
    category = cat_match.group(1) if cat_match else "Unknown"
    
    # Extract submitter
    sub_match = re.search(r"(?:employee|submitted by(?:\s+employee)?)\s+['\"]([^'\"]+)['\"]", text, re.IGNORECASE)
    submitter = sub_match.group(1) if sub_match else "Unknown"
    
    # Default date
    date = "2026-06-23"
    
    return {
        "amount": amount,
        "submitter": submitter,
        "category": category,
        "description": description,
        "date": date
    }

def extract_payload(node_input: Any) -> dict:
    """Decodes and extracts the expense payload from various inputs."""
    raw_str = ""
    if isinstance(node_input, str):
        raw_str = node_input
    elif isinstance(node_input, dict):
        return node_input
    elif hasattr(node_input, "parts") and node_input.parts:
        raw_str = "".join([part.text for part in node_input.parts if part.text])
    elif hasattr(node_input, "text") and node_input.text:
        raw_str = node_input.text
    else:
        raw_str = str(node_input)

    # Try parsing raw_str as JSON first
    try:
        data = json.loads(raw_str)
        
        # Check if the details are under the "data" key (Pub/Sub or local event)
        if isinstance(data, dict) and "data" in data:
            inner_data = data["data"]
            if isinstance(inner_data, str):
                # Try base64 decoding (standard for Pub/Sub payload)
                try:
                    decoded_bytes = base64.b64decode(inner_data, validate=True)
                    inner_data = json.loads(decoded_bytes.decode("utf-8"))
                except Exception:
                    # If base64 fails, try parsing it as a plain JSON string
                    try:
                        inner_data = json.loads(inner_data)
                    except json.JSONDecodeError:
                        pass
            if isinstance(inner_data, dict):
                return inner_data
            return data
        return data
    except json.JSONDecodeError:
        # Fallback to regex parser for non-JSON text prompts
        return parse_plain_text_expense(raw_str)

# --- Security & Scrubbing Helpers ---

def scrub_description(description: str) -> tuple[str, list[str]]:
    """Scrubs SSNs and Credit Card numbers from the description.
    
    Returns the cleaned description and a list of redacted categories.
    """
    if not description:
        return description, []
        
    redacted_categories = []
    cleaned = description
    
    # 1. Scrub SSN: XXX-XX-XXXX
    ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    if ssn_pattern.search(cleaned):
        cleaned = ssn_pattern.sub("[SSN_REDACTED]", cleaned)
        redacted_categories.append("SSN")
        
    # 2. Scrub Credit Card numbers (13-16 digits with optional spaces or hyphens)
    cc_pattern = re.compile(
        r'\b(?:\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}|\d{4}[-\s]?\d{6}[-\s]?\d{5}|\d{4}[-\s]?\d{6}[-\s]?\d{4}|\d{13,16})\b'
    )
    if cc_pattern.search(cleaned):
        cleaned = cc_pattern.sub("[CREDIT_CARD_REDACTED]", cleaned)
        redacted_categories.append("Credit Card")
        
    return cleaned, redacted_categories

def detect_prompt_injection(description: str) -> bool:
    """Checks if the description contains common prompt injection techniques."""
    if not description:
        return False
        
    desc_lower = description.lower()
    
    # Phrases trying to override instructions, bypass check, or force auto-approval
    injection_phrases = [
        "ignore previous instructions",
        "ignore instructions",
        "ignore the policy",
        "ignore policy",
        "ignore all rules",
        "bypass policy",
        "bypass rules",
        "bypass verification",
        "override policy",
        "override rules",
        "force auto-approval",
        "force approval",
        "auto-approve this",
        "auto approve this",
        "approve this expense",
        "system: approve",
        "system: auto-approve",
        "instruction bypass",
        "ignore check_expense_policy",
    ]
    
    for phrase in injection_phrases:
        if phrase in desc_lower:
            return True
            
    # Check for formatting patterns commonly used in jailbreaks/prompt injections
    suspicious_patterns = [
        r"\[\s*system\s*:",
        r"system\s*message\s*:",
        r"new\s+instruction\b",
        r"ignore\s+above\b",
        r"ignore\s+below\b",
    ]
    for pattern in suspicious_patterns:
        if re.search(pattern, desc_lower):
            return True
            
    return False

# --- Workflow Nodes ---

@node
def parse_event_node(ctx: Context, node_input: Any) -> Event:
    """Parses incoming event payload, extracts expense details, and route/decision path."""
    payload = extract_payload(node_input)
    
    # Safely extract and format fields
    amount = float(payload.get("amount", 0.0))
    submitter = payload.get("submitter", "Unknown")
    category = payload.get("category", "Unknown")
    description = payload.get("description", "No description")
    date = payload.get("date", "Unknown")
    
    # Scrub PII from description first to ensure it never reaches logs or state in raw form
    cleaned_description, redacted = scrub_description(description)
    
    expense = {
        "amount": amount,
        "submitter": submitter,
        "category": category,
        "description": cleaned_description,
        "date": date
    }
    
    # Store expense details in session state
    ctx.state["expense"] = expense
    ctx.state["redacted_categories"] = redacted
    
    msg = f"📋 Received expense report: ${amount:.2f} by {submitter} for '{cleaned_description}' under category '{category}'."
    
    if amount < config.THRESHOLD:
        return Event(
            output=expense,
            route="auto_approve",
            state={"expense": expense, "redacted_categories": redacted},
            content=types.Content(role="model", parts=[types.Part.from_text(text=msg)])
        )
    else:
        return Event(
            output=expense,
            route="review_required",
            state={"expense": expense, "redacted_categories": redacted},
            content=types.Content(role="model", parts=[types.Part.from_text(text=msg)])
        )

@node
def auto_approve_node(ctx: Context, node_input: dict) -> Event:
    """Automatically approves expenses under the threshold."""
    expense = ctx.state.get("expense", node_input)
    status = "Approved"
    reason = f"Auto-approved instantly: amount ${expense.get('amount'):.2f} is under the ${config.THRESHOLD:.2f} threshold."
    
    outcome = {
        "status": status,
        "reason": reason,
        "expense": expense,
        "risk_review": None
    }
    
    msg = f"🟢 {reason}"
    
    return Event(
        output=outcome,
        state={"outcome": status, "outcome_reason": reason},
        content=types.Content(role="model", parts=[types.Part.from_text(text=msg)])
    )

@node
def security_checkpoint_node(ctx: Context, node_input: dict) -> Event:
    """Security checkpoint checking for PII and prompt injection before LLM review."""
    expense = dict(node_input)
    
    # 1. Scrub PII from description (safeguard/redundancy)
    cleaned_desc, redacted = scrub_description(expense.get("description", ""))
    expense["description"] = cleaned_desc
    ctx.state["expense"] = expense
    ctx.state["redacted_categories"] = redacted
    
    # 2. Check for prompt injection
    is_injection = detect_prompt_injection(cleaned_desc)
    
    if is_injection:
        # Flag as security event and route directly to human approval
        risk_review = {
            "risk_score": 10,
            "risk_factors": ["Security Event: Prompt Injection Attempt"],
            "alert_raised": True,
            "reasoning": "Prompt injection attempt detected in expense description. Bypassing LLM reviewer for security."
        }
        return Event(
            output=risk_review,
            route="security_event"
        )
    else:
        return Event(
            output=expense,
            route="clean"
        )

# LLM Risk Review Agent Node
llm_risk_review = LlmAgent(
    name="llm_risk_review",
    model=config.MODEL_NAME,
    instruction=(
        "You are an expense risk auditor. Evaluate the following expense report for potential policy violations, "
        "suspicious patterns, or high risk factors:\n\n"
        "Expense details:\n"
        "{expense}\n\n"
        "Provide a structured risk review output."
    ),
    output_schema=RiskReviewResult,
    output_key="risk_review",
)

@node(rerun_on_resume=True)
async def human_approval_node(ctx: Context, node_input: dict):
    """Raises risk alert, pauses workflow for human input, and captures the decision."""
    expense = ctx.state.get("expense", {})
    
    # 1. Raise alert (content event) if not already done
    if not ctx.state.get("alert_raised"):
        risk_score = node_input.get("risk_score", 0)
        risk_factors = node_input.get("risk_factors", [])
        reasoning = node_input.get("reasoning", "")
        
        alert_msg = (
            f"⚠️ RISK ALERT: Expense of ${expense.get('amount'):.2f} submitted by {expense.get('submitter')} requires human review.\n"
            f"• Risk Score: {risk_score}/10\n"
            f"• Risk Factors: {', '.join(risk_factors)}\n"
            f"• Reasoning: {reasoning}"
        )
        
        yield Event(
            content=types.Content(role="model", parts=[types.Part.from_text(text=alert_msg)]),
            state={"alert_raised": True, "risk_review": node_input}
        )
    
    # 2. Yield RequestInput to pause the workflow for human approval
    if not ctx.resume_inputs or "decision" not in ctx.resume_inputs:
        yield RequestInput(
            interrupt_id="decision",
            message=f"Please approve or reject this expense report of ${expense.get('amount'):.2f} submitted by {expense.get('submitter')}."
        )
        return
        
    # 3. Retrieve response once workflow is resumed
    decision = ctx.resume_inputs["decision"]
    yield Event(output=decision)

@node
def record_outcome_node(ctx: Context, node_input: str) -> Event:
    """Records the outcome after human review and returns the final workflow summary."""
    expense = ctx.state.get("expense", {})
    risk_review = ctx.state.get("risk_review", {})
    
    decision_str = str(node_input).strip().lower()
    if "approve" in decision_str:
        status = "Approved"
        reason = "Approved by human reviewer."
    elif "reject" in decision_str:
        status = "Rejected"
        reason = "Rejected by human reviewer."
    else:
        status = "Completed"
        reason = f"Decision processed: '{node_input}'"
        
    outcome = {
        "status": status,
        "reason": reason,
        "expense": expense,
        "risk_review": risk_review
    }
    
    msg = f"📝 Decision recorded: {status}. Reason: {reason}"
    
    return Event(
        output=outcome,
        state={"outcome": status, "outcome_reason": reason},
        content=types.Content(role="model", parts=[types.Part.from_text(text=msg)])
    )

# --- Workflow Graph Setup ---

root_agent = Workflow(
    name="expense_approval_workflow",
    edges=[
        ('START', parse_event_node),

        # Under threshold
        (parse_event_node, auto_approve_node, "auto_approve"),

        # Over threshold
        (parse_event_node, security_checkpoint_node, "review_required"),

        # Clean expense
        (security_checkpoint_node, llm_risk_review, "clean"),

        # Security event detected
        (security_checkpoint_node, human_approval_node, "security_event"),

        # Normal review path
        (llm_risk_review, human_approval_node),

        # Final decision
        (human_approval_node, record_outcome_node)
    ]
)