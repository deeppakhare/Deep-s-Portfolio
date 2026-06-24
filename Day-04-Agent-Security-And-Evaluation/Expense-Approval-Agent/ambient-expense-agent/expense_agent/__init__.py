from google.adk.apps import App, ResumabilityConfig
from .agent import root_agent

# Initialize the ADK App instance.
# The app name matches the containing directory name.
app = App(
    name="expense_agent",
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
