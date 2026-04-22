from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from .. import models, schemas
from ..database import get_db
from datetime import datetime, timezone
import random
import string
from ..auth import send_prediction_confirmation

router = APIRouter(
    prefix="/api/v1/challenges",
    tags=["challenges"],
)

@router.get("", response_model=List[schemas.ChallengeResponse])
def get_challenges(db: Session = Depends(get_db)):
    challenges = db.query(models.Challenge).filter(models.Challenge.is_active == True).all()
    
    # Calculate participant count for each challenge
    result = []
    for challenge in challenges:
        participant_count = db.query(models.Prediction).filter(models.Prediction.challenge_id == challenge.id).count()
        
        # Convert to response schema manually to add participant_count
        challenge_data = schemas.ChallengeResponse.from_orm(challenge)
        challenge_data.participant_count = participant_count
        result.append(challenge_data)
        
    return result

@router.get("/{challenge_id}", response_model=schemas.ChallengeResponse)
def get_challenge(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    participant_count = db.query(models.Prediction).filter(models.Prediction.challenge_id == challenge.id).count()
    
    challenge_data = schemas.ChallengeResponse.from_orm(challenge)
    challenge_data.participant_count = participant_count
    
    return challenge_data

@router.post("/{challenge_id}/predict", response_model=schemas.PredictionResponse)
def create_prediction(challenge_id: int, prediction: schemas.PredictionCreate, db: Session = Depends(get_db)):
    # Check if challenge exists and is active
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    if not challenge.is_active:
        raise HTTPException(status_code=400, detail="Challenge is no longer active")
    
    if challenge.end_date < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Challenge has ended")

    if challenge.prediction_deadline and challenge.prediction_deadline < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="La fecha límite para participar en este desafío ha pasado.")

    # Check if email already participated in this challenge
    existing_email = db.query(models.Prediction).filter(
        models.Prediction.challenge_id == challenge_id,
        models.Prediction.email == prediction.email
    ).first()
    
    if existing_email:
        raise HTTPException(status_code=400, detail="Ya has participado en este desafío con este email.")

    # Check if nickname already taken in this challenge
    existing_nickname = db.query(models.Prediction).filter(
        models.Prediction.challenge_id == challenge_id,
        models.Prediction.nickname == prediction.nickname
    ).first()
    
    if existing_nickname:
        raise HTTPException(status_code=400, detail="Ese apodo ya está en uso para este desafío. ¡Prueba con otro!")

    # Check if minute already taken (only first 16 chars: YYYY-MM-DDTHH:mm)
    minute_prefix = prediction.prediction_value[:16]
    existing_minute = db.query(models.Prediction).filter(
        models.Prediction.challenge_id == challenge_id,
        models.Prediction.prediction_value.like(f"{minute_prefix}%")
    ).first()
    
    if existing_minute:
        raise HTTPException(status_code=400, detail="Este minuto ya ha sido seleccionado por otro participante. ¡Nadie puede repetir el mismo minuto! Por favor, elige uno diferente.")

    # Generate verification code
    verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # Create prediction
    db_prediction = models.Prediction(
        challenge_id=challenge_id,
        nickname=prediction.nickname,
        email=prediction.email,
        prediction_value=prediction.prediction_value,
        verification_code=verification_code
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    # Send confirmation email
    send_prediction_confirmation(
        to_email=db_prediction.email,
        nickname=db_prediction.nickname,
        challenge_title=challenge.title,
        prediction_date=db_prediction.prediction_value,
        code=verification_code
    )

    return db_prediction

@router.get("/{challenge_id}/predictions", response_model=List[schemas.PredictionPublic])
def get_challenge_predictions(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
        
    predictions = db.query(models.Prediction).filter(models.Prediction.challenge_id == challenge_id).order_by(models.Prediction.prediction_value.asc()).all()
    return predictions
