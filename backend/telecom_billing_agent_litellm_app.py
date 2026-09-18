import json

from .llm_router import router
from .tools import LITELLM_TOOLS, execute_tool
from .prompts import BILLING_AGENT_INSTRUCTIONS


def investigate_billing(user_input: str) -> str:
    """
    Process a user request using the LiteLLM Router
    and available telecom billing tools.
    """

    messages = [
        {
            "role": "system",
            "content": BILLING_AGENT_INSTRUCTIONS
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    try:
        # Initial LLM request
        response = router.completion(
            model="telecom-agent",
            messages=messages,
            tools=LITELLM_TOOLS
        )

        while response.choices[0].message.tool_calls:

            assistant_message = response.choices[0].message

            messages.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": assistant_message.tool_calls
            })

            for tool_call in assistant_message.tool_calls:

                try:
                    result = execute_tool(
                    tool_call.function.name,
                    json.loads(tool_call.function.arguments)
                    )
                except Exception as e:
                    print(f"Tool execution error: "f"{tool_call.function.name} - {type(e).__name__}: {e}")

                    result = {
                        "status": "ERROR",
                        "message": (
                        "The requested billing information could not be retrieved "
                        "because the billing data service encountered an error."
                        )
                    }

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

            response = router.completion(
                model="telecom-agent",
                messages=messages,
                tools=LITELLM_TOOLS
            )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Billing investigation error: {type(e).__name__}: {e}")

        return (
            "I’m unable to complete the billing investigation right now. "
            "The billing investigation service encountered a temporary "
            "processing error. Please try again later."
        )