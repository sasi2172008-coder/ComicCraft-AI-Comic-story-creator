from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from reportlab.pdfgen import canvas
from fastapi.responses import StreamingResponse
from io import BytesIO

from ai_services import (
    generate_outline,
    generate_story,
    generate_image
)

router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str


@router.get("/health")
def health_check():
    return {
        "status": "success",
        "message": "ComicCraft backend is running"
    }


@router.get("/about")
def about():
    return {
        "project": "ComicCraft",
        "description": "AI Comic Story Creator"
    }


@router.post("/generate-comic/json")
def generate_comic_json(request: PromptRequest):

    try:
        outline = generate_outline(request.prompt)

        panels = generate_story(outline)

        for index, panel in enumerate(panels, start=1):

            panel["image_url"] = generate_image(
                panel["image_prompt"],
                f"json_panel_{index}.png"
            )

        return {
            "status": "success",
            "message": "Comic generated successfully",
            "panels": panels,
            "panel_count": len(panels),
            "pdf_path": "ComicCraft.pdf"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Comic generation failed: {str(e)}"
        )


@router.get("/export-success")
def export_success():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ComicCraft - Export Success</title>
    </head>

    <body>
        <h1>Comic Export Successful!</h1>

        <p>Your ComicCraft comic has been successfully exported.</p>

        <p>Your comic PDF is ready.</p>

        <a href="/">
            <button>Go Create Another Comic</button>
        </a>
    </body>
    </html>
    """


@router.get("/test-image")
def test_image(prompt: str = "A cartoon character"):

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


@router.get("/download-pdf")
def download_pdf(
    story_prompt: str,
    character_name: str,
    setting: str,
    story_tone: str,
    art_style: str
):

    try:

        buffer = BytesIO()

        pdf = canvas.Canvas(buffer)

        pdf.setTitle("ComicCraft Comic")

        pdf.drawString(
            50, 800,
            "ComicCraft - AI Comic"
        )

        pdf.drawString(
            50, 770,
            f"Story: {story_prompt}"
        )

        pdf.drawString(
            50, 740,
            f"Character: {character_name}"
        )

        pdf.drawString(
            50, 710,
            f"Setting: {setting}"
        )

        pdf.drawString(
            50, 680,
            f"Story Tone: {story_tone}"
        )

        pdf.drawString(
            50, 650,
            f"Art Style: {art_style}"
        )

        pdf.drawString(
            50, 600,
            "Comic generated successfully!"
        )

        pdf.save()

        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                "attachment; filename=ComicCraft.pdf"
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {str(e)}"
        )
