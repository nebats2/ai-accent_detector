import os
import shutil
import tempfile

import ffmpeg
import httpx
from langgraph_sdk.auth.exceptions import HTTPException
from moviepy import VideoFileClip
temp_dir = tempfile.gettempdir()
downloaded_video_path = os.path.join(temp_dir, "downloaded_video.mp4")
downloaded_audio_path = os.path.join(temp_dir,"downloaded_audio.wav")


async def download_video_url(download_url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(download_url)
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=f"Error downloading video: {e}")

    try:

        with open(downloaded_video_path, "wb") as f:
            async for chunk in response.aiter_bytes():
                f.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving video: {e}")

    return downloaded_video_path

def download_local_video(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Source video file not found")

    try:
         shutil.copyfile(file_path, downloaded_video_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error copying video file: {e}")

    return downloaded_video_path