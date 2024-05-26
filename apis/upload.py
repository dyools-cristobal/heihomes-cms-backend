from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "/public_html/images"

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        # Open the file in binary write mode and write the uploaded file's contents directly
        with open(os.path.join(UPLOAD_DIR, file.filename), "wb") as f: # type: ignore
            f.write(await file.read())

        # Assuming your server has a public URL for serving static files
        file_url = f"https://files.000webhost.com/{UPLOAD_DIR}/{file.filename}"

        return JSONResponse(content={"file_url": file_url})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
