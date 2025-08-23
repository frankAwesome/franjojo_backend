import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

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
    "storyId": 2,
    "title": "Monkey: Making of a King",
    "lore": "A young, talented thief named Monkey embarks on a journey of self-discovery, learning and fulfilling his destiny one piece at a time.",
    "characters": [
        {
            "id": 1,
            "name": "Monkey",
            "subtitle": "The talented thief",
            "image": "https://firebasestorage.googleapis.com/v0/b/storysocial-23aa1.appspot.com/o/1.png?alt=media&token=3017e363-34e8-499e-a4a8-c155de28db0b",
            "description": "A clever and agile thief with a mysterious past, destined for greatness.",
            "type": "protagonist",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 2,
            "name": "Pig",
            "subtitle": "The loyal companion",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGKGOMUKX8Wnut_NbM86Prwf49sDhaoaxrA5y9yTwnqk1y8tXE_fMHJ-ATi160EYrcbDU&usqp=CAU",
            "description": "Monkey's steadfast friend, always ready with a joke or a helping hand.",
            "type": "npc",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 3,
            "name": "Dr. Mad Monkey",
            "subtitle": "The enigmatic mentor",
            "image": "https://townsquare.media/site/442/files/2024/08/attachment-the-monkey-stephen-king-movie.jpg?w=780&q=75",
            "description": "A brilliant but eccentric scientist who guides Monkey on his journey.",
            "type": "npc",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    ],
    "chapters": [
        {
            "id": 1,
            "title": "The Heist Begins",
            "image": "https://www.gamerevolution.com/wp-content/uploads/sites/2/2018/05/bge2.jpg?w=640",
            "description": "Monkey plans and executes a daring heist, setting off a chain of events that will change his life forever.",
            "milestones": make_milestones([
                "Scout the city for opportunities",
                "Assemble the crew",
                "Steal the artifact from the museum"
            ], start_id=1),
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 2,
            "title": "Allies and Enemies",
            "image": "https://assets.vg247.com/current//2017/06/beyond_good_and_evil_2_e3_2017-15.jpg",
            "description": "Monkey meets new friends and faces powerful foes as he learns more about his true purpose.",
            "milestones": make_milestones([
                "Meet Dr. Mad Monkey",
                "Escape from the city guards",
                "Uncover the secret map"
            ], start_id=4),
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 3,
            "title": "Crowning Destiny",
            "image": "https://global-img.gamergen.com/beyond-good-and-evil-2-17-05-06-2019_0900925570.jpg",
            "description": "In a final showdown, Monkey must prove himself worthy and claim his place as king.",
            "milestones": make_milestones([
                "Confront the rival gang",
                "Solve the king's riddle",
                "Take the throne"
            ], start_id=7),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    ],
    "timestamp": datetime.now(timezone.utc).isoformat()
}

db.collection("game_stories").document(str(story_data["storyId"])).set(story_data)
print(f"Story '{story_data['storyId']}' populated in Firebase.")
