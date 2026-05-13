import zipfile
from io import BytesIO
from typing import Any

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from backend.database import fetch_all_files

download_zip_router = APIRouter()

@download_zip_router.get("/api/download_zip/{session_id}")
def download_zip(session_id: str):
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zip_file:
        files: list[Any] = fetch_all_files(session_id)
        for file_name, content in files:
            if file_name == "build.gradle":
                zip_file.writestr("game/build.gradle", content)
            elif file_name.endswith(".java"):
                zip_file.writestr(f"backend/game/src/main/java/com/example/{file_name}", content)
            else:
                zip_file.writestr(f"frontend/{file_name}", content)

    buf.seek(0)

    return StreamingResponse(buf, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=game.zip"})
