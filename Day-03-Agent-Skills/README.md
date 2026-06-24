# 🤖 Day 03 – Agent Skills

## Assignment Completed ✅

**Unit 3 – Agent Skills**

---

## Overview

Day 3 focused on one of the most important concepts in modern Agent Engineering: **Agent Skills**.

Agent Skills allow AI agents to dynamically acquire specialized capabilities without loading massive prompts into context.

Instead of providing every instruction at once, skills use a structured directory-based architecture that loads information only when required. This helps avoid context overload, improves performance, and enables a single agent to perform many specialized tasks efficiently.

---

## Learning Resources

### 📄 Whitepaper

**Agent Skills**

https://drive.google.com/file/d/1Wso-CM4aAvTxFZa5wjBntKM3IVSg7PWW/view

---

### 🧪 Codelab 1

**Getting Started with Antigravity Skills**

https://codelabs.developers.google.com/getting-started-with-antigravity-skills?hl=en#0

---

### 🧪 Codelab 2

**Build Agents in Antigravity with Agents CLI and ADK**

https://codelabs.developers.google.com/agents-cli-adk-lifecycle#0

---

# What Are Agent Skills?

Agent Skills are reusable capability modules that can be attached to agents when needed.

Each skill contains:

```text
SKILL/
│
├── SKILL.md
├── tools/
├── prompts/
├── examples/
└── resources/
```

Instead of placing everything in a system prompt, the agent loads only the required skill when needed.

This approach is called:

### Progressive Disclosure

Benefits:

* Smaller context windows
* Better performance
* Reduced prompt complexity
* Easier maintenance
* Improved scalability

---

# Concepts Learned

## Context Rot

As conversations grow, agents may forget important information or become less effective.

This phenomenon is called:

**Context Rot**

Agent Skills help solve this problem by loading knowledge on demand.

---

## Progressive Context Loading

Rather than loading everything upfront:

```text
User Query
      ↓
Relevant Skill Selected
      ↓
Required Context Loaded
      ↓
Task Executed
```

This improves efficiency and response quality.

---

## ADK 2.0 Workflows

Learned how ADK models agent systems as graph-based workflows.

Components:

* Nodes
* Edges
* Routes
* Context
* Events
* Agents

---

# Hands-On Activities

## Agents CLI Setup

Configured:

* Agents CLI
* Antigravity Skills
* Gemini API
* Local Development Environment

Installed Skills:

* google-agents-cli-adk-code
* google-agents-cli-deploy
* google-agents-cli-eval
* google-agents-cli-observability
* google-agents-cli-publish
* google-agents-cli-scaffold
* google-agents-cli-workflow

---

# Project Built

## Customer Support Agent

As part of the Day 3 assignment, I built a shipping customer support agent using ADK 2.0 and Agents CLI.

The agent acts as a shipping company representative.

---

### Workflow Logic

```text
User Query
      ↓
Classifier Agent
      ↓
 ┌──────────────┐
 │ Shipping?    │
 └──────┬───────┘
        │
   Yes  │  No
        │
        ▼
Shipping FAQ Agent
        │
        ▼
Response

OR

Decline Node
        │
        ▼
Polite Rejection
```

---

### Features

* Intent Classification
* Shipping FAQ Responses
* Conditional Routing
* Graph-Based Workflow
* Gemini Integration
* Local Playground Testing
* ADK 2.0 Architecture

---

### Technologies Used

* Python
* Google ADK 2.0
* Agents CLI
* Gemini API
* Antigravity IDE

---

### Commands Used

Setup Agents CLI:

```bash
uvx google-agents-cli setup
```

Check Version:

```bash
google-agents-cli --version
```

List Skills:

```bash
npx -y skills list
```

Launch Playground:

```bash
adk web
```

---

# Testing & Debugging

During development I encountered several real-world issues:

* Agent naming validation errors
* Workflow routing issues
* Gemini API quota limitations
* Event validation errors
* ADK compatibility changes

These issues provided practical experience debugging AI workflows and understanding how graph-based agents operate internally.

---

# Screenshot Gallery

## Agents CLI Installation

(Add Screenshot)

screenshots/agents-cli-setup.png

---

## Agent Project Generation

(Add Screenshot)

screenshots/project-generation.png

---

## Workflow Code

(Add Screenshot)

screenshots/workflow-code.png

---

## ADK Playground

(Add Screenshot)

screenshots/adk-playground.png

---

## Shipping Query Test

(Add Screenshot)

screenshots/shipping-query-test.png

---

## Agent Routing

(Add Screenshot)

screenshots/agent-routing.png

---

# Key Learnings

Through Day 3 I learned:

* Agent Skills Architecture
* Progressive Disclosure
* Context Management
* ADK 2.0 Graph Workflows
* Agents CLI Lifecycle
* Agent Routing
* Local Playground Testing
* Workflow Debugging
* AI Agent Development

---

# Outcome

Successfully Completed:

✅ Agent Skills Whitepaper

✅ Antigravity Skills Codelab

✅ Agents CLI Lifecycle Codelab

✅ Agents CLI Setup

✅ ADK 2.0 Workflow Development

✅ Customer Support Agent Project

✅ Local Playground Testing

---

# Project Folder

```text
Customer-Support-Agent/
```

Contains:

* agent.py
* requirements.txt
* workflow logic
* ADK configuration
* project documentation

---

# Next Step

➡ Day 04 – Vibe Coding Agent Security & Evaluation
