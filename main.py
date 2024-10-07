from fastapi import FastAPI, status, UploadFile
from utility import get_file
import uvicorn
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post('/')
def main():
    return {"message": "Welcome to Sentimental Detection Analysis"}

@app.post('/upload/filename')
async def upload_file_xlsx(file: UploadFile):
    message = "Bad request"
    status_code = status.HTTP_400_BAD_REQUEST
    try:
        status_code, message = await get_file(file)

        return JSONResponse(status_code=status_code, content={"message": message})

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Bad request"})

