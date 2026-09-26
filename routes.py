from fastapi import APIRouter
from fastapi.responses import HTMLResponse, StreamingResponse
from reportlab.pdfgen import canvas
from io import BytesIO

router = APIRouter()


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


@router.get("/generate-comic/json")
def generate_comic_json():
    return {
        "status": "success",
        "message": "Comic generation API is working",
        "panels": 5
    }


@router.get("/test-image")
def test_image():
    return {
        "status": "success",
        "message": "Image generation test endpoint is working"
    }


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


@router.get("/download-pdf")
def download_pdf(
    story_prompt: str,
    character_name: str,
    setting: str,
    story_tone: str,
    art_style: str
):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle("ComicCraft Comic")

    pdf.drawString(50, 800, "ComicCraft - AI Comic")
    pdf.drawString(50, 770, f"Story: {story_prompt}")
    pdf.drawString(50, 740, f"Character: {character_name}")
    pdf.drawString(50, 710, f"Setting: {setting}")
    pdf.drawString(50, 680, f"Story Tone: {story_tone}")
    pdf.drawString(50, 650, f"Art Style: {art_style}")

    pdf.drawString(50, 600, "Comic generated successfully!")

    pdf.save()

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=ComicCraft.pdf"
        }
    )
