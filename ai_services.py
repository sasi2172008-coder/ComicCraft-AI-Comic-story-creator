
def generate_outline(story_prompt):
    return [
        {
            "title": "The Discovery",
            "scene_description": f"The main character begins the adventure: {story_prompt}",
            "caption": "Something unexpected is about to happen."
        },
        {
            "title": "The Mystery",
            "scene_description": "The character discovers something strange and mysterious.",
            "caption": "What could this mean?"
        },
        {
            "title": "The Adventure",
            "scene_description": "The character follows the mystery and faces a new challenge.",
            "caption": "The adventure begins."
        },
        {
            "title": "The Climax",
            "scene_description": "The character discovers the truth and must make an important decision.",
            "caption": "There is no turning back now."
        },
        {
            "title": "The Ending",
            "scene_description": "The character completes the adventure and learns something important.",
            "caption": "Every adventure leaves a story behind."
        }
    ]


def generate_story(outline):
    panels = []

    for panel in outline:
        panels.append({
            "title": panel["title"],
            "scene_description": panel["scene_description"],
            "caption": panel["caption"],
            "narration": "The story continues as the adventure unfolds.",
            "dialogue": "What will happen next?",
            "image_prompt": (
                "Cartoon comic panel showing "
                + panel["scene_description"]
            ),
            "image": "Comic illustration placeholder"
        })

    return panels


def generate_illustration(prompt):
    return {
        "status": "Illustration placeholder ready",
        "prompt": prompt
    }
