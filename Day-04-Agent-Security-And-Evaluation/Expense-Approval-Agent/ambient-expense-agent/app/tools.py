from google.adk.tools import ToolContext

def check_expense_policy(
    amount: float,
    category: str,
    description: str,
) -> dict:
    """Checks if an expense complies with company policy.

    Args:
        amount: The dollar amount of the expense.
        category: The category of the expense (e.g., travel, meals, software, office).
        description: A short description explaining the expense.

    Returns:
        A dict with 'status' (approved, policy_violation, or review_required) and 'reason'.
    """
    valid_categories = {"travel", "meals", "software", "office"}
    
    if category.lower() not in valid_categories:
        return {
            "status": "policy_violation",
            "reason": f"Category '{category}' is not a valid expense category. Allowed categories are: {', '.join(valid_categories)}."
        }
        
    if amount <= 0:
        return {
            "status": "policy_violation",
            "reason": "Expense amount must be greater than 0."
        }

    # Policy threshold: Expenses over $100 require manager approval
    if amount > 100.0:
        return {
            "status": "review_required",
            "reason": f"Expense amount ${amount:.2f} exceeds the automatic approval limit of $100.00."
        }

    return {
        "status": "approved",
        "reason": f"Expense of ${amount:.2f} for '{description}' under category '{category}' is within automatic limits."
    }

def notify_manager(
    amount: float,
    employee_name: str,
    reason: str,
) -> dict:
    """Sends a notification to the manager for manual review of an expense.

    Args:
        amount: The dollar amount of the expense requiring review.
        employee_name: The name of the employee who submitted the expense.
        reason: The reason why manual review is required.

    Returns:
        A dict with 'status' indicating if the notification was sent successfully.
    """
    # In a real application, this would send an email or Pub/Sub notification.
    # For the starter template, we mock the success response.
    return {
        "status": "success",
        "message": f"Manager notification sent successfully for ${amount:.2f} expense by {employee_name} due to: {reason}."
    }
