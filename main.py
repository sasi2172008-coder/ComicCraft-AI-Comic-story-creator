from fastapi import FastAPI, Request, Form
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

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


def create_panels(
    character_name,
    setting,
    art_style,
    story
):

    illustration = generate_illustration(
        f"{art_style} comic illustration of {character_name} in {setting}"
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

    return panels


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

    panels = create_panels(
        character_name,
        setting,
        art_style,
        story
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
            "panels": panels
        }
    )


@app.get("/download-pdf")
def download_pdf(
    story_prompt: str,
    character_name: str,
    setting: str,
    story_tone: str,
    art_style: str
):

    outline = generate_outline(story_prompt)

    story = generate_story(outline)

    panels = create_panels(
        character_name,
        setting,
        art_style,
        story
    )

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "ComicCraft - AI Comic Story",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            f"<b>Story:</b> {story_prompt}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Character:</b> {character_name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Setting:</b> {setting}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Story Tone:</b> {story_tone}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Art Style:</b> {art_style}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    for index, panel in enumerate(panels, start=1):

        content.append(
            Paragraph(
                f"Panel {index} - {panel['title']}",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                f"<i>{panel['scene_description']}</i>",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Caption:</b> {panel['caption']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Narration:</b> {panel['narration']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Image Prompt:</b> {panel['image_prompt']}",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 15))

        if index < len(panels):
            content.append(PageBreak())

    document.build(content)

    pdf_buffer.seek(0)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=ComicCraft_Comic.pdf"
        }
    )
        
