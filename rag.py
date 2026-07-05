from itertools import chain

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from vector_stores import VectorStoreService
from file_history_store import get_session_history
from langchain_core.documents import Document


def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

import config_data as config

class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=config.OPENAI_API_KEY,
                base_url=config.OPENAI_API_BASE
            )
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的已知参考资料为主,"
                 "简洁和专业的回答用户问题.参考资料:{context}."),
                ("system","并且我提供用户的对话历史记录,如下:"),
                MessagesPlaceholder(variable_name="history"),
                ("user","请回答用户提问:{input}")

            ]
        )
        self.chat_model = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_API_BASE
        )
        self.chain = self.__get_chain()
    def __get_chain(self):
        """
        获取问答链
        :return:
        """
        retriever = self.vector_service.get_retriever()
        def format_document(docs:list[Document]):
            if not docs:
                return "无相关参考资料"
            formatted_str = ""
            for doc in docs:
                formatted_str +=f"文档片段:{doc.page_content}\n文档元数据:{doc.metadata}\n\n"
            return formatted_str
        chain = (
            {
                "input": lambda x: x["input"],
                "context": lambda x: format_document(retriever.invoke(x["input"])),
                "history": lambda x: x["history"]
            } | self.prompt_template |print_prompt | self.chat_model |StrOutputParser()
        )
        chain_with_history = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        return chain_with_history

if __name__ == '__main__':
    # 方式1：invoke 调用（推荐）
    res = RagService().chain.invoke(
        {"input": "我的体重200斤,购买女装,为我尺码推荐"},
        config={"configurable": {"session_id": "user_001"}}
    )
    print(res)