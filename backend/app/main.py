from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title="FishTrace", version="0.1.0", debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_method_list,
    allow_headers=settings.cors_header_list,
)
app.include_router(v1_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
def liveness() -> dict[str, str]:
    return {"status": "ok"}
