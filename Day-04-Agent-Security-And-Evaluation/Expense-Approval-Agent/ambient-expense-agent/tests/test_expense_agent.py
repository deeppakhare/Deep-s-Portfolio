import base64
import pytest
from google.adk.runners import InMemoryRunner
from google.genai import types
from expense_agent import app
from expense_agent.agent import extract_payload

def test_extract_payload_json():
    # Plain JSON string
    payload = '{"amount": 45.0, "submitter": "Bob", "category": "travel", "description": "Taxi", "date": "2026-06-23"}'
    extracted = extract_payload(payload)
    assert extracted["amount"] == 45.0
    assert extracted["submitter"] == "Bob"

def test_extract_payload_pubsub_b64():
    # Base64-encoded inner data
    inner_json = '{"amount": 120.0, "submitter": "Alice", "category": "meals", "description": "Dinner", "date": "2026-06-23"}'
    b64_data = base64.b64encode(inner_json.encode("utf-8")).decode("utf-8")
    payload = {"data": b64_data}
    extracted = extract_payload(payload)
    assert extracted["amount"] == 120.0
    assert extracted["submitter"] == "Alice"

def test_extract_payload_plain_text():
    # Plain text format (from dataset/eval)
    text = "Review expense of 45.00 USD for 'Uber ride' under category 'travel'."
    extracted = extract_payload(text)
    assert extracted["amount"] == 45.0
    assert extracted["category"] == "travel"
    assert extracted["description"] == "Uber ride"

@pytest.mark.asyncio
async def test_auto_approve_flow():
    runner = InMemoryRunner(app=app)
    session = await runner.session_service.create_session(
        app_name="expense_agent", user_id="test_user"
    )
    
    # Send a compliant expense (under 100)
    msg = '{"amount": 45.00, "submitter": "Bob", "category": "travel", "description": "Uber ride", "date": "2026-06-23"}'
    
    events = []
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part.from_text(text=msg)]),
    ):
        events.append(event)
        
    # Get the final output
    final_output_event = next((e for e in events if e.output is not None), None)
    assert final_output_event is not None
    output = final_output_event.output
    assert output["status"] == "Approved"
    assert "Auto-approved" in output["reason"]
