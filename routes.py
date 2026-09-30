from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
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


class PromptRequest(BaseModel):
    prompt: str


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
# GENERATE COMIC
# -------------------------------------------------

@router.post("/generate-comic/json")
def generate_comic_json(request: PromptRequest):

    try:

        # Create 5-panel outline
        outline = generate_outline(request.prompt)

        # Create story for each panel
        panels = generate_story(outline)

        # Generate image for every panel
        for index, panel in enumerate(panels, start=1):

            filename = f"comic_panel_{index}.png"

            image_url = generate_image(
                panel["image_prompt"],
                filename
            )

            panel["image_url"] = image_url

        # Build comic layout
        comic = build_comic_layout(panels)

        return {
            "status": "success",
            "message": "Comic generated successfully",
            "story_prompt": request.prompt,
            "panel_count": len(panels),
            "panels": panels,
            "comic": comic
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Comic generation failed: {str(e)}"
        )


# -------------------------------------------------
# TEST IMAGE GENERATION
# -------------------------------------------------

@router.get("/test-image")
def test_image(
    prompt: str = "A colorful cartoon character standing in a beautiful forest"
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
# EXPORT SUCCESS PAGE
# -------------------------------------------------

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


# -------------------------------------------------
# DOWNLOAD PDF
# -------------------------------------------------

@router.get("/download-pdf")
def download_pdf():

    try:

        buffer = BytesIO()

        pdf = canvas.Canvas(
            buffer,
            pagesize=A4
        )

        page_width, page_height = A4

        pdf.setTitle("ComicCraft - AI Comic")

        # Title
        pdf.setFont("Helvetica-Bold", 20)

        pdf.drawString(
            50,
            page_height - 50,
            "ComicCraft - AI Comic"
        )

        y = page_height - 90

        # Find generated panel images
        image_folder = "static/images"

        panel_files = []

        for index in range(1, 6):

            filename = f"comic_panel_{index}.png"

            path = os.path.join(
                image_folder,
                filename
            )

            if os.path.exists(path):
                panel_files.append(path)

        # Add each panel
        for index, image_path in enumerate(panel_files, start=1):

            # New page if necessary
            if y < 250:

                pdf.showPage()

                pdf.setFont(
                    "Helvetica-Bold",
                    18
                )

                pdf.drawString(
                    50,
                    page_height - 50,
                    "ComicCraft - AI Comic"
                )

                y = page_height - 90

            pdf.setFont(
                "Helvetica-Bold",
                14
            )

            pdf.drawString(
                50,
                y,
                f"Panel {index}"
            )

            y -= 20

            # Add image
            try:

                image = ImageReader(image_path)

                image_width = 480
                image_height = 270

                pdf.drawImage(
                    image,
                    50,
                    y - image_height,
                    width=image_width,
                    height=image_height,
                    preserveAspectRatio=True,
                    mask="auto"
                )

                y -= image_height + 30

            except Exception:
                pass

        # Finish PDF
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
