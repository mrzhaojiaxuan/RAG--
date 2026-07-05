import streamlit as st
from rag import RagService

st.title('智能客服')
st.divider()

# 1. 初始化对话记录（统一键名 messages）
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role":"assistant","content":"您好,有什么可以帮助你?"}]

# 2. 初始化RAG服务
if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# 3. 固定会话ID，用于LangChain对话历史记忆
SESSION_ID = "streamlit_user_001"

# 渲染历史聊天记录
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入框
prompt = st.chat_input()

# 只有输入不为空时才执行逻辑
if prompt:
    # 渲染用户消息并存入会话
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    ai_res_list = []

    with st.spinner("AI思考中..."):
        # 定义分片捕获生成器，收集完整回答同时流式输出
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        # ===== LangChain 标准流式调用（适配你的RagService）=====
        # 入参字典 + 携带session_id的config配置
        stream_input = {"input": prompt}
        stream_config = {"configurable": {"session_id": SESSION_ID}}
        res_stream = st.session_state["rag"].chain.stream(stream_input, config=stream_config)

        # 前端流式打字机输出
        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))

    # 拼接所有分片得到完整回答，存入对话历史
    res_full = "".join(ai_res_list)
    st.session_state["messages"].append({"role": "assistant", "content": res_full})