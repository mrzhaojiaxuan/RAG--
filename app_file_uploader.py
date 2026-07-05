"""
上传文件 知识库更新服务
"""
import streamlit as st

from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title('知识库更新服务')
# 文件上传
uploader_file = st.file_uploader(
    '请上传文件',
    type=['txt'],
    accept_multiple_files=False  # 代表仅接受一个文件上传
)
if "service" not in st.session_state:
    st.session_state.service = KnowledgeBaseService()

if uploader_file is not None:
    # 提取文件信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024  # KB

    st.subheader(f'文件名：{file_name}')
    st.write(f'文件类型：{file_type} | 文件大小：{file_size:.2f} KB')

    # 获取内容（修复后）
    text = uploader_file.read().decode('utf-8')
    with st.spinner('正在处理文件...'):
        result = st.session_state["service"].upload_by_str(text,file_name)
        st.write(result)