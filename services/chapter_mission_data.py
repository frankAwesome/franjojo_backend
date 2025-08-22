# Example mission and chapter data for demo purposes
CHAPTERS = {
    "story1": {
        1: {
            "description": "The adventure begins in the town square.",
            "missions": [
                {"id": "find_sword", "description": "Find the lost sword in the forest.", "completed": False},
                {"id": "talk_to_mayor", "description": "Speak to the mayor about your quest.", "completed": False}
            ]
        },
        2: {
            "description": "The journey continues to the mountain pass.",
            "missions": [
                {"id": "defeat_bandits", "description": "Defeat the bandits blocking the pass.", "completed": False}
            ]
        }
    }
}

def get_chapter_data(story_id, chapter):
    return CHAPTERS.get(story_id, {}).get(chapter, {"description": "", "missions": []})

def are_all_missions_complete(story_id, chapter):
    chapter_data = get_chapter_data(story_id, chapter)
    return all(m["completed"] for m in chapter_data["missions"])

def get_mission_status(story_id, chapter, mission_id):
    chapter_data = get_chapter_data(story_id, chapter)
    for m in chapter_data["missions"]:
        if m["id"] == mission_id:
            return m["completed"]
    return False

def set_mission_complete(story_id, chapter, mission_id):
    chapter_data = get_chapter_data(story_id, chapter)
    for m in chapter_data["missions"]:
        if m["id"] == mission_id:
            m["completed"] = True
            return True
    return False
