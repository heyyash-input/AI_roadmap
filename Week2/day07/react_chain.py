
import os
import json
import ast
import operator

from dotenv import load_dotenv
from groq import Groq


# ==========================================
# 1. GROQ CONFIGURATION
# ==========================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)

model = "openai/gpt-oss-20b"


# ==========================================
# 2. TOOL FUNCTIONS
# ==========================================

def get_product_price(product):
    prices = {
        "iPhone 17": 1000,
        "iPhone 15": 500
    }

    return prices.get(product, 0)


def calculator(expression):

    # Safe arithmetic evaluator, no eval()
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
    }

    def evaluate(node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

        elif isinstance(node, ast.BinOp):
            op = type(node.op)

            if op in allowed_operators:
                return allowed_operators[op](
                    evaluate(node.left),
                    evaluate(node.right)
                )

        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -evaluate(node.operand)

            if isinstance(node.op, ast.UAdd):
                return evaluate(node.operand)

        raise ValueError("Invalid arithmetic expression")

    try:
        tree = ast.parse(expression, mode="eval")
        return evaluate(tree.body)

    except Exception:
        return "Calculation error"


# ==========================================
# 3. AVAILABLE TOOLS
# ==========================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Get the price of a product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "Product name"
                    }
                },
                "required": ["product"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform arithmetic calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# Map tool names to Python functions
available_functions = {
    "get_product_price": get_product_price,
    "calculator": calculator
}


# ==========================================
# 4. SYSTEM PROMPT
# ==========================================

system_prompt = """
You are a shopping assistant.

You can use these tools:

1. get_product_price(product)
2. calculator(expression)

Instructions:

1. Understand the user's question.
2. Decide which tool is required.
3. Call only the necessary tool.
4. Use the tool result to continue solving the task.
5. Never invent tool results.
6. Give a clear final answer when finished.
7. You may call multiple tools sequentially.
"""


# ==========================================
# 5. REACT AGENT
# ==========================================

def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(5):

        print("\n------------------")
        print("STEP", step + 1)
        print("------------------")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0
        )

        assistant_message = response.choices[0].message

        # Add assistant response to conversation
        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        # Check whether model wants to call a tool
        tool_calls = assistant_message.tool_calls

        if not tool_calls:

            print("\nFINAL ANSWER:")
            print(assistant_message.content)

            return assistant_message.content

        # Execute requested tools
        for tool_call in tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print("\nACTION:", tool_name)
            print("INPUT:", arguments)

            if tool_name in available_functions:

                function = available_functions[tool_name]

                observation = function(**arguments)

            else:

                observation = "Tool not found"

            print("OBSERVATION:", observation)

            # Send observation back to LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(observation)
            })

    print("\nMaximum steps reached.")
    return None


# ==========================================
# 6. RUN AGENT
# ==========================================

prompt = """
I have 5000 rupees.

What is the price of an iPhone 17?
And how much money will I have left?
"""

run_agent(prompt)
