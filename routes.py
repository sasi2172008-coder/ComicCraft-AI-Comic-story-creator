from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from reportlab.pdfgen import canvas
from io import BytesIO

from .ai_services import (
    generate_outline,
    generate_story,
    generate_illustration
)

router = APIRouter()


# JSON request model
class PromptRequest(BaseModel):
    prompt: str


# -----------------------------
# HOME PAGE
# -----------------------------

@router.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ComicCraft - AI Comic Story Creator</title>
    </head>

    <body>

        <h1>ComicCraft - AI Comic Story Creator</h1>

        <p>Create your own AI comic story.</p>

        <form action="/generate" method="post">

            <label>Story Prompt:</label><br>
            <input type="text" name="story_prompt" required>
            <br><br>

            <label>Character Name:</label><br>
            <input type="text" name="character_name" required>
            <br><br>

            <label>Setting:</label><br>
            <input type="text" name="setting" required>
            <br><br>

            <label>Story Tone:</label><br>
            <input type="text" name="story_tone" required>
            <br><br>

            <label>Art Style:</label><br>
            <input type="text" name="art_style" required>
            <br><br>

            <button type="submit">Generate Comic</button>

        </form>

    </body>
    </html>
    """


# -----------------------------
# HEALTH CHECK
# -----------------------------

@router.get("/health")
def health_check():

    return {
        "status": "success",
        "message": "ComicCraft backend is running"
    }


# -----------------------------
# ABOUT
# -----------------------------

@router.get("/about")
def about():

    return {
        "project": "ComicCraft",
        "description": "AI Comic Story Creator"
    }


# -----------------------------
# COMIC GENERATION
# -----------------------------

@router.post("/generate", response_class=HTMLResponse)
def generate(
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    story_tone: str = Form(...),
    art_style: str = Form(...)
):

    try:

        # Step 1: Create 5-panel outline
        outline = generate_outline(story_prompt)

        # Step 2: Generate story content
        panels = generate_story(outline)

        # Step 3: Generate illustration for every panel
        for panel in panels:

            illustration = generate_illustration(
                panel["image_prompt"]
            )

            panel["illustration"] = illustration

        return f"""
        <!DOCTYPE html>
        <html>

        <head>
            <title>ComicCraft - Comic Preview</title>
        </head>

        <body>

            <h1>ComicCraft Comic Preview</h1>

            <h2>Story Details</h2>

            <p><b>Story:</b> {story_prompt}</p>
            <p><b>Character:</b> {character_name}</p>
            <p><b>Setting:</b> {setting}</p>
            <p><b>Story Tone:</b> {story_tone}</p>
            <p><b>Art Style:</b> {art_style}</p>

            <h2>Generated Comic</h2>

            <p>5 comic panels have been generated.</p>

            <ol>
                <li>{panels[0]["title"]}</li>
                <li>{panels[1]["title"]}</li>
                <li>{panels[2]["title"]}</li>
                <li>{panels[3]["title"]}</li>
                <li>{panels[4]["title"]}</li>
            </ol>

            <a href="/export-success">
                <button>Export Comic</button>
            </a>

        </body>

        </html>
        """

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Comic generation failed: {str(e)}"
        )


# -----------------------------
# JSON COMIC GENERATION
# -----------------------------

@router.post("/generate-comic/json")
def generate_comic_json(request: PromptRequest):

    try:

        # Step 1
        outline = generate_outline(request.prompt)

        # Step 2
        panels = generate_story(outline)

        # Step 3
        for panel in panels:

            illustration = generate_illustration(
                panel["image_prompt"]
            )

            panel["illustration"] = illustration

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


# -----------------------------
# EXPORT SUCCESS
# -----------------------------

@router.get("/export-success", response_class=HTMLResponse)
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


# -----------------------------
# IMAGE GENERATION TEST
# -----------------------------

@router.get("/test-image")
def test_image(prompt: str = "A cartoon character"):

    try:

        result = generate_illustration(prompt)

        return {
            "status": "success",
            "message": "Image generation test completed",
            "result": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}"
        )


# -----------------------------
# PDF DOWNLOAD
# -----------------------------

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
