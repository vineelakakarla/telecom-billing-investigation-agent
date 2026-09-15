import json

from .llm_router import router
from .tools import TOOLS, execute_tool
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

    # Initial LLM request
    response = router.completion(
        model="telecom-agent",
        messages=messages
    )
    return response.choices[0].message.content

    """# Tool-calling loop
    while True:

        message = response.choices[0].message

        # Model has completed the investigation
        if not message.tool_calls:
            return message.content

        # Add assistant tool-call message
        messages.append(
            message.model_dump(exclude_none=True)
        )

        # Execute requested tools
        for tool_call in message.tool_calls:

            arguments = json.loads(
                tool_call.function.arguments
            )

            result = execute_tool(
                tool_call.function.name,
                arguments
            )

            # Add tool result to conversation
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                }
            )

        # Send tool results back to the LLM
        response = router.completion(
            model="telecom-agent",
            messages=messages
        )"""