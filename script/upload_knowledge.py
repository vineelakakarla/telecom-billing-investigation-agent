import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"
VECTOR_STORE_ID = "vs_6a9e87674fb4819181ce5a86d8fb610a"

existing_files = set()

for vector_file in client.vector_stores.files.list(
    vector_store_id=VECTOR_STORE_ID
).data:
    existing_files.add(vector_file.id)

for file_path in KNOWLEDGE_DIR.glob("*.md"):
    print(f"Processing: {file_path.name}")

    with open(file_path, "rb") as file:
        uploaded_file = client.files.create(
            file=file,
            purpose="assistants"
        )

    if uploaded_file.id not in existing_files:
        client.vector_stores.files.create(
            vector_store_id=VECTOR_STORE_ID,
            file_id=uploaded_file.id
        )
        print(f"Added: {file_path.name}")
    else:
        print(f"Already exists: {file_path.name}")

print("Knowledge base update completed.")