import asyncio
import logging

from fastapi import HTTPException
from firebase_admin import credentials, firestore
import firebase_admin

logger = logging.getLogger("franjojo_backend")

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-service-account.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()


class FirestoreDbService:
    def __init__(self):
        self._cache = {}
        self._lock = asyncio.Lock()  # avoid race conditions
    
    async def get_game_story_by_story_id(self, story_id: str):
        # ✅ Return cached version if available
        if story_id in self._cache:
            logger.info(f"Cache hit for storyId {story_id}")
            return self._cache[story_id]

        async with self._lock:  # prevent multiple concurrent Firestore calls
            if story_id in self._cache:  # check again after lock
                return self._cache[story_id]

            logger.info(f"Fetching storyId {story_id} from Firestore")
            doc_ref = db.collection("game_stories").document(story_id)
            doc = await asyncio.to_thread(doc_ref.get)

            if not doc.exists:
                raise HTTPException(status_code=404, detail=f"Story '{story_id}' not found.")

            response = doc.to_dict()
            self._cache[story_id] = response  # ✅ cache it

            logger.info(f"Done fetching storyId {story_id}")
            return response

    async def update_game_story_by_story_id(self, story_id: str, data: dict):
        """Update a story in Firestore and invalidate cache"""
        logger.info(f"Updating storyId {story_id}")

        doc_ref = db.collection("game_stories").document(story_id)
        await asyncio.to_thread(doc_ref.update, data)

        # Invalidate cache
        if story_id in self._cache:
            del self._cache[story_id]
            logger.info(f"Cache invalidated for storyId {story_id}")

        logger.info(f"Done updating storyId {story_id}")
        return {"status": "success", "story_id": story_id}
