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
    "storyId": 3,
    "title": "Harry Pooter and the Sorcerer's Bone",
    "lore": "A magical parody adventure where Harry Pooter, a young wizard, discovers his destiny at Hogwash School of Witchcraft and Wizardry.",
    "characters": [
        {
            "id": 1,
            "name": "Harry Pooter",
            "subtitle": "The chosen one",
            "image": "https://static.wikia.nocookie.net/harrypotter/images/4/44/HarryPotter5.jpg",
            "description": "A young wizard with a lightning-shaped scar, destined for greatness.",
            "type": "protagonist",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 2,
            "name": "Hermione Stranger",
            "subtitle": "The clever friend",
            "image": "https://static.wikia.nocookie.net/harrypotter/images/6/6e/HermioneGranger_WB_F5_HermioneGrangerPromoShot_Still_01.jpg",
            "description": "Brilliant and resourceful, always ready with a spell or a fact.",
            "type": "npc",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 3,
            "name": "Ron Teasley",
            "subtitle": "The loyal companion",
            "image": "https://static.wikia.nocookie.net/harrypotter/images/5/5e/Ron_Weasley_poster.jpg",
            "description": "Harry's best friend, brave and always hungry.",
            "type": "npc",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 4,
            "name": "Lord Moldywart",
            "subtitle": "The dark wizard",
            "image": "https://static.wikia.nocookie.net/harrypotter/images/9/9d/Lordvoldemort.jpg",
            "description": "The most feared wizard of all time, seeking the Sorcerer's Bone.",
            "type": "npc",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    ],
    "chapters": [
        {
            "id": 1,
            "title": "The Letter Arrives",
            "image": "https://static.wikia.nocookie.net/harrypotter/images/7/7b/Harry-receives-his-letter.jpg",
            "description": "Harry receives a mysterious letter inviting him to Hogwash.",
            "milestones": make_milestones([
                "Receive the letter from the owl",
                "Convince the Dursleys to let you go",
                "Find Platform 9¾"
            ], start_id=1),
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 2,
            "title": "The Sorting Hat's Song",
            "image": "https://static.wikia.nocookie.net/harrypotter/images/2/2e/Sorting_Hat_HP1.png",
            "description": "Harry is sorted into his house and meets his new friends.",
            "milestones": make_milestones([
                "Meet Hermione and Ron",
                "Face the Sorting Hat",
                "Join the house feast"
            ], start_id=4),
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 3,
            "title": "The Sorcerer's Bone",
            "image": "https://static.wikia.nocookie.net/harrypotter/images/3/3f/Philosopher%27s_Stone_Film.png",
            "description": "Harry and friends discover the secret of the Sorcerer's Bone and face Lord Moldywart.",
            "milestones": make_milestones([
                "Sneak past Fluffy the three-headed dog",
                "Solve the potions riddle",
                "Defeat Lord Moldywart"
            ], start_id=7),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    ],
    "timestamp": datetime.now(timezone.utc).isoformat()
}

db.collection("game_stories").document(str(story_data["storyId"])).set(story_data)
print(f"Story '{story_data['title']}' populated in Firebase.")