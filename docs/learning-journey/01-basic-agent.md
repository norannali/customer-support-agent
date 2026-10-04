# **Learning Journey — Milestone 01: Building the Basic Customer Support Agent**

**Date:** October 2026
**Project Version:** v0.1.0
**Status:** Completed

##  **Main Notes**

In this milestone, I built a basic AI-powered customer support agent using LangChain and an LLM.

The agent can understand customer requests, choose appropriate tools, execute them, use the returned information, and generate a final response.

The main concepts explored in this milestone were:

* LLMs
* Tool Calling
* Tool Descriptions and Schemas
* Agent Loop
* Multi-step Tool Use
* Dynamic Tool Selection
* Structured Output
* Pydantic-based response schemas

---

##  **Deep Understanding**

### 1. Tool Calling

An LLM does not directly execute Python functions.

Instead, the available tools are provided to the model with information such as:

* Tool name
* Tool description
* Expected input parameters
* Input schema

For example:

```python
@tool
def get_order(order_id: str):
    """Get order details using the order ID."""
```

The model can understand that `get_order` is responsible for retrieving order information and that it requires an `order_id`.

For a request such as:

> "Where is my order ORD101?"

the model can decide to call:

```text
get_order(order_id="ORD101")
```

The agent runtime then executes the actual Python function and returns the result to the model.

So the process is:

```text
User Request
     ↓
LLM
     ↓
Select Tool + Generate Arguments
     ↓
Agent Runtime
     ↓
Execute Python Tool
     ↓
Tool Result
     ↓
LLM
     ↓
Final Response or Another Tool Call
```

### 2. Agent Loop

A simple LLM interaction can follow:

```text
User → LLM → Answer
```

An agent can instead perform multiple actions:

```text
User
 ↓
LLM
 ↓
Choose Tool
 ↓
Execute Tool
 ↓
Tool Result
 ↓
LLM
 ↓
Need more information?
 ├── Yes → Another Tool Call
 └── No  → Final Answer
```

The important point is that the agent does **not** have to follow a fixed sequence of tools.

It dynamically chooses the next action based on the user's request and the information available so far.

For example:

```text
User:
"Where is my order ORD101?"

        ↓

get_order(ORD101)

        ↓

status = Shipped
tracking = TRK123
delivery_date = 2026-10-05

        ↓

Enough information?

        ↓

Yes

        ↓

Final Answer
```

There is no reason to call `search_policy()` or `calculate_refund()` because the result of `get_order()` already contains the information needed to answer the question.

This helped me understand the difference between an **agent** and a fixed workflow:

```text
Fixed Workflow:
Tool A → Tool B → Tool C

Agent:
Choose next action based on the current information.
```

### 3. Multi-step Tool Use

For more complex requests, the agent can perform multiple tool calls.

Example:

> "Tell me the status of all my orders and whether I can get a refund for each one."

A possible trajectory is:

```text
get_customer_orders(C001)
        ↓
calculate_refund(ORD101, C001)
        ↓
calculate_refund(ORD102, C001)
        ↓
Final Response
```

Each tool result becomes part of the context available to the agent for the next decision.

---

##  **Implementation**

The agent was implemented using LangChain's agent functionality with:

* An LLM connected through OpenRouter
* Python-based tools
* Pydantic schemas for structured responses
* Customer and order test data
* A refund policy document

The main tools currently include:

```text
get_customer()
get_order()
get_customer_orders()
search_policy()
calculate_refund()
check_all_refunds()
```

---

##  **Experiments & Results**

One of the main experiments tested a multi-step customer request:

> "I'm customer C001. Tell me the status of all my orders and whether I can get a refund for each one."

The agent successfully performed multiple tool calls:

```text
get_customer_orders(C001)
        ↓
calculate_refund(ORD101, C001)
        ↓
calculate_refund(ORD102, C001)
```

The tools returned:

* ORD101: Shipped → refund not currently eligible
* ORD102: Delivered → refund eligible for 1500 EGP

This demonstrated that the agent can perform a multi-step trajectory instead of relying on a single tool call.

---

##  **Challenges & Debugging**

The first structured response implementation revealed an important limitation.

The Pydantic schema expected order information inside:

```text
orders[]
```

However, the model returned the order details inside the natural-language `message` field while leaving:

```text
orders = []
```

The response was technically schema-valid, but the structured data was not populated in the way intended.

This showed me that:

> **Structured output provides a response contract, but it does not guarantee that the model will semantically populate every field correctly.**

This will be addressed in the next milestone through stronger validation and more reliable structured-output handling.

---

##  **Active Recall**

Questions I can now answer:

**How does an LLM choose a tool?**

It uses the available tool names, descriptions, and input schemas to determine which tool is relevant to the user's request and generates the required arguments.

**Does the LLM execute the Python function itself?**

No. The agent runtime executes the actual tool and sends the result back to the LLM.

**What is the Agent Loop?**

It is the iterative process where the agent selects an action, executes it, receives the result, and decides whether it needs another action or can produce the final answer.

**Does an agent always call every available tool?**

No. It dynamically chooses the tools required for the current task.

---

## 🚀 Next Steps

The next milestone will focus on making the agent more reliable:

* Improve structured output reliability
* Add stronger validation
* Improve tool descriptions
* Improve error handling
* Test edge cases
* Add proper automated tests
* Review and improve refund-policy logic

This will become **Milestone 02 — Reliable Agent**.
