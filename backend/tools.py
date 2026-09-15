import json

from .billing_data_tool import (
    get_customer_details,
    get_account_details,
    get_product_billing_information,
    get_billing_information,
    get_customer_billing_information,
)

VECTOR_STORE_ID = 'vs_6a9e87674fb4819181ce5a86d8fb610a'

TOOLS = [
    {
        "type": "file_search",
        "vector_store_ids": [VECTOR_STORE_ID]
    },
    {
        "type": "function",
        "name": "get_customer_details",
        "description": "Retrieve customer details using a customer ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Customer ID, such as C1001."
                }
            },
            "required": ["customer_id"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_account_details",
        "description": "Retrieve account details using an account ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "account_id": {
                    "type": "string",
                    "description": "Account ID, such as A1002."
                }
            },
            "required": ["account_id"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_product_billing_information",
        "description": (
            "Retrieve a product and its related bills, bill items, "
            "and billing events."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "Product ID, such as P10002."
                }
            },
            "required": ["product_id"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_billing_information",
        "description": (
            "Retrieve a bill and its related bill items and events."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "bill_id": {
                    "type": "string",
                    "description": "Bill ID, such as B10001."
                }
            },
            "required": ["bill_id"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_customer_billing_information",
        "description": (
            "Retrieve all accounts, products, bills, bill items, "
            "and events for a customer."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Customer ID, such as C1001."
                }
            },
            "required": ["customer_id"],
            "additionalProperties": False
        },
        "strict": True
    }
]


def execute_tool(tool_name, arguments):
    """Execute an AI-requested billing tool."""

    if tool_name == "get_customer_details":
        return get_customer_details(arguments["customer_id"])

    if tool_name == "get_account_details":
        return get_account_details(arguments["account_id"])

    if tool_name == "get_product_billing_information":
        return get_product_billing_information(arguments["product_id"])

    if tool_name == "get_billing_information":
        return get_billing_information(arguments["bill_id"])

    if tool_name == "get_customer_billing_information":
        return get_customer_billing_information(arguments["customer_id"])

    return {
        "error": f"Unknown tool: {tool_name}"
    }