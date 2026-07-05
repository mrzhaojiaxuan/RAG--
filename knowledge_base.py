"""
知识库
"""
import datetime
import os


from langchain_text_splitters import RecursiveCharacterTextSplitter

import config_data as config
import hashlib
from langchain_chroma  import Chroma
from langchain_openai import OpenAIEmbeddings

def check_md5(md5_str:str):
    """
    检查传入的md5是否已经被处理过了
    return False 未处理过
    return True 处理过
    """
    if not os.path.exists(config.md5_path):
        #if进入表示文件不存在 不存在就没处理过
        open(config.md5_path,'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8').readlines():
            line = line.strip() #处理空格和回车
            if line == md5_str:
                return True
        return False



def save_md5(md5_str:str):
    """将传入的md5文件记录到文件内保存"""
    with open(config.md5_path,'a',encoding='utf-8') as f:
        f.write(md5_str+'\n')

def get_str_md5(input_str:str,encoding='utf-8'):
    """将传入的字符串转为md5字符串"""
    #将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)
    #创建md5对象
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes) #更新内容传入要转换的字节数组
    md5_hex = md5_obj.hexdigest() #转16进制
    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self):
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=config.OPENAI_API_KEY,
                base_url=config.OPENAI_API_BASE
            ),
            persist_directory=config.persist_directory,
        )  #向量存储的实例Chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, #分割后的本段最大长度
            chunk_overlap=config.chunk_overlap, #连续文本段之间的字符重叠数量
            separators=config.separators,#自然段落划分的符号
            length_function=len,#使用Python自带的len函数做长度统计的依据
        ) #文本分割器的对象

    def upload_by_str(self,data,filename):
        """将传入的字符串进行向量化存入向量数据库中"""
        md5_hex = get_str_md5(data)

        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"

        if len(data)>config.max_split_char_number:
            knowledge_chunks:list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadatas = {
            "source": filename,
            "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"小曹"
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas = [metadatas for _ in knowledge_chunks],
        )

        save_md5(md5_hex)
        return "[成功]内容已经存入知识库中"
if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_str("林俊杰","testfile")
    print(r)