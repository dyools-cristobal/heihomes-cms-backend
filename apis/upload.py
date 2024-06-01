from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException, Depends
import aiofiles
import os
from ftplib import FTP

router = APIRouter()

# FTP credentials and server details
FTP_SERVER = '82.197.80.89'
FTP_USER = 'u810413882'
FTP_PASSWORD = 'livewithHEI1989!'
FTP_UPLOAD_DIR = '/public_html/assets/images/rooms/'

ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

async def upload_to_ftp(file_path: str, remote_path: str):
    try:
        with FTP() as ftp:
            ftp.connect(FTP_SERVER)
            ftp.login(FTP_USER, FTP_PASSWORD)
            with open(file_path, 'rb') as f:
                ftp.storbinary(f'STOR {remote_path}', f)
    except ConnectionRefusedError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to FTP server: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"FTP upload failed: {str(e)}")
    
@router.post("/upload/")
async def upload_image(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    UPLOAD_DIR = "uploads"
    
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    if file.filename:
        # File type validation
        file_ext = file.filename.split('.')[-1]
        if file_ext.lower() not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Only jpeg, jpg, and png files are allowed.")

        # File size validation
        if file.file.__sizeof__() > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds 2MB limit.")

        # File name validation
        if ' ' in file.filename:
            raise HTTPException(status_code=400, detail="File name should not contain spaces.")

        file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file locally
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # Upload the file to the FTP server
    if file.filename:
        remote_path = os.path.join(FTP_UPLOAD_DIR, file.filename)
        background_tasks.add_task(upload_to_ftp, file_path, remote_path)
        await background_tasks()

        # Construct the URL of the uploaded image
        file_url = f"{file.filename}"
   
    return {"info": f"file '{file.filename}' uploaded successfully", "url": file_url}

@router.post("/upload_image/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    UPLOAD_DIR = "uploads"
    
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    if file.filename:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file locally
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # Upload the file to the FTP server
    if file.filename:
        remote_path = os.path.join(FTP_UPLOAD_DIR, file.filename)
        background_tasks.add_task(upload_to_ftp, file_path, remote_path)
        await background_tasks()

        # Construct the URL of the uploaded image
        file_url = f"{file_path}{file.filename}"
   
    return {"info": f"file '{file.filename}' uploaded successfully", "url": file_url}
