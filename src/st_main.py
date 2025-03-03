import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
import time
# from create_agents import get_rag_agent
# @st.cache_resource
# def get_rag_agent():
#     rag_agent = get_rag_agent()
#     return rag_agent
# rag_agent = get_rag_agent()
# Thiết lập giao diện cơ bản
st.set_page_config(page_title="University Assistant", page_icon="🤖")
st.title("University Assistant")
# Hàm get_response với chuỗi cứng
def get_response(user_query, chat_history):
    # response = rag_agent.run(message=user_query)
    s = "có phải bạn vừa nói về "
    response = stream_text(s+user_query)
    return response
def stream_text(text):
    """Generator function để stream từng từ của văn bản"""
    time.sleep(1)
    # Chuỗi mới được thêm vào cuối văn bản
    new_text =text +" Nếu bạn có câu hỏi nào khác hãy cho tôi biết nhé! Mời bạn tham khảo thêm các thông tin khác tại đây: "
    link = "[Sổ tay sinh viên](https://ctsv.hust.edu.vn/#/so-tay-sv)"
    # Streaming từng từ trong văn bản
    for word in new_text.split():
        yield word + " "
        # Nếu muốn điều chỉnh tốc độ stream, có thể thêm time.sleep()
        time.sleep(0.05)
    yield link
    # Sau khi hoàn thành streaming, hiển thị link
    #st.markdown(link)
###app###
def process_user_input(user_query):
    if not user_query:
        return None
    if len(user_query) > 512:
        st.error("Độ dài câu hỏi quá dài, vui lòng nhập câu hỏi ngắn hơn!")
        return None
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))


    st.session_state.chat_history.append(AIMessage(content=response))
    return response
def display_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chat_history.append(AIMessage(
            content="Chào bạn, Tôi là trợ lý ảo của Đại học . Tôi có thể giúp gì cho bạn?"
        ))
    
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

# Main interaction
display_chat_history()
user_query = st.chat_input("Nhập tin nhắn của bạn...")
if user_query:
    process_user_input(user_query)