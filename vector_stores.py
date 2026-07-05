

from langchain_chroma import Chroma
import config_data as config

class VectorStoreService(object):
    def __init__(self,embedding):
        """

        :param embedding: 嵌入模型的接入
        """
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.top_k})

if __name__ == '__main__':
    from langchain_openai import OpenAIEmbeddings
    retriever = VectorStoreService(OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=config.OPENAI_API_KEY,
                base_url=config.OPENAI_API_BASE
            )).get_retriever()

    res=  retriever.invoke("我的体重180斤,购买男装上衣,为我尺码推荐,只返回最适合的尺码")
    print(res)