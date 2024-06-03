from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os


# Create the FastAPI app
app = FastAPI()

# Mount the static files directory

static_dir = os.path.join(os.path.dirname(__file__), "public")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

# Run the app  

