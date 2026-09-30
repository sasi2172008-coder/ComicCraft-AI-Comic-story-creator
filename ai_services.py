import os
import requests
from urllib.parse import quote


# -------------------------------------------------
# 1. CREATE 5-PANEL COMIC OUTLINE
# -------------------------------------------------

def generate_outline(story_prompt):
    prompt = story_prompt.strip()

    if not prompt:
        prompt = "A young character goes on an exciting adventure."

    return [
        {
            "title": "The Beginning",
            "scene_description": (
                f"The main character begins the adventure based on this idea: {prompt}. "
                "Show the character in the starting situation."
            ),
            "caption": "The adventure begins."
        },
        {
            "title": "The Discovery",
            "scene_description": (
                f"The character discovers something unexpected connected to: {prompt}. "
                "Show surprise and curiosity."
            ),
            "caption": "Something unexpected appears."
        },
        {
            "title": "The Challenge",
            "scene_description": (
                f"The character faces an exciting challenge related to: {prompt}. "
                "Show action, emotion and a clear problem."
            ),
            "caption": "A difficult challenge stands in the way."
        },
        {
            "title": "The Climax",
            "scene_description": (
                f"The character finds a solution and faces the most important moment "
                f"of the adventure based on: {prompt}."
            ),
            "caption": "This is the most important moment."
        },
        {
            "title": "The Ending",
            "scene_description": (
                f"The adventure based on '{prompt}' reaches a happy and meaningful ending. "
                "Show the character after solving the main problem."
            ),
            "caption": "Every adventure leaves a lesson."
        }
    ]


# -------------------------------------------------
# 2. CREATE STORY CONTENT FOR EACH PANEL
# -------------------------------------------------

def generate_story(outline):
    panels = []

    for number, panel in enumerate(outline, start=1):

        narration = (
            f"In panel {number}, {panel['scene_description']}"
        )

        dialogue = (
            "I must keep going and find out what happens next!"
        )

        image_prompt = (
            "Create a high-quality colorful cartoon comic panel. "
            "Keep the same main character throughout the comic. "
            "Show clear facial expressions, cinematic composition, "
            "detailed background, bright colors and family-friendly style. "
            f"Scene: {panel['scene_description']}. "
            "Do not add written text, captions, speech bubbles or watermarks."
        )

        panels.append({
            "panel_number": number,
            "title": panel["title"],
            "scene_description": panel["scene_description"],
            "caption": panel["caption"],
            "narration": narration,
            "dialogue": dialogue,
            "image_prompt": image_prompt
        })

    return panels


# -------------------------------------------------
# 3. GENERATE IMAGE USING POLLINATIONS
# -------------------------------------------------

def generate_image(prompt, filename):

    api_key = os.getenv("POLLINATIONS_API_KEY")

    if not api_key:
        raise RuntimeError(
            "POLLINATIONS_API_KEY is missing. "
            "Please check your .env file."
        )

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

    file_path = os.path.join(
        "static",
        "images",
        filename
    )

    with open(file_path, "wb") as file:
        file.write(response.content)

    return f"/static/images/{filename}"


# -------------------------------------------------
# 4. BUILD COMIC LAYOUT
# -------------------------------------------------

def build_comic_layout(panels):

    return {
        "title": "ComicCraft - AI Comic Story",
        "panel_count": len(panels),
        "panels": panels
    }


# -------------------------------------------------
# 5. PREPARE PDF DATA
# -------------------------------------------------

def save_pdf_data(panels):

    return {
        "title": "ComicCraft - AI Comic",
        "panels": panels,
        "panel_count": len(panels)
    }
