import os
import requests
from urllib.parse import quote


def generate_outline(story_prompt):
    return [
        {
            "title": "The Discovery",
            "scene_description": f"The adventure begins with {story_prompt}"
        },
        {
            "title": "The Mystery",
            "scene_description": "A mysterious situation appears."
        },
        {
            "title": "The Adventure",
            "scene_description": "The main character starts an exciting adventure."
        },
        {
            "title": "The Climax",
            "scene_description": "The main challenge is faced."
        },
        {
            "title": "The Ending",
            "scene_description": "The adventure reaches a happy ending."
        }
    ]


def generate_story(outline):
    panels = []

    for item in outline:
        panels.append({
            "title": item["title"],
            "scene_description": item["scene_description"],
            "dialogue": "Let's continue the adventure!"
        })

    return panels


def generate_image(prompt, filename):
    api_key = os.getenv("POLLINATIONS_API_KEY")

    url = (
        "https://gen.pollinations.ai/image/"
        + quote(prompt)
    )

    headers = {}

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=60
        )

        if response.status_code == 200:
            folder = "static/images"
            os.makedirs(folder, exist_ok=True)

            filepath = os.path.join(folder, filename)

            with open(filepath, "wb") as file:
                file.write(response.content)

            return f"/static/images/{filename}"

    except Exception as e:
        print("Image generation error:", e)

    return ""


def build_comic_layout(panels):
    return panels


def save_pdf_data(panels):
    return panels
