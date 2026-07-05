import os

md5_path = './md5.txt'

collection_name = 'rag'
persist_directory = './chroma_data'

chunk_size = 400
chunk_overlap = 60
separators = ['\n\n','\n','.','!','?',',','。','！','？','，'," "]
max_split_char_number = 5000

top_k = 2
similarity_threshold = 1
score_threshold = 0.58

history_dir = './chat_history'

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai-proxy.org/v1")