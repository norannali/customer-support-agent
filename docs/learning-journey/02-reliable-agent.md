# **Learning Journey — Milestone 02: Building a Reliable Customer Support Agent**

**Date:** October 2026

**Project Version:** v0.2.0

**Status:** Completed

---

## **Main Notes**

In this milestone, I focused on making the basic customer support agent more reliable and predictable.

The main improvements were:

* Improving structured response reliability
* Handling missing orders explicitly
* Preventing unauthorized order access
* Distinguishing existing refunds from new refund requests
* Enforcing the refund policy programmatically
* Testing edge cases and boundary conditions
* Validating the complete agent flow
* Performing regression testing after changes

The main engineering principle I learned in this milestone was:

> **The LLM should interpret requests and orchestrate actions, while deterministic application logic should enforce critical business rules.**

---

## **Deep Understanding**

### 1. Improving Structured Output Reliability

In Milestone 01, I discovered that having a Pydantic schema does not guarantee that the LLM will populate every field correctly.

For example, the model could return the order information inside the natural-language `message` field while leaving:

```text
orders = []
```

The response could still be technically valid according to the schema, but it would not contain the structured information I actually needed.

Instead of weakening the schema, I kept `OrderInfo` strict and improved the information available to the model.

The `calculate_refund()` tool was updated to return the complete order context:

```text
order_id
product
status
tracking_number
delivery_date
```

along with the refund decision.

This gave the model enough information to construct a complete `OrderInfo` object.

### Key Lesson

> **A structured-output schema provides a response contract, but it does not guarantee correct semantic population of the fields.**

---

### 2. Missing Order Handling

I tested:

> "I'm customer C001. What's the status of order ORD999?"

The agent called:

```text
get_order(C001, ORD999)
```

The tool returned:

```text
{"error": "Order not found"}
```

The agent correctly:

* Did not retrieve all other customer orders
* Informed the customer that the order does not exist
* Asked the customer to verify the order ID

Result:

**PASS**

This showed that an agent should handle tool errors explicitly instead of making assumptions or silently changing the requested operation.

---

### 3. Unauthorized Order Access

I tested:

> "I'm customer C001. What's the status of order ORD103?"

ORD103 belongs to customer C002.

The `get_order()` tool rejected the request:

```text
This order does not belong to this customer
```

The agent did not expose the order information.

### Important Engineering Lesson

Authorization should not rely only on the system prompt.

The tool itself must enforce ownership.

The flow is:

```text
LLM
 ↓
Select get_order()
 ↓
Tool validates customer ownership
 ↓
Authorized data OR error
 ↓
LLM
 ↓
Final response
```

Result:

**PASS**

---

### 4. Existing Refund Status

The initial refund logic mainly handled refund eligibility.

However, an existing refund request is a different situation.

ORD102 already contains:

```text
refund_requested = true
refund_status = Processing
```

The `calculate_refund()` tool was updated to detect an existing refund request and return its current status.

For ORD102, the tool returned:

```text
refund_requested = true
refund_status = Processing
refund_amount = 1500
currency = EGP
```

The agent then correctly informed the customer that the refund was still being processed.

Result:

**PASS**

---

### 5. Enforcing the Refund Policy

The refund policy states:

```text
Customers can request a refund within 30 days
of delivery.
```

The original implementation did not enforce this rule programmatically.

I added date-based validation to `calculate_refund()`.

The logic is:

```text
days_since_delivery <= 30
        ↓
Eligible

days_since_delivery > 30
        ↓
Not eligible
```

The 30th day is included in the allowed window.

---

### Why the Rule Is Implemented in Python

I did not rely on the LLM to calculate refund eligibility.

The LLM can understand the customer's request and decide which tool to use, but the actual business rule should be deterministic.

The flow is:

```text
Customer Request
       ↓
      LLM
       ↓
calculate_refund()
       ↓
Deterministic Business Rules
       ↓
Eligibility Result
       ↓
      LLM
       ↓
Structured Response
```

This makes the behavior easier to test, debug, and maintain.

---

### 6. Refund Eligibility Testing

I tested the refund logic with several scenarios:

| Scenario                        | Expected Result      | Actual Result |
| ------------------------------- | -------------------- | ------------- |
| Delivered 19 days ago           | Eligible             | PASS          |
| Delivered exactly 30 days ago   | Eligible             | PASS          |
| Delivered more than 30 days ago | Not eligible         | PASS          |
| Order not delivered             | Not eligible         | PASS          |
| Order already refunded          | Not eligible         | PASS          |
| Existing refund request         | Return refund status | PASS          |

---

### 7. Boundary Testing

I specifically tested the boundary of the 30-day refund window.

For a delivery date of:

```text
2026-09-05
```

and the current date:

```text
2026-10-05
```

the difference is exactly:

```text
30 days
```

The result was:

```text
eligible = True
```

I also tested a delivery date of:

```text
2026-09-04
```

which resulted in:

```text
31 days
```

The result was:

```text
eligible = False
```

This confirmed that the implementation correctly handles the policy boundary.

---

### 8. Data Consistency

While implementing the refund policy, I found that ORD103 originally contained:

```text
return_days = 14
```

However, the official refund policy specifies a 30-day window.

Having both values could create conflicting sources of truth.

