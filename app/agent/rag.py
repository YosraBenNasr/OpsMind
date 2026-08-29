import os
from typing import List
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

INCIDENTS_DIR = "incidents"
FAISS_INDEX_PATH = "data/faiss_incidents_index"

# Utilisation d'un modèle d'embeddings open-source performant et léger
EMBEDDINGS_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def build_or_load_vectorstore() -> FAISS:
    """
    Charge l'index FAISS existant depuis le disque.
    S'il n'existe pas, il lit les fiches incidents/*.md, les découpe et crée l'indexation.
    """
    if os.path.exists(FAISS_INDEX_PATH):
        print("⚡ [RAG] Chargement de l'index FAISS existant...")
        return FAISS.load_local(
            FAISS_INDEX_PATH, 
            EMBEDDINGS_MODEL, 
            allow_dangerous_deserialization=True
        )

    print("🔨 [RAG] Indexation initiale des fiches d'incidents...")
    if not os.path.exists(INCIDENTS_DIR):
        raise FileNotFoundError(f"Le dossier '{INCIDENTS_DIR}' est introuvable.")

    # Chargement de tous les fichiers .md du dossier incidents/ avec TextLoader
    loader = DirectoryLoader(INCIDENTS_DIR, glob="*.md", loader_cls=TextLoader)
    documents = loader.load()

    # Découpage du texte en tronçons contextuels (chunks)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs_chunks = text_splitter.split_documents(documents)

    # Création du magasin vectoriel FAISS
    vectorstore = FAISS.from_documents(docs_chunks, EMBEDDINGS_MODEL)
    
    # Sauvegarde sur le disque
    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    vectorstore.save_local(FAISS_INDEX_PATH)
    print("✅ [RAG] Indexation terminée et sauvegardée dans", FAISS_INDEX_PATH)
    
    return vectorstore

def retrieve_incident_context(query: str, top_k: int = 2) -> List[str]:
    """
    Effectue une recherche par similarité vectorielle pour extraire les fiches 
    d'incidents les plus pertinentes en rapport avec la panne.
    """
    try:
        vectorstore = build_or_load_vectorstore()
        results = vectorstore.similarity_search(query, k=top_k)
        return [doc.page_content for doc in results]
    except Exception as e:
        print(f"⚠️ [RAG Error] Échec de la récupération contextuelle : {str(e)}")
        return []