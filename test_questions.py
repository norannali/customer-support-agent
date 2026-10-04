from agent import run_agent

questions = [
    "I'm customer C001. Where is my order?",

    "I'm customer C001. Why hasn't my refund arrived?",

    "I'm customer C001. Am I eligible for a refund?",

    "I'm customer C001. How much will I get refunded for order ORD102?",

    "What is your refund policy?"
]

for index, question in enumerate(questions, 1):

    print(f"\nTEST CASE {index}")

    run_agent(question)