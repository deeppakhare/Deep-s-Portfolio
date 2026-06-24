from google.adk import Agent, Context, Workflow
from google.adk.events import Event, EventActions
from google.adk.workflow import node

# 1. Classifier Agent to determine if the query is related to shipping
classifier_agent = Agent(
    name="classifier_agent",
    model="gemini-2.5-flash",
    instruction="""
You are a shipping FAQ assistant.

Shipping FAQ:

- Standard shipping costs $5.99
- Express shipping costs $12.99
- Orders over $50 get free shipping
- Delivery time is 3-5 business days
- Express delivery is 1-2 business days
- Returns are accepted within 30 days

Answer ONLY using the FAQ above.
"""
)

# 2. Classifier Node that runs the classifier agent and handles conditional routing
@node(name="classifier", rerun_on_resume=True)
async def classifier_node(ctx: Context, node_input: str):
    # Run the classifier agent
    result = await ctx.run_node(classifier_agent, node_input)
    
    # Extract text from the result
    text = ""
    if hasattr(result, "content") and result.content and result.content.parts:
        text = result.content.parts[0].text.strip().lower()
    else:
        text = str(result).strip().lower()
        
    # Route based on the classification result
    if "shipping" in text:
        yield Event(
    author="classifier",
    actions=EventActions(route="shipping")
)
    else:
        yield Event(
    author="classifier",
    actions=EventActions(route="unrelated")
)

# 3. Shipping FAQ Agent to answer shipping-related questions    
shipping_faq_agent = Agent(
    name="shipping_faq",
    model="gemini-2.5-flash",
    instruction="""
    You are a customer support representative for a shipping company.
    Your job is to answer user questions about shipping, tracking, delivery, rates, and returns.
    Provide polite, accurate, and helpful answers.
    """
)

# 4. Decline Node to politely decline answering unrelated questions
@node(name="decline", rerun_on_resume=True)
def decline_node(ctx: Context, node_input=None):
    yield Event(
        author="decline",
        content="I am sorry, but I can only answer questions related to shipping (shipping rates, tracking, delivery, or returns)."
    )

# 5. Root Agent Workflow Orchestrator defining the graph edges
root_agent = Workflow(
    name="customer_support_agent",
    edges=[
        ("START", classifier_node),
        (classifier_node, {
            "shipping": shipping_faq_agent,
            "unrelated": decline_node
        })
    ]
)
