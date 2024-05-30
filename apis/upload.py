from fastapi import APIRouter, File, UploadFile, HTTPException
from ftplib import FTP
import aiofiles
import os

router = APIRouter()

# FTP credentials and server details
FTP_SERVER = 'ftp://82.197.80.89:21'
FTP_USER = 'u810413882'
FTP_PASSWORD = 'livewithHEI1989!'
FTP_UPLOAD_DIR = '/assets/images/'

async def upload_to_ftp(file_path: str, remote_path: str):
    try:
        ftp = FTP(FTP_SERVER)
        ftp.login(user=FTP_USER, passwd=FTP_PASSWORD)
        with open(file_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_path}', f)
        ftp.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"FTP upload failed: {str(e)}")

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    UPLOAD_DIR = "uploads"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename) # type: ignore
    
    # Save the uploaded file locally
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # Upload the file to the FTP server
    remote_path = os.path.join(FTP_UPLOAD_DIR, file.filename) # type: ignore
    await upload_to_ftp(file_path, remote_path)
    
    # Optionally, delete the local file after upload
    os.remove(file_path)
    
    return {"info": f"file '{file.filename}' uploaded successfully"}