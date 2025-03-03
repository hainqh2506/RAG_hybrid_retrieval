from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.google import Gemini
from dotenv import load_dotenv
import os
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.knowledge.langchain import LangChainKnowledgeBase
from hybrid_search import hybrid_retriever
from agno.playground import Playground, serve_playground_app
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
#Create a storage backend using the Sqlite database

storage = SqliteAgentStorage(
    # store sessions in the ai.sessions table
    table_name="agent_sessions",
    # db_file: Sqlite database file
    db_file="tmp/data.db",
)
retriever = hybrid_retriever("raptor")
knowledge_base = LangChainKnowledgeBase(retriever=retriever)


#================================================================================================
# db_uri = "tmp/lancedb"
# # Create a knowledge base from a PDF
# knowledge_base = PDFUrlKnowledgeBase(
#     urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
#     # Use LanceDB as the vector database
#     vector_db=LanceDb(table_name="recipes", uri=db_uri, search_type=SearchType.vector),
# )
# # Load the knowledge base: Comment out after first run
# knowledge_base.load(upsert=True)
# # -*- Create a knowledge base from the vector store
#================================================================================================

def get_rag_agent():
    return Agent(
    tools=[DuckDuckGoTools()],
    model=Gemini(id="gemini-2.0-flash-exp", api_key=GEMINI_API_KEY),
    show_tool_calls=True,
    name="Information Retrieval Agent",
    role="Tìm kiếm thông tin phù hợp dựa trên tools và knowledge base",
    storage=storage,
    description="Bạn là trợ lý ảo AI của đại học ABC",
    search_knowledge=True,
    knowledge=knowledge_base, 
    read_chat_history=True,
    read_tool_call_history=True,
    instructions=[
        "Tìm kiếm trong knowledge_base nếu hỏi về đại học Bách Khoa Hà Nội.",
        "If the question is better suited for the web, search the web to fill in gaps.",
        "Prefer the information in your knowledge base over the web results."
    ],
    goal="Tìm kiếm thông tin phù hợp dựa trên tools và knowledge base",
    markdown=True,
    debug_mode=True,
)
