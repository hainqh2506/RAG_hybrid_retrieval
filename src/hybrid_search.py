from dotenv import load_dotenv
from langchain_elasticsearch import ElasticsearchRetriever
from typing import Dict, Optional, List
from sentence_transformers import SentenceTransformer
import os
from model_config import VietnameseEmbeddings
# Configure logging with UTF-8 encoding
load_dotenv()
embeddings = VietnameseEmbeddings()
ELASTIC_URL = os.getenv("ELASTIC_URL")
elastic_api_key = os.getenv("elastic_api_key")
def hybrid_query(search_query: str, k_vector: int = 50, k_final: int = 5) -> Dict:
    """
    Tạo truy vấn kết hợp full-text search và vector search rồi rerank để lấy 5 kết quả tốt nhất.

    Tham số:
    - search_query: Câu hỏi người dùng cần tìm kiếm.
    - k_text: Số lượng kết quả tìm kiếm full-text.
    - k_vector: Số lượng kết quả tìm kiếm vector.
    - k_final: Số lượng kết quả rerank cuối cùng.

    Trả về:
    - Truy vấn Elasticsearch.
    """
    # Chuyển câu hỏi thành vector embedding
    vector = embeddings.embed_query(search_query)
    
    return {
        "retriever": {
            "rrf": {
                "retrievers": [
                    {
                        "standard": {
                            "query": {
                                "match": {
                                    "text": search_query,
                                }
                            }
                        }
                    },
                    {
                        "knn": {
                            "field": "vector",
                            "query_vector": vector,
                            "k": k_vector,  # Vector search: tìm kiếm 50 kết quả
                            "num_candidates": k_vector * 2  # Số ứng viên xét là gấp đôi k_vector
                        }
                    },
                ],
            "rank_window_size": k_vector,
            "rank_constant": 60 #default = 60
            }
        }, "size": k_final # Rerank để lấy 5 kết quả tốt nhất
        
    }
def hybrid_retriever(index_name: str) -> ElasticsearchRetriever:
    return  ElasticsearchRetriever.from_es_params(
    index_name=index_name,
    body_func=hybrid_query,
    content_field="text",
    url=  ELASTIC_URL,
    api_key = elastic_api_key
)