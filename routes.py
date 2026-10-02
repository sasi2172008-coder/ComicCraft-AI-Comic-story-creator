from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

from io import BytesIO
import os

from ai_services import (
    generate_outline,
    generate_story,
    generate_image,
    build_comic_layout
)


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# -------------------------------------------------
# JSON REQUEST MODEL
# -------------------------------------------------

class PromptRequest(BaseModel):
    prompt: str


# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# -------------------------------------------------
# HEALTH
# -------------------------------------------------

@router.get("/health")
def health_check():
    return {
        "status": "success",
        "message": "ComicCraft backend is running"
    }


# -------------------------------------------------
# ABOUT
# -------------------------------------------------

@router.get("/about")
def about():
    return {
        "project": "ComicCraft",
        "description": "AI Comic Story Creator"
    }


# -------------------------------------------------
# SAVE PDF
# -------------------------------------------------

def save_pdf(panels):

    os.makedirs("static/comics", exist_ok=True)

    pdf_path = os.path.join(
        "static",
        "comics",
        "ComicCraft.pdf"
    )

    pdf = canvas.Canvas(
        pdf_path,
        pagesize=A4
    )

    page_width, page_height = A4

    pdf.setTitle("ComicCraft - AI Comic")

    for index, panel in enumerate(panels, start=1):

        if index > 1:
            pdf.showPage()

        # Title
        pdf.setFont("Helvetica-Bold", 18)

        pdf.drawString(
            40,
            page_height - 50,
            f"Panel {index}: {panel.get('title', '')}"
        )

        # Narration
        pdf.setFont("Helvetica", 11)

        text = panel.get(
            "narration",
            panel.get("scene_description", "")
        )

        text_object = pdf.beginText(
            40,
            page_height - 80
        )

        text_object.setLeading(15)

        # Split long text into lines
        words = text.split()
        line = ""

        for word in words:

            if len(line) + len(word) > 90:

                text_object.textLine(line)
                line = word + " "

            else:
                line += word + " "

        if line:
            text_object.textLine(line)

        pdf.drawText(text_object)

        # Image
        image_url = panel.get("image_url", "")

        if image_url:

            image_path = image_url.lstrip("/")

            if os.path.exists(image_path):

                try:

                    image = ImageReader(image_path)

                    pdf.drawImage(
                        image,
                        50,
                        150,
                        width=490,
                        height=300,
                        preserveAspectRatio=True,
                        anchor="c",
                        mask="auto"
                    )

                except Exception:
                    pass

        # Caption
        pdf.setFont(
            "Helvetica-Oblique",
            10
        )

        pdf.drawString(
            40,
            100,
            panel.get("caption", "")
        )

    pdf.save()

    return pdf_path


# -------------------------------------------------
# GENERATE COMIC FROM FORM
# -------------------------------------------------

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    story_tone: str = Form(...),
    art_style: str = Form(...)
):

    try:

        # Combine all user inputs
        complete_prompt = f"""
Story idea: {story_prompt}

Main character: {character_name}

Setting: {setting}

Story tone: {story_tone}

Art style: {art_style}
"""

        # Create 5-panel outline
        outline = generate_outline(
            complete_prompt
        )

        # Generate story
        panels = generate_story(
            outline
        )

        # Generate images
        for index, panel in enumerate(
            panels,
            start=1
        ):

            filename = (
                f"comic_panel_{index}.png"
            )

            image_url = generate_image(
                panel["image_prompt"],
                filename
            )

            panel["image_url"] = image_url

        # Build layout
        comic = build_comic_layout(
            panels
        )

        # Save PDF
        pdf_path = save_pdf(
            panels
        )

        # Send data to preview page
        return templates.TemplateResponse(
            "comic_preview.html",
            {
                "request": request,
                "story_prompt": story_prompt,
                "character_name": character_name,
                "setting": setting,
                "story_tone": story_tone,
                "art_style": art_style,
                "panels": panels,
                "comic": comic,
                "pdf_path": pdf_path
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Comic generation failed: {str(e)}"
        )


# -------------------------------------------------
# GENERATE COMIC - JSON API
# -------------------------------------------------

@router.post("/generate-comic/json")
def generate_comic_json(
    request: PromptRequest
):

    try:

        # Create outline
        outline = generate_outline(
            request.prompt
        )

        # Create story
        panels = generate_story(
            outline
        )

        # Generate image for each panel
        for index, panel in enumerate(
            panels,
            start=1
        ):

            filename = (
                f"comic_panel_{index}.png"
            )

            image_url = generate_image(
                panel["image_prompt"],
                filename
            )

            panel["image_url"] = image_url

        # Build layout
        comic = build_comic_layout(
            panels
        )

        # Save PDF
        pdf_path = save_pdf(
            panels
        )

        return {
            "status": "success",
            "message": "Comic generated successfully",
            "story_prompt": request.prompt,
            "panel_count": len(panels),
            "panels": panels,
            "comic": comic,
            "pdf_path": pdf_path
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Comic generation failed: {str(e)}"
        )


# -------------------------------------------------
# TEST IMAGE
# -------------------------------------------------

@router.get("/test-image")
def test_image(
    prompt: str = (
        "A colorful cartoon character "
        "standing in a beautiful forest"
    )
):

    try:

        image_url = generate_image(
            prompt,
            "test_image.png"
        )

        return {
            "status": "success",
            "message": "Image generation test completed",
            "image_url": image_url
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}"
        )


# -------------------------------------------------
# DOWNLOAD PDF
# -------------------------------------------------

@router.get("/download-pdf")
def download_pdf():

    pdf_path = os.path.join(
        "static",
        "comics",
        "ComicCraft.pdf"
    )

    if not os.path.exists(pdf_path):

        raise HTTPException(
            status_code=404,
            detail="PDF not found. Generate a comic first."
        )

    with open(pdf_path, "rb") as file:

        content = file.read()

    return StreamingResponse(
        BytesIO(content),
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=ComicCraft.pdf"
        }
    )


# -------------------------------------------------
# EXPORT SUCCESS
# -------------------------------------------------

@router.get(
    "/export-success",
    response_class=HTMLResponse
)
def export_success(
    request: Request
):

    return templates.TemplateResponse(
        "export_success.html",
        {
            "request": request
        }
)
