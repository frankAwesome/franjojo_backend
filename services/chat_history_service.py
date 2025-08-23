class ChatHistoryService:
    chat_histories = {}

    def get_chat_history(self, key: str):
        return self.chat_histories[key] if key in self.chat_histories.keys() else []

    def save_chat(self, key: str, player_chat: str, npc_chat: str, npc_name: str):
        
        if key not in self.chat_histories.keys():
            self.chat_histories[key] = []
        
        self.chat_histories[key].append('Player: ' + player_chat)
        self.chat_histories[key].append(npc_name + ': ' + npc_chat)