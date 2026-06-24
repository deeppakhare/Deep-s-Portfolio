# Ambient Expense Agent

An automated background agent for monitoring and evaluating expense reports against corporate policies, built using the Google Agent Development Kit (ADK).

## Project Structure

```text
ambient-expense-agent/
├── app/                      # Agent code
│   ├── __init__.py           # Registers the ADK App instance
│   ├── agent.py              # Main agent definition and instructions
│   └── tools.py              # Custom tools (policy check, notifications)
├── tests/                    # Evaluation and testing suite
│   └── eval/                 # Evaluation dataset and configs
│       ├── eval_config.yaml  # Evaluation metric definitions
│       └── datasets/         # JSON-formatted evaluation cases
│           └── basic-dataset.json
├── agents-cli-manifest.yaml  # Configuration for agents-cli orchestrator
├── pyproject.toml            # Project dependencies and configuration
├── Makefile                  # Developer shortcuts for running/evaluating
└── .env                      # Local environment variable configuration
```

## Getting Started

### Prerequisites

- [Python](https://www.python.org/) (>= 3.10)
- [uv](https://docs.astral.sh/uv/) (highly recommended Python package manager)

### Installation

Sync all dependencies and virtual environment using:

```bash
make install
```

### Running the Agent

To run a quick single-turn test query:

```bash
make run
```

Or open the interactive web playground:

```bash
make playground
```

### Running Evaluation

To evaluate the agent's performance and accuracy against test cases:

```bash
make eval
```
