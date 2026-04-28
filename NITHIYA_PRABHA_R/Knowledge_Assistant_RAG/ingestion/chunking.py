from langchain_text_splitters import RecursiveCharacterTextSplitter

#splitting the documents into smaller chunks
def split_docs(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,  #adjusting based on the model's context window and document size  
        chunk_overlap=30 
    )
    return splitter.split_documents(documents)

    