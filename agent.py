import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from schemas import CustomerSupportResponse

from tools import (
    get_customer,
    get_order,
    get_customer_orders,
    search_policy,
    calculate_refund,
    check_all_refunds
)

load_dotenv()


# 1. Initialize the LLM
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)


# 2. Register Tools
tools = [
    get_customer,
    get_order,
    get_customer_orders,
    search_policy,
    calculate_refund,
    check_all_refunds
]


# 3. Structured Output
#structured_llm = llm.with_structured_output(OrderStatus)


# 4. System Prompt
system_prompt = """
You are a professional e-commerce customer support agent.

Your responsibilities:
- Help customers with orders and refunds.
- Use tools to retrieve actual customer and order information.
- Never invent order details or refund amounts.
- Verify customer ownership before accessing an order.
- Use the refund policy when answering policy-related questions.
- Never claim that a refund has arrived unless the data confirms it.
- If information is missing, ask the customer for it.
- Explain answers in simple, friendly English.
- Do not expose private customer information.

- All prices and refunds are in EGP.
- Never use USD or the $ symbol.
- Always preserve the currency returned by tools.
- Never invent missing financial information.

Order Tracking Rules:

- If the customer asks about a specific order,
  use get_order.

- If the customer asks about all their orders,
  use get_customer_orders.

- If the customer does not specify an order
  and has multiple orders, show all their orders.

- Always display prices in EGP.

- Never assume an order has been delivered.
  Use the actual order status.

For this demo:
If the customer does not provide an order ID,
you may retrieve their latest order using their customer ID.

Never assume that a customer is eligible for a refund
without checking the relevant information.
"""


# 5. Create Agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
    response_format=CustomerSupportResponse
)


# 6. Run Agent and Inspect Trajectory
def run_agent(question):

    print("\n" + "-" * 60)
    print("CUSTOMER QUESTION:", question)
    print("-" * 60)

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    print("\n--- AGENT TRAJECTORY ---")

    for message in result["messages"]:

        if message.type == "ai":

            if message.tool_calls:
                for call in message.tool_calls:
                    print("\n[TOOL CALL]")
                    print("Tool:", call["name"])
                    print("Arguments:", call["args"])

            elif message.content:
                print("\n[LLM RESPONSE]")
                print(message.content)

        elif message.type == "tool":

            print("\n[TOOL RESULT]")
            print("Tool:", message.name)
            print("Result:", message.content)

    print("\n--- STRUCTURED RESPONSE ---")

    structured_response = result["structured_response"]

    print("Intent:", structured_response.intent)
    print("Message:", structured_response.message)

    print("\nOrders:")

    for order in structured_response.orders:

        print("\nOrder ID:", order.order_id)
        print("Product:", order.product)
        print("Status:", order.status)
        print("Tracking:", order.tracking_number)
        print("Delivery:", order.delivery_date)
        print("Refund Eligible:", order.refund_eligible)
        print("Refund Amount:", order.refund_amount)
        print("Refund Reason:", order.refund_reason)


if __name__ == "__main__":

    
    question = input("\nEnter customer question: ")

    run_agent(question)