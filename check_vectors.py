from app.db.pinecone_client import get_index
try:
    index = get_index()
    stats = index.describe_index_stats()
    print("=" * 40)
    print(f"Total Vectors stored in Pinecone: {stats.total_vector_count}")
    print("=" * 40)
except Exception as e:
    print(f"Error checking Pinecone: {e}")
