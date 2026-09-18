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

    # Initial LLM request
    response = router.completion(
        model="telecom-agent",
        messages=messages,
        tools = LITELLM_TOOLS
    )
    while response.choices[0].message.tool_calls:

        assistant_message = response.choices[0].message

        messages.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": assistant_message.tool_calls
        })

        for tool_call in assistant_message.tool_calls:

            result = execute_tool(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )

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
