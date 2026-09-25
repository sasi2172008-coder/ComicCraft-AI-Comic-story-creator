from fastapi import APIRouter

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
