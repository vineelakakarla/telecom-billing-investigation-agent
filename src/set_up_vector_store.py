from openai import OpenAI

client = OpenAI()

# Create a vector store
vector_store = client.vector_stores.create(
    name="Telecom Billing Knowledge"
)

print("Vector store created:")
print(vector_store.id)

# Upload the knowledge file
with open("data/billing_knowledge.txt", "rb") as file:
    uploaded_file = client.files.create(
        file=file,
        purpose="assistants"
    )

# Add the uploaded file to the vector store
vector_store_file = client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=uploaded_file.id
)

print("File uploaded:")
print(vector_store_file.id)

print("\nSave this Vector Store ID:")
print(vector_store.id)