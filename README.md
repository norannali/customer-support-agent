# Customer Support Agent

An evolving AI-powered customer support agent built with LangChain, LLMs, and tool calling.

This project is being developed incrementally as a practical learning journey toward building reliable and production-oriented Agentic AI systems.

## Current Version

**v0.1.0 — Initial Agent**

The current version demonstrates a basic customer support agent that can:

* Retrieve customer information
* Retrieve individual orders
* Retrieve all orders for a customer
* Search customer support policies
* Check refund eligibility
* Calculate refund amounts
* Perform multi-step tool calling
* Return responses using a Pydantic structured output schema

## Architecture

```text
User
  ↓
LangChain Agent
  ↓
LLM
  ↓
Tool Calling
  ├── get_customer
  ├── get_order
  ├── get_customer_orders
  ├── search_policy
  ├── calculate_refund
  └── check_all_refunds
  ↓
Tool Results
  ↓
LLM
  ↓
Structured Response
```

## Tech Stack

* Python
* LangChain
* LangChain OpenAI integration
* OpenRouter
* Pydantic
* python-dotenv

## Project Structure

```text
customer-support-agent/
│
├── agent.py
├── tools.py
├── data.py
├── schemas.py
├── structured_test.py
├── test_questions.py
├── policies/
│   └── refund_policy.txt
├── .env.example
├── .gitignore
└── requirements.txt
```

## Example Workflow

For a request such as:

> "I'm customer C001. Tell me the status of all my orders and whether I can get a refund for each one."

The agent can:

1. Identify the customer.
2. Retrieve the customer's orders.
3. Check refund eligibility for each order.
4. Use the tool results to generate the final response.

## Current Limitations

This is an evolving learning project, not a production-ready customer support system.

Current limitations include:

* Structured response fields are not always populated as intended.
* Refund policy enforcement is still simplified.
* Customer and order data are currently stored in Python data structures.
* No persistent conversation memory yet.
* No RAG pipeline yet.
* No automated evaluation framework yet.
* No production database or API layer yet.

## Learning Journey

The project is being developed incrementally.

Planned milestones include:

1. Basic Agent
2. Reliable Agent
3. Conversation Memory
4. RAG
5. LangGraph Workflows
6. Advanced Agentic AI Patterns
7. Evaluation and Observability
8. Production Engineering

Each milestone will be implemented, tested, documented, and committed separately to preserve the project's development history.
