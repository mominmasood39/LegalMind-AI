from pinecone import Pinecone
from backend.config import settings

pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX_NAME)

# If you DO NOT use namespaces:
index.delete(deleteAll=True)

# If you DO use a namespace, comment the line above and use this:
# index.delete(deleteAll=True, namespace="legal")

print("✅ All vectors deleted.")