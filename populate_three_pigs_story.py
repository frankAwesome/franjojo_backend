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
    "lore": "A Minecraft-themed retelling of the classic tale, where three pigs build their homes and face the cunning wolf.",
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
            "title": "Pig 1 Builds a Straw House",
            "image": "https://i.ytimg.com/vi/bsiE5jTiaaA/maxresdefault.jpg",
            "description": "Percy Pig quickly builds his house out of straw. It goes up fast, but is it strong enough to keep him safe?",
            "milestones": make_milestones([
                "Gather straw from the field",
                "Build the house before sunset",
                "Test the house for strength"
            ], start_id=1),
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 2,
            "title": "Pig 2 Builds a Wood House",
            "image": "https://i.ytimg.com/vi/gJgLwcKGOto/sddefault.jpg",
            "description": "Penny Pig chooses wood for her home, hoping it will be sturdier than straw. She decorates it with flowers.",
            "milestones": make_milestones([
                "Collect wood from the forest",
                "Build a wooden house with windows",
                "Decorate the house with flowers"
            ], start_id=4),
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 3,
            "title": "Pig 3 Builds a Brick House",
            "image": "https://i.ytimg.com/vi/Q36THRWXRDY/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAWDwEwXNEG6udMXXxNkjBCi4DRZg",
            "description": "Peter Pig works hard to build a strong brick house. It takes longer, but he feels safe inside.",
            "milestones": make_milestones([
                "Find clay and make bricks",
                "Build a sturdy brick house",
                "Invite siblings to visit"
            ], start_id=7),
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 4,
            "title": "The Wolf Arrives",
            "image": "https://i.ytimg.com/vi/PfeQUEges2g/hq720.jpg",
            "description": "The cunning wolf comes to the village, eyeing the pigs’ houses. He starts with Percy’s straw house.",
            "milestones": make_milestones([
                "Scout the village for pigs",
                "Try to blow down the straw house",
                "Move to the next house if unsuccessful"
            ], start_id=10),
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 5,
            "title": "The Pigs Stand Together",
            "image": "https://i.ytimg.com/vi/LTfN32O5f1o/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAkiG_d4VlXV0E_CbTr7pC_UibrBw",
            "description": "After the wolf blows down the straw and wood houses, all three pigs hide in Peter’s brick house and outsmart the wolf.",
            "milestones": make_milestones([
                "Hide in the brick house",
                "Work together to defend the house",
                "Outsmart the wolf"
            ], start_id=13),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    ],
    "timestamp": datetime.now(timezone.utc).isoformat()
}

db.collection("game_stories").document(str(story_data["storyId"])).set(story_data)
print(f"Story '{story_data['storyId']}' populated in Firebase.")