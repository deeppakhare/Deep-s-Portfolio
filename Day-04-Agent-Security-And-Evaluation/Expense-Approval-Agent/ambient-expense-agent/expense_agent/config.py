import os

# Configurable threshold for automatic approval (in USD)
THRESHOLD = float(os.getenv("EXPENSE_THRESHOLD", "100.00"))

# Model for risk judgment
MODEL_NAME = os.getenv("EXPENSE_MODEL_NAME", "gemini-3.1-flash-lite")
