from fastapi import APIRouter
from fastapi.responses import HTMLResponse

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
