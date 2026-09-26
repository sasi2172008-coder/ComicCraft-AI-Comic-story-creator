
import os
import requests
from urllib.parse import quote


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
            )
        })

    return panels


def generate_image(prompt, filename):
    api_key = os.getenv("POLLINATIONS_API_KEY")

    if not api_key:
        raise RuntimeError("POLLINATIONS_API_KEY is missing")

    model = "sana"

    image_url = (
        "https://gen.pollinations.ai/image/"
        + quote(prompt)
        + "?model="
        + quote(model)
    )

    response = requests.get(
        image_url,
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        timeout=120
    )

    response.raise_for_status()

    os.makedirs("static/images", exist_ok=True)

    file_path = os.path.join("static", "images", filename)

    with open(file_path, "wb") as file:
        file.write(response.content)

    return f"/static/images/{filename}"
