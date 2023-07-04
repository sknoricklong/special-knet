from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def upvote(vote: schemas.Upvote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    event = db.query(models.Event).filter(
        models.Event.id == vote.event_id).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with id: {vote.event_id} was not found")

    is_upvoted = db.query(models.Upvote).filter_by(
        user_id=current_user.id, event_id=vote.event_id).first()

    if is_upvoted:
        db.delete(is_upvoted)
    else:
        new_vote = models.Upvote(
            user_id=current_user.id, event_id=vote.event_id)
        db.add(new_vote)

    db.commit()
    return event
