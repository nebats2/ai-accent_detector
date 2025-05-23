from fastapi import FastAPI, Query

from app.openai.Configuration import OpenaiSettingBaseModel, set_openai_config, get_openai_settings
from app.openai.OpenaiChatService import get_video_transcript_text, get_accent_scale
from app.services.Downloader import download_video_url, download_local_video


app = FastAPI()

@app.get("/config/openai", response_model=OpenaiSettingBaseModel)
def get_openai_config_setting():
    return get_openai_settings()

@app.post("/config/openai")
def set_openai_settings(model: OpenaiSettingBaseModel):
    set_openai_config(model)
    return get_openai_settings()

@app.post("/download/video/web")
async def download_video(url: str = Query(...)):
    file_path = await download_video_url(url)
    return {
        "content":"successfully downloaded in temp",
        "path":file_path
    }
@app.post("/download/video/local/{url}")
def download_video(url:str):
    file_path = download_local_video(url)
    return {
        "content":"successfully downloaded in temp",
        "path":file_path
    }

@app.get("/accent/rate")
def get_accent_rate():
    transcript_text = get_video_transcript_text().text
    return {
        "content":get_accent_scale(transcript_text)
    }

