import json
import os
from typing import List

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict

import config_data as config


class FileHistoryStore(BaseChatMessageHistory):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history_dir = config.history_dir
        self.file_path = os.path.join(self.history_dir, f"{session_id}.json")
        self._messages: List[BaseMessage] = self._load_messages()

    @property
    def messages(self) -> List[BaseMessage]:
        return self._messages

    def add_message(self, message: BaseMessage) -> None:
        self._messages.append(message)
        self._save_messages()

    def clear(self) -> None:
        self._messages = []
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def _load_messages(self) -> List[BaseMessage]:
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return messages_from_dict(data)
        return []

    def _save_messages(self) -> None:
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([message_to_dict(msg) for msg in self._messages], f, ensure_ascii=False, indent=2)


def get_session_history(session_id: str) -> FileHistoryStore:
    return FileHistoryStore(session_id)