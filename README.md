# RAG-某东商品

基于 RAG（Retrieval-Augmented Generation）技术的京东商品问答助手，支持尺码推荐、洗涤养护、颜色选择等知识库问答。

## 功能特性

- ✅ **RAG 检索增强生成**：基于 Chroma 向量数据库进行知识检索
- ✅ **流式输出**：支持打字机效果的流式问答响应
- ✅ **对话历史持久化**：自动保存用户对话历史到 JSON 文件
- ✅ **Streamlit 聊天界面**：简洁友好的 Web 聊天页面
- ✅ **知识库管理**：支持文本内容向量化入库

## 文件结构

```
├── app_qa.py              # Streamlit 聊天页面入口
├── app_file_uploader.py   # 文件上传入库脚本
├── rag.py                 # RAG 问答服务核心逻辑
├── vector_stores.py       # 向量存储服务
├── knowledge_base.py      # 知识库管理服务
├── file_history_store.py  # 对话历史文件存储
├── config_data.py         # 配置文件
├── .env.example           # 环境变量模板
├── .gitignore             # Git 忽略配置
├── chroma_data/           # Chroma 向量数据库数据
├── chat_history/          # 对话历史存储目录
└── *.txt                  # 知识库源文件（尺码推荐、洗涤养护、颜色选择）
```

## 环境要求

- Python 3.10+
- Anaconda 或虚拟环境

## 安装步骤

```bash
# 克隆项目
git clone <repository-url>
cd RAG-某东商品

# 创建虚拟环境（可选但推荐）
conda create -n rag python=3.10
conda activate rag

# 安装依赖
pip install langchain langchain-openai langchain-chroma chromadb streamlit python-dotenv
```

## 配置说明

1. 复制 `.env.example` 为 `.env`：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入您的 OpenAI API Key：
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai-proxy.org/v1
```

## 启动方式

### 1. 知识库入库（首次使用）

```bash
python knowledge_base.py
```

或使用文件上传脚本：

```bash
python app_file_uploader.py
```

### 2. 启动 Streamlit 聊天页面

```bash
streamlit run app_qa.py --server.port 8501
```

访问 http://localhost:8501 即可使用聊天功能。

### 3. 命令行测试

```bash
python rag.py
```

## 使用说明

1. 在聊天输入框中输入您的问题
2. 系统会自动检索知识库并给出答案
3. 对话历史会自动保存，刷新页面后仍然保留
4. 可在侧边栏切换会话 ID 或清空对话

## 技术栈

- **框架**: Streamlit
- **LLM**: OpenAI GPT-3.5-turbo
- **向量数据库**: Chroma
- **RAG**: LangChain
- **嵌入模型**: text-embedding-3-small

## 注意事项

- 首次启动需要联网下载模型，可能需要几分钟
- API Key 请妥善保管，不要提交到版本控制
- 建议使用代理地址以提高国内访问速度