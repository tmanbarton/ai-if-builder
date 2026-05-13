import zipfile
from io import BytesIO

from fastapi import FastAPI

app = FastAPI()

@app.get("/api/download_zip/{session_id}")
def download_zip():
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zip_file:
        zip_file.writestr("game/build.gradle", )
        zip_file.writestr("game/src/main/java/com/example/", )
    buf.seek(0)
