import logging
logger = logging.getLogger("franjojo_backend")

class ChatHistoryService:
    chat_histories = {}

    def get_chat_history(self, key: str):
        logger.info("Gettin chat history")
        chat_history = self.chat_histories[key] if key in self.chat_histories.keys() else []
        logger.info("Done gettin chat history")
        return chat_history

    def save_chat(self, key: str, player_chat: str, npc_chat: str, npc_name: str):
        logger.info("Saving chat history")
        
        if key not in self.chat_histories.keys():
            self.chat_histories[key] = []
        
        self.chat_histories[key].append('Player: ' + player_chat)
        self.chat_histories[key].append(npc_name + ': ' + npc_chat)
        logger.info("Done saving chat history")