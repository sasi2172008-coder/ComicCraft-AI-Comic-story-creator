from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from ai_services import (
    generate_outline,
    generate_story,
    generate_image
)

from routes import router

app = FastAPI()

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
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

    panels = generate_story(outline)

    for index, panel in enumerate(panels, start=1):

        panel["image_prompt"] = (
            f"{art_style} comic illustration of "
            f"{character_name} in {setting}. "
            f"{panel['scene_description']}"
        )

        panel["image_url"] = generate_image(
            panel["image_prompt"],
            f"panel_{index}.png"
        )

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "story_prompt": story_prompt,
            "character_name": character_name,
            "setting": setting,
            "story_tone": story_tone,
            "art_style": art_style,
            "panels": panels
        }
         )
