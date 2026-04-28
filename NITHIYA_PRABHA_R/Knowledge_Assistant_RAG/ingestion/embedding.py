from langchain_community.embeddings import HuggingFaceEmbeddings

#converting to numeric vectors
def get_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    return embeddings
