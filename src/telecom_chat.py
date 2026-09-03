from openai import OpenAI
client = OpenAI()
conversation = []

print("Welcome to the AI Chatbot! Type 'exit' to end the conversation.")

while(True):
    user_input = input("You:")
    if user_input.lower() =="exit":
        print("Ending the conversation. Goodbye!")
        break
    else:
        conversation.append({"role":"user", "content":user_input})
        response = client.responses.create(model = 'gpt-5.6-luna',input =conversation)
        conversation.append({"role":"assistant", "content":response.output_text})
        print("\nAssistant:", response.output_text, "\n")




