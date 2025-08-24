import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

# Helper to generate milestone dicts with ids
def make_milestones(names, start_id=1):
    return [
        {"id": start_id + i, "name": name, "completed": False, "timestamp": datetime.now(timezone.utc).isoformat()}
        for i, name in enumerate(names)
    ]

cred = credentials.Certificate("firebase-service-account.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()
story_data = {
    "storyId": 1,
    "title": "The Three Pigs and the Wolf",
    "lore": "Once upon a time, in a bright, blocky meadow, three little pigs built their homes—Percy’s of straw, Penny’s of wood, and Peter’s of brick. They were just settling in when the forest fell quiet: eyes in the shadows, soft steps on the path. The Big Bad Wolf was coming to huff and puff at every door. Gather close—your adventure starts now.",
    "characters": [
        {
            "id": 1,
            "name": "Percy Pig",
            "subtitle": "The quick builder (straw house)",
            "image": "https://laby.net/api/v3/render/skin/8bb5b7f8f6314f128a68419ce4a8040c.png",
            "description": "Percy Pig quickly builds his house out of straw. It goes up fast, but is it strong enough to keep him safe?",
            "type": "protagonist",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 2,
            "name": "Penny Pig",
            "subtitle": "The creative builder (wood house)",
            "image": "https://s.namemc.com/3d/skin/body.png?id=292a520f3c0d60a1&model=classic&width=308&height=308",
            "description": "Penny Pig chooses wood for her home, hoping it will be sturdier than straw. She decorates it with flowers.",
            "type": "npc",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 3,
            "name": "Peter Pig",
            "subtitle": "The careful builder (brick house)",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3JTmZNVMCDXEfuS7JE1IHJxrD6_0WpNvvQw1XL1ZWeowRWgJxQmFq6SyGuAwPgMNyAio&usqp=CAU",
            "description": "Peter Pig works hard to build a strong brick house. It takes longer, but he feels safe inside.",
            "type": "npc",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 4,
            "name": "Wolf",
            "subtitle": "The cunning antagonist",
            "image": "https://s.namemc.com/3d/skin/body.png?id=814cafedc6a44064&model=classic&width=308&height=308",
            "description": "The cunning wolf comes to the village, eyeing the pigs’ houses. He starts with Percy’s straw house.",
            "type": "npc",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    ],
    "chapters": [
        {
            "id": 1,
            "title": "Percy Pig Build a Straw House",
            "image": "https://i.ytimg.com/vi/bsiE5jTiaaA/maxresdefault.jpg",
            "description": "Percy Pig quickly build his house out of straw. It goes up fast, but is it strong enough to keep him safe?",
            "milestones": make_milestones([
                "Greet Percy Pig",
                "Threaten to Blow up the straw house, see if there is weaknesses",
                "Find ways to Blow up the straw house"
            ], start_id=1),
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 2,
            "title": "Penny Pig Builds a Wood House",
            "image": "https://i.ytimg.com/vi/gJgLwcKGOto/sddefault.jpg",
            "description": "Penny Pig chooses wood for her home, hoping it will be sturdier than straw. She decorates it with flowers.",
            "milestones": make_milestones([
                "Threaten to Blow up the Wood House, see if there is weaknesses",
                "Find ways to Blow up the Wood House"
            ], start_id=4),
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 3,
            "title": "Peter Pig Builds a Brick House",
            "image": "https://i.ytimg.com/vi/Q36THRWXRDY/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAWDwEwXNEG6udMXXxNkjBCi4DRZg",
            "description": "Peter Pig works hard to build a strong brick house. It takes longer, but he feels safe inside.",
            "milestones": make_milestones([
                "Threaten to Blow up the Brick House, see if there is weaknesses",
                "Find ways to Blow up the Brick House"
            ], start_id=7),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    ],
    "timestamp": datetime.now(timezone.utc).isoformat()
}

db.collection("game_stories").document(str(story_data["storyId"])).set(story_data)
print(f"Story '{story_data['storyId']}' populated in Firebase.")