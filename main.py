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
            "illustration": illustration
        }
    )
