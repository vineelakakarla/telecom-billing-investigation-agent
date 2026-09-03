from openai import OpenAI 
client = OpenAI()

prompt = input("Enter Your Prompt")

response = client.responses.create(model='gpt-5.6-luna', input=prompt)
print("\nAI Response:")
print(response.output)
