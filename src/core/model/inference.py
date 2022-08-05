from pydantic import BaseModel


class Inference(BaseModel):
    id: str
    age: int
    sex: str
    user_id: str
    model_id: str
    status: str


class UploadAudio(BaseModel):
    content: bytes
    filename: str


class InferenceFiles(BaseModel):
    aceite: UploadAudio
    vogal_sustentada: UploadAudio
    parlenda_ritmada: UploadAudio
    frase: UploadAudio
