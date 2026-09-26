from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

from ai_services import (
    generate_outline,
    generate_story,
    generate_illustration
)

from routes import router

app = FastAPI()

app.include_router(router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/generate")
def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    story_tone: str = Form(...),
    art_style: str = Form(...)
):

    outline = generate_outline(story_prompt)

    story = generate_story(outline)

    illustration = generate_illustration(
        f"{art_style} comic illustration of {character_name} "
        f"in {setting}"
    )

    panels = [
        {
            "title": "Introduction",
            "image": illustration,
            "scene_description": f"{character_name} is introduced in the {setting}.",
            "caption": "A new adventure begins.",
            "narration": story["narration"],
            "image_prompt": f"{art_style} comic illustration of {character_name} in {setting}"
        },
        {
            "title": "Problem",
            "image": illustration,
            "scene_description": f"{character_name} faces a problem in the {setting}.",
            "caption": "Something unexpected happens.",
            "narration": story["narration"],
            "image_prompt": f"{art_style} comic scene showing a problem in {setting}"
        },
        {
            "title": "Development",
            "image": illustration,
            "scene_description": f"{character_name} tries to solve the problem.",
            "caption": "The adventure continues.",
            "narration": story["narration"],
            "image_prompt": f"{art_style} comic scene of {character_name} solving a problem"
        },
        {
            "title": "Climax",
            "image": illustration,
            "scene_description": f"{character_name} reaches the most important moment of the story.",
            "caption": "The biggest challenge begins.",
            "narration": story["narration"],
            "image_prompt": f"{art_style} dramatic comic scene in {setting}"
        },
        {
            "title": "Ending",
            "image": illustration,
            "scene_description": f"{character_name} completes the adventure successfully.",
            "caption": "The story comes to an end.",
            "narration": story["narration"],
            "image_prompt": f"{art_style} comic ending scene in {setting}"
        }
    ]

    return templates.TemplateResponse(
        "comic_preview.html",
        {
            "request": request,
            "story_prompt": story_prompt,
            "character_name": character_name,
            "setting": setting,
            "story_tone": story_tone,
            "art_style": art_style,
            "outline": outline,
            "story": story,
            "illustration": illustration,
            "panels": panels
        }
    )
