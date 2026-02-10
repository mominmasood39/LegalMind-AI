from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import timedelta
from typing import Optional
import speech_recognition as sr
from gtts import gTTS
import os
import shutil

from backend.config import settings
from backend.auth import (
    authenticate_user, create_access_token, get_current_user,
    Token, User, create_user, get_password_hash
)
from backend.rag_engine import RAGEngine

# Initialize FastAPI
app = FastAPI(title="LegalMind AI API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine
rag_engine = None

@app.on_event("startup")
async def startup_event():
    global rag_engine
    print("Starting LegalMind AI API...")
    rag_engine = RAGEngine()
    print("✓ API ready")

# Pydantic models
class SignupRequest(BaseModel):
    username: str
    email: str
    full_name: str
    password: str

class QueryRequest(BaseModel):
    question: str
    language: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: list
    language: str

# Routes
@app.get("/")
async def root():
    return {
        "message": "LegalMind AI API",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/signup")
async def signup(request: SignupRequest):
    """Create new user account"""
    try:
        user = create_user(
            username=request.username,
            email=request.email,
            full_name=request.full_name,
            password=request.password
        )
        return {
            "message": "Account created successfully",
            "username": user.username
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating account: {str(e)}"
        )

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user

@app.post("/query", response_model=QueryResponse)
async def query_legal_assistant(
    request: QueryRequest,
    current_user: User = Depends(get_current_user)
):
    """Query the legal assistant"""
    try:
        # Pass user_id for conversation state tracking
        result = rag_engine.query(request.question, user_id=current_user.username)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )
@app.post("/voice-query")
async def voice_query(
    audio_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Process voice query"""
    try:
        # Save uploaded audio file
        audio_path = f"uploads/{audio_file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Convert audio to text
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        # Clean up audio file
        os.remove(audio_path)
        
        # Process query
        result = rag_engine.query(text)
        
        # Generate audio response
        tts = gTTS(text=result['answer'], lang='en' if result['language'] == 'english' else 'ur')
        audio_response_path = f"uploads/response_{current_user.username}.mp3"
        tts.save(audio_response_path)
        
        return {
            "transcribed_text": text,
            "answer": result['answer'],
            "sources": result['sources'],
            "audio_response": audio_response_path
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing voice query: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)