import os
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
import uuid
from core.converter import process_file, resize_file, optimize_file, create_gif, convert_document, extract_text

app = FastAPI(title="Noire Converter API", version="2.4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = os.path.join(os.getcwd(), "temp_workspace")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.post("/api/v1/convert")
async def convert_media(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    target_format: str = Form(...),
    quality: int = Form(100)
):
    try:
        safe_filename = f"{uuid.uuid4()}_{file.filename}"
        input_path = os.path.join(TEMP_DIR, safe_filename)
        
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        output_path = process_file(input_path, target_format, quality, TEMP_DIR)
        
        # Hafıza/Disk şişmesini önleme: İstek bitince geçici dosyaları sil
        def cleanup(f1, f2):
            if os.path.exists(f1): os.remove(f1)
            if os.path.exists(f2): os.remove(f2)
            
        background_tasks.add_task(cleanup, input_path, output_path)
        
        pure_name = file.filename.rsplit('.', 1)[0]
        ext = target_format.lower().strip()
        
        return FileResponse(
            output_path,
            filename=f"converted_{pure_name}.{ext}",
            media_type="application/octet-stream"
        )
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/api/v1/resize")
async def resize_media(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    width: int = Form(...),
    height: int = Form(...)
):
    try:
        safe_filename = f"{uuid.uuid4()}_{file.filename}"
        input_path = os.path.join(TEMP_DIR, safe_filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        output_path = resize_file(input_path, width, height, TEMP_DIR)
        
        def cleanup(f1, f2):
            if os.path.exists(f1): os.remove(f1)
            if os.path.exists(f2): os.remove(f2)
        background_tasks.add_task(cleanup, input_path, output_path)
        
        return FileResponse(output_path, filename=f"resized_{file.filename}")
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/api/v1/optimize")
async def optimize_media(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    quality: int = Form(80)
):
    try:
        safe_filename = f"{uuid.uuid4()}_{file.filename}"
        input_path = os.path.join(TEMP_DIR, safe_filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        output_path = optimize_file(input_path, quality, TEMP_DIR)
        
        def cleanup(f1, f2):
            if os.path.exists(f1): os.remove(f1)
            if os.path.exists(f2): os.remove(f2)
        background_tasks.add_task(cleanup, input_path, output_path)
        
        return FileResponse(output_path, filename=f"optimized_{file.filename}")
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/api/v1/gif-studio")
async def gif_studio_media(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    start_time: str = Form("00:00"),
    end_time: str = Form("00:05")
):
    try:
        safe_filename = f"{uuid.uuid4()}_{file.filename}"
        input_path = os.path.join(TEMP_DIR, safe_filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        output_path = create_gif(input_path, start_time, end_time, TEMP_DIR)
        
        def cleanup(f1, f2):
            if os.path.exists(f1): os.remove(f1)
            if os.path.exists(f2): os.remove(f2)
        background_tasks.add_task(cleanup, input_path, output_path)
        
        return FileResponse(output_path, filename=f"animated_{file.filename}.gif")
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/api/v1/doc-station")
async def doc_station_media(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    target_format: str = Form(...)
):
    try:
        safe_filename = f"{uuid.uuid4()}_{file.filename}"
        input_path = os.path.join(TEMP_DIR, safe_filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        output_path = convert_document(input_path, target_format, TEMP_DIR)
        
        def cleanup(f1, f2):
            if os.path.exists(f1): os.remove(f1)
            if os.path.exists(f2): os.remove(f2)
        background_tasks.add_task(cleanup, input_path, output_path)
        
        return FileResponse(output_path, filename=f"doc_{file.filename}_{target_format}")
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/api/v1/extract-text")
async def extract_text_media(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    language: str = Form("eng+tur")
):
    try:
        safe_filename = f"{uuid.uuid4()}_{file.filename}"
        input_path = os.path.join(TEMP_DIR, safe_filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        output_path = extract_text(input_path, language, TEMP_DIR)
        
        def cleanup(f1, f2):
            if os.path.exists(f1): os.remove(f1)
            if os.path.exists(f2): os.remove(f2)
        background_tasks.add_task(cleanup, input_path, output_path)
        
        return FileResponse(output_path, filename=f"extracted_ocr.txt")
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

app.mount("/", StaticFiles(directory="web", html=True), name="web")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
