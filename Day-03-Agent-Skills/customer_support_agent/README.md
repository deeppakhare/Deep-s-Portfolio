# 📦 Customer Support Agent

An AI-powered Customer Support Agent built using **Google Agent Development Kit (ADK) 2.0** and **Gemini 2.5 Flash**.

The agent is designed to answer customer queries related to **shipping, delivery, tracking, shipping costs, and returns** while politely declining unrelated questions.

---

# 🚀 Features

* 🤖 Built with Google ADK 2.0
* 🧠 Powered by Gemini 2.5 Flash
* 🔀 Workflow-based agent routing
* 📦 Shipping FAQ support
* 🚫 Automatically declines unrelated queries
* ⚡ Event-driven architecture
* 🏗 Modular agent design

---

# 📋 Project Overview

This project demonstrates how to build a multi-node AI workflow using Google ADK.

The workflow contains:

1. **Classifier Agent**

   * Analyzes incoming user queries
   * Determines whether the query is shipping-related

2. **Shipping FAQ Agent**

   * Handles valid shipping questions
   * Provides customer support responses

3. **Decline Node**

   * Handles unrelated questions
   * Returns a polite refusal message

4. **Workflow Orchestrator**

   * Routes requests between nodes
   * Manages execution flow

---

# 🏗 Architecture

```text
User Query
     │
     ▼
Classifier Agent
     │
 ┌───┴────┐
 │        │
 ▼        ▼
Shipping  Unrelated
 Route     Route
 │          │
 ▼          ▼
Shipping   Decline
 FAQ       Node
 Agent
 │
 ▼
Response
```

---

# 📂 Project Structure

```text
customer_support_agent/
│
├── agent.py                # Main workflow definition
├── requirements.txt        # Project dependencies
├── __init__.py
├── .env                    # Environment variables
└── README.md
```

---

# ⚙️ Tech Stack

### AI Framework

* Google Agent Development Kit (ADK)

### LLM

* Gemini 2.5 Flash

### Language

* Python 3.10+

---

# 📦 Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd customer_support_agent
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Setup

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=your_google_api_key
```

Get your API key from:

https://aistudio.google.com/app/apikey

---

# ▶️ Running the Agent

## Run Using ADK Web Interface

From the parent directory:

```bash
adk web
```

Open:

```text
http://localhost:8000
```

Select:

```text
customer_support_agent
```

and start chatting with the agent.

---

## Run Using ADK CLI

```bash
adk run customer_support_agent
```

---

# 💬 Example Queries

### Shipping Cost

**User**

```text
What is the standard shipping cost?
```

**Agent**

```text
Standard shipping costs $5.99.
```

---

### Free Shipping

**User**

```text
Do you offer free shipping?
```

**Agent**

```text
Orders over $50 qualify for free shipping.
```

---

### Delivery Time

**User**

```text
How long does delivery take?
```

**Agent**

```text
Delivery typically takes 3–5 business days.
```

---

### Returns

**User**

```text
What is your return policy?
```

**Agent**

```text
Returns are accepted within 30 days.
```

---

### Unrelated Question

**User**

```text
Who won the cricket match yesterday?
```

**Agent**

```text
I am sorry, but I can only answer questions related to shipping (shipping rates, tracking, delivery, or returns).
```

---

# 🧠 Workflow Logic

## Classifier Agent

The classifier agent evaluates incoming user questions and determines whether they are related to shipping.

Supported topics:

* Shipping costs
* Delivery times
* Tracking
* Returns
* Shipping policies

---

## Routing Logic

```python
if "shipping" in text:
    route = "shipping"
else:
    route = "unrelated"
```

The workflow then routes the request to the appropriate node.

---

## Shipping FAQ Agent

Handles:

* Shipping rates
* Delivery timelines
* Return policies
* General shipping support

Model:

```python
gemini-2.5-flash
```

---

## Decline Node

Handles questions outside the supported domain.

Example:

```text
Politics
Sports
Movies
General Knowledge
Coding Questions
```

---

# 🔄 Workflow Execution Process

```text
Step 1:
User submits question

Step 2:
Classifier Agent analyzes query

Step 3:
Workflow determines route

Step 4:
Shipping FAQ Agent OR Decline Node executes

Step 5:
Response returned to user
```

---

# 🛠 Dependencies

```text
google-adk >= 2.0.0
```

Install manually:

```bash
pip install google-adk
```

---

# 📚 Learning Objectives

This project demonstrates:

* Agent-based application design
* Workflow orchestration
* Multi-agent routing
* Event-driven AI systems
* Google ADK fundamentals
* Gemini integration

---

# 🎯 Future Improvements

* Order tracking integration
* Live shipment status
* CRM integration
* Customer authentication
* Knowledge base retrieval (RAG)
* Multi-language support
* Human handoff workflow

---

# 📜 License

This project is created for educational and learning purposes using Google ADK and Gemini models.

---

# 👨‍💻 Author

**Deep Pakhare**

Built as part of the **AI Agents & Agentic Engineering Learning Journey** using Google ADK.
