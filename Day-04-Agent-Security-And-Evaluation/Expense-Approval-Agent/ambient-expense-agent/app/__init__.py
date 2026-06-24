from google.adk.apps import App
from .agent import root_agent

# Initialize the ADK App instance.
# The app name 'app' matches the containing directory name.
app = App(name="app", root_agent=root_agent)
