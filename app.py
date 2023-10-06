from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
import uvicorn
import time
import json
import yaml
import os

timestr = time.strftime("%Y%m%d-%H%M%S")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}

@app.post("/file/upload")
def upload_file(file: UploadFile):
    if file.content_type != 'application/json':
        raise HTTPException(400, detail="Invalid document type")
    else:
        data = json.loads(file.file.read())
        return {"content": data, "filename": file.filename}
    
@app.post("/file/uploadndownload")
def upload_n_downloadfile(file: UploadFile):
    """"Return a YAML file for the uploaded JSON"""
    if file.content_type != 'application/json':
        raise HTTPException(400, detail="Invalid document type")
    else:
        json_data = json.loads(file.file.read())
        new_filename = "{}_{}.yaml".format(os.path.splitext(file.filename)[0], timestr)
        # Write the data to a file
        # Store the saved file
        SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_filename)
        with open(SAVE_FILE_PATH, "w") as f:
            yaml.dump(json_data,f)
        # Return as a download
        return FileResponse(path=SAVE_FILE_PATH, media_type="application/txt", filename=new_filename)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)