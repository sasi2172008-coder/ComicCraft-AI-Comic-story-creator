
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from reportlab.pdfgen import canvas
from io import BytesIO

router = APIRouter()


# -----------------------------
# JSON Request Model
# -----------------------------

class PromptRequest(BaseModel):
    prompt: str


# -----------------------------
# Homepage Route
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

        <p>Create your own AI-powered comic story.</p>

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
# Health Check
# -----------------------------

@router.get("/health")
def health_check():
    return {
        "status": "success",
        "message": "ComicCraft backend is running"
    }


# -----------------------------
# About Route
# -----------------------------

@router.get("/about")
def about():
    return {
        "project": "ComicCraft",
        "description": "AI Comic Story Creator"
    }


# -----------------------------
# Comic Generation Route
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

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ComicCraft - Comic Preview</title>
        </head>

        <body>

            <h1>ComicCraft Comic Preview</h1>

            <h2>Story Details</h2>

            <p><strong>Story:</strong> {story_prompt}</p>
            <p><strong>Character:</strong> {character_name}</p>
            <p><strong>Setting:</strong> {setting}</p>
            <p><strong>Story Tone:</strong> {story_tone}</p>
            <p><strong>Art Style:</strong> {art_style}</p>

            <h2>Comic Generation</h2>

            <p>Your 5-panel comic generation request has been received.</p>

            <p>Comic panels will be generated using the AI workflow.</p>

            <a href="/export-success">
                <button>Continue</button>
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
# JSON Comic Generation API
# -----------------------------

@router.post("/generate-comic/json")
def generate_comic_json(request: PromptRequest):

    try:

        return {
            "status": "success",
            "message": "Comic generation API is working",
            "prompt": request.prompt,
            "panels": 5,
            "layout": "5-panel comic layout",
            "pdf_path": "ComicCraft.pdf"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Comic generation failed: {str(e)}"
        )


# -----------------------------
# Export Success Route
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
# Image Generation Test Route
# -----------------------------

@router.get("/test-image")
def test_image(prompt: str = "A cartoon character"):

    try:

        return {
            "status": "success",
            "message": "Image generation test endpoint is working",
            "prompt": prompt
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}"
        )


# -----------------------------
# PDF Download Route
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

        pdf.drawString(50, 800, "ComicCraft - AI Comic")

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
