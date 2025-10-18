from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes.claims import router as claims_router
from .routes.moderation import router as moderation_router
from .routes.demo import router as demo_router
from .config import settings

app = FastAPI(title="VerityVue API", version="0.4.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.mount('/media', StaticFiles(directory=settings.media_dir), name='media')

app.include_router(claims_router)
app.include_router(moderation_router)
app.include_router(demo_router)

@app.get("/")

def root():
	return {"status": "ok", "service": "verityvue"}
