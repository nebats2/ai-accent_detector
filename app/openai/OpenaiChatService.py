import os

from fastapi import HTTPException
from openai import OpenAI, BaseModel
from langchain.chat_models import init_chat_model
from pydantic import Field


from app.openai.Configuration import OpenaiSettingModel
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.Downloader import downloaded_video_path

openai_setting = OpenaiSettingModel()

openai_client = OpenAI(api_key =openai_setting.api_key)

class ScalingSchema(BaseModel):
    us:float=Field("accent or dialect scale from 0 to 5 for USA")
    au:float=Field("accent or dialect scale from 0 to 5 for Australia")
    ca:float=Field("accent or dialect scale from 0 to 5 for Canada")
    gb:float=Field("accent or dialect scale from 0 to 5 for Britain ")
    ind:float=Field("accent or dialect scale from 0 to 5 for India")
    ng: float =Field("accent or dialect scale from 0 to 5 for Nigeria")
    ke:float =Field("accent or dialect scale from 0 to 5 for Kenya")
    za:float=Field("accent or dialect scale from 0 to 5 for South Africa")
    model_config = {
        "extra": "forbid"
    }

openai_chat_model = init_chat_model(
    openai_setting.model,
    model_provider ="openai",
    api_key = openai_setting.api_key
)


def get_accent_scale(transcript_text:str):
    openai_structured = openai_chat_model.with_structured_output(ScalingSchema)
    messages =[
        SystemMessage(content=(
                "You are a dialect classifier. Given a sentence, return a JSON object exactly matching this schema: rating  each dialect from 0 to 5"
            )),
        HumanMessage(transcript_text)
    ]
    result: ScalingSchema = openai_structured.invoke(messages)
    return result

def get_video_transcript_text():
    file_path = downloaded_video_path
    if os.path.isfile(file_path):
        print("File exists.")
    else:
        raise HTTPException(status_code=500, detail="Video is not downloaded.Please download the video from url or local system.")

    with open(file_path, "rb") as f:
        transcript = transcript_video(f)
        print(f"\n {transcript}")
    return transcript

def openai_unstructured_chat(system_message:str, human_message: str):
    messages= [
        SystemMessage(system_message),
        HumanMessage(human_message)
    ]
    result = openai_chat_model.invoke(messages)

def transcript_video(video_file):
    return  openai_client.audio.transcriptions.create(
        model=openai_setting.transcription_model,
        file=video_file,
        language="en"
    )