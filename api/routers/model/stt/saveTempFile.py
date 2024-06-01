import aiofiles
import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends

async def save_temp_file(upload_file: UploadFile) -> str:
    temp_folder_path = 'temp'
    os.makedirs(temp_folder_path, exist_ok=True)
    temp_file_path = os.path.join(temp_folder_path, upload_file.filename)
    
    try:
        async with aiofiles.open(temp_file_path, 'wb') as out_file:
            while True:
                content = await upload_file.read(1024*1024)  # 1MB 단위로 읽기
                if not content:
                    break
                await out_file.write(content)
    except Exception as e:
        print(f"Failed to write to file: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save file")
    
    return temp_file_path
