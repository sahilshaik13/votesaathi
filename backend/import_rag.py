import vertexai
from vertexai.preview import rag
from config import GCP_PROJECT_ID, GCP_LOCATION, RAG_CORPUS_ID

def import_rag_documents():
    print(f"Initializing Vertex AI in {GCP_LOCATION} for {GCP_PROJECT_ID}...")
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
    
    # We must use the full resource name
    corpus_name = f"projects/{GCP_PROJECT_ID}/locations/{GCP_LOCATION}/ragCorpora/{RAG_CORPUS_ID}"
    print(f"Importing files into Corpus: {corpus_name}")
    
    try:
        response = rag.import_files(
            corpus_name=corpus_name,
            paths=["gs://votesaathi-rag-documents-495109-1777729892/"],
            chunk_size=1000,
            chunk_overlap=200
        )
        print("Import successfully finished!")
        print(f"Imported files count: {response.imported_rag_files_count}")
        print(f"Failed files count: {response.failed_rag_files_count}")
    except Exception as e:
        print(f"Error importing files: {e}")

if __name__ == "__main__":
    import_rag_documents()
