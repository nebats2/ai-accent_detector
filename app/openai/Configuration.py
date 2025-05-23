from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

openai_config_path = Path(__file__).parent/ "openai.env"

class OpenaiSettingBaseModel(BaseModel):
    url : str
    api_key:str
    model: str
    transcription_model: str = "whisper-1"    #whisper-1 is a default value for the transcription model


class OpenaiSettingModel(BaseSettings):
    url: str
    api_key: str
    model:str
    transcription_model:str

    class Config:
        env_file = openai_config_path


def set_openai_config(model : OpenaiSettingBaseModel):
    setting_path = openai_config_path
    print(f"setting openai config {model}")
    try:
        with open(setting_path, "w") as f:
            for key, value in model.model_dump().items():
               f.write(f"{key.upper()}={value}\n")
    except Exception as e:
        print(f"Exception while configuring openai settings {e}")
        raise e
    print(f"setting openai config completed successfully")

def get_openai_settings() -> OpenaiSettingBaseModel:
    openai_settings = OpenaiSettingModel()
    setting_out = OpenaiSettingBaseModel(**openai_settings.model_dump())
    return setting_out