from llm_router import router

response = router.completion(
    model="telecom-agent",
    messages=[
        {
            "role": "user",
            "content": "Explain telecom billing in one sentence."
        }
    ]
)

print(response.choices[0].message.content)