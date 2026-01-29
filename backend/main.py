from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
import converters  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["http://localhost:5173"],
    allow_headers=["http://localhost:5173"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/convert")
async def convert_file(file: UploadFile):
    filename = file.filename
    base_name, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    supported_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.bmp']
    if ext not in supported_extensions:
        raise HTTPException(status_code=400, detail=f"Extension {ext} not supported.")

    unique_id = str(uuid.uuid4())
    input_filename = f"{unique_id}{ext}"
    input_path = os.path.join(UPLOAD_DIR, input_filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if ext == '.pdf':
        output_filename = f"{unique_id}.docx"
        output_path = os.path.join(UPLOAD_DIR, output_filename)

        success = converters.convert_pdf_to_docx(input_path, output_path)
        download_name = f"{base_name}.docx"

    else: 
        output_filename = f"{unique_id}.pdf"
        output_path = os.path.join(UPLOAD_DIR, output_filename)

        success = converters.convert_image_to_pdf(input_path, output_path)
        download_name = f"{base_name}.pdf"

    if success and os.path.exists(output_path):
        return FileResponse(
            path=output_path, 
            filename=download_name, 
            media_type='application/octet-stream'
        )
    else:
        raise HTTPException(status_code=500, detail="Intern error at conversion.")

@app.get("/")
def read_root():
    return {"status": "Backend running succesfully"}