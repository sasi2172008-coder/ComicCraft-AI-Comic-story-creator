from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import router


app = FastAPI(
    title="ComicCraft - AI Comic Story Creator"
)

# Include all application routes
app.include_router(router)

# Serve images, CSS and other static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
