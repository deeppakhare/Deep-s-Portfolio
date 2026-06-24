import base64
import json
import logging
from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ambient Expense Agent")


def normalize_subscription(subscription: str) -> str:
    if not subscription:
        return "unknown"

    return subscription.split("/")[-1]


@app.get("/")
async def home():
    return {"status": "running"}


@app.post("/apps/expense_agent/trigger/pubsub")
async def pubsub_trigger(request: Request):
    body = await request.json()

    try:
        message = body.get("message", {})
        encoded_data = message.get("data", "")

        decoded = base64.b64decode(encoded_data).decode("utf-8")

        payload = json.loads(decoded)

        subscription = normalize_subscription(
            body.get("subscription", "")
        )

        logger.info(
            f"Received expense event from {subscription}: {payload}"
        )

        return {
            "status": "received",
            "subscription": subscription,
            "expense": payload
        }

    except Exception as e:
        logger.exception("Failed processing Pub/Sub event")

        return {
            "status": "error",
            "message": str(e)
        }