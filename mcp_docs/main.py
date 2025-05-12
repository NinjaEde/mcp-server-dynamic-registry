from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Frage(BaseModel):
    frage: str

@app.post("/answer")
def antwort(frage: Frage):
    return {"antwort": f"Antwort von Docs: {frage.frage}"}