Since the official policy should determine refund eligibility, I removed the conflicting `return_days` field from ORD103.

The policy is now treated as the source of truth.

---

## **Experiments & Results**

### Test 1 — Normal Refund Eligibility

Question:

> "I'm customer C002. Can I get a refund for order ORD103?"

The agent performed:

```text
get_customer(C002)
        ↓
calculate_refund(ORD103, C002)
        ↓
Structured Response
```

Result:

```text
Order: ORD103
Product: Keyboard
Status: Delivered
Refund Eligible: True
Refund Amount: 1000 EGP
```

**PASS**

---

### Test 2 — Expired Refund

I temporarily changed the delivery date during runtime to simulate an expired order.

The tool returned:

```text
eligible = False
reason = The refund request is outside the 30-day refund window
```

The agent then produced a structured response with:

```text
refund_eligible = False
refund_amount = None
refund_reason = The refund request is outside the 30-day refund window
```

The model did not invent a refund amount.

**PASS**

---

### Test 3 — Existing Refund

Question:

> "I'm customer C001. What's the status of my refund for order ORD102?"

The agent used:

```text
get_order(ORD102)
        ↓
calculate_refund(ORD102, C001)
```

Result:

```text
Refund Status: Processing
Refund Amount: 1500 EGP
```

**PASS**

---

### Test 4 — Missing Order

Question:

> "I'm customer C001. What's the status of order ORD999?"

The agent called:

```text
get_order(C001, ORD999)
```

The tool returned:

```text
Order not found
```

The agent responded that the order does not exist and asked the customer to verify the order ID.

The structured response contained:

```text
orders = []
```

**PASS**

---

### Test 5 — Unauthorized Order

Question:

> "I'm customer C001. What's the status of order ORD103?"

Since ORD103 belongs to C002, the tool rejected the request.

The customer's order information was not exposed.

**PASS**

---

### Test 6 — Already Refunded

I tested the `returned=True` branch temporarily in memory without modifying the stored dataset.

The tool returned:

```text
eligible = False
reason = This order has already been refunded
```

**PASS**

---

### Test 7 — Refund Policy Retrieval

Question:

> "I'm customer C002. What is your refund policy?"

The agent called:

```text
search_policy()
```

and correctly retrieved the refund policy, including:

* 30-day refund window
* Acceptable product condition
* 5–7 business day processing time
* Non-refundable shipping fees
* No duplicate refunds
* Refund amount equals the product price

**PASS**

---

## **Regression Testing**

After modifying the refund logic, previously working scenarios were tested again.

### Existing Refund

```text
ORD102
→ Processing
→ 1500 EGP
```

**PASS**

### Missing Order

```text
ORD999
→ Order does not exist
→ orders = []
```

**PASS**

### Normal Refund

```text
ORD103
→ Delivered
→ Eligible
→ 1000 EGP
```

**PASS**

The regression tests confirmed that the new refund-policy logic did not break the previously implemented behavior.

---

## **Challenges & Debugging**

The main challenge in this milestone was not the date calculation itself.

The more important issue was understanding **where business logic should live in an agentic system**.

Initially, the refund tool returned only the eligibility result.

This caused the LLM to sometimes lack enough information to populate the complete `OrderInfo` structure.

I solved this by returning the relevant order context directly from the tool.

This reinforced the idea that:

> **Tools should return reliable, sufficient context for the task they perform.**

At the same time, deterministic rules should remain inside the tool instead of being delegated to the LLM.

---

## **Active Recall**

### Why shouldn't the LLM calculate refund eligibility?

Because refund eligibility is a deterministic business rule. It should be enforced by application logic so that the result is predictable and testable.

### Why did I keep `OrderInfo` strict?

Because making required fields optional would hide the underlying information-flow problem instead of fixing it.

### Why does `calculate_refund()` return order information?

Because the structured response requires complete order information, and the model needs that context to populate `OrderInfo` correctly.

### Why is ownership checked inside `get_order()`?

Because authorization should be enforced by the application/tool layer rather than relying on the LLM to follow a prompt instruction.

### What is boundary testing?

Boundary testing checks values around the limit of a rule.

For the refund policy:

```text
30 days → allowed
31 days → rejected
```

---

## **Key Takeaways**

This milestone helped me understand that building an agent is not only about making the LLM call tools successfully.

A reliable agent also requires:

* Strong schemas
* Deterministic business logic
* Tool-level validation
* Authorization checks
* Explicit error handling
* Edge-case testing
* Regression testing
* Sufficient tool context

The resulting architecture is:

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │      LLM        │
                    │ Interpretation  │
                    │ + Orchestration │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │      Tools      │
                    │ Validation +    │
                    │ Business Rules  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Reliable Result │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Structured      │
                    │ Response        │
                    └─────────────────┘
```

---

## 🚀 Next Steps

The next milestone will focus on moving from manually validated reliability toward more systematic testing and stronger agent architecture.

Planned improvements:

* Add automated tests with `pytest`
* Increase tool-level test coverage
* Improve policy search
* Improve error handling
* Add better observability for agent trajectories
* Test more complex multi-step requests
* Explore more advanced agent behavior
* Continue documenting implementation decisions and debugging experiments

This will become:

**Milestone 03 — Testing & Advanced Agent Behavior**
