from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal
from .models import Doctor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

disease_keywords = {
    "Cardiology": ["jantung", "dada", "nyeri dada", "sakit dada", "berdebar"],
    "Dermatology": ["kulit", "ruam", "gatal", "iritasi kulit"],
    "General Practice": ["umum", "demam", "batuk", "pilek", "flu"],
    "Neurology": ["saraf", "kepala", "sakit kepala", "pusing", "migraine"],
    "Pulmonology": ["paru", "sesak napas", "nafas", "batuk berat"],
    "Ophthalmology": ["mata", "merah", "penglihatan", "rabun"],
    "ENT Specialist": ["telinga", "hidung", "tenggorokan", "sakit telinga"],
}

def get_specializations():
    db = SessionLocal()
    specs = set()
    try:
        for doc in db.query(Doctor).all():
            if doc.specialization:
                specs.add(doc.specialization)
    finally:
        db.close()
    return list(specs)

def recommend_specialist(message: str):
    message_lower = message.lower()
    specs = get_specializations()
    for specialist, keywords in disease_keywords.items():
        if specialist in specs:
            for keyword in keywords:
                if keyword in message_lower:
                    return specialist
    return specs[0] if specs else "General Practice"

class ChatRequest(BaseModel):
    messages: List[str]

class ChatResponse(BaseModel):
    reply: str
    recommended_specialist: str = None

@app.post("/chat", response_model=ChatResponse)
def chat_ai(req: ChatRequest):
    last_message = req.messages[-1] if req.messages else ""
    specialist = recommend_specialist(last_message)
    reply = f"Berdasarkan gejala yang Anda sebutkan, kami sarankan konsultasi ke {specialist}. Apakah Anda ingin booking appointment?"
    return ChatResponse(reply=reply, recommended_specialist=specialist)
