from fastapi import APIRouter, HTTPException, Depends, status, Response, Query
from sqlalchemy import distinct, and_, text, or_, desc, func
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.EventOut])
async def get_events(
    skip: int = 0,
    limit: int = 10,
    q: Optional[str] = None,
    tags: List[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    query = (db.query(models.Event, func.count(models.Upvote.event_id).label("upvotes"))
             .outerjoin(models.Upvote, models.Upvote.event_id == models.Event.id)
             .group_by(models.Event.id))

    if tags and q:
        print(q)
        search = "%{}%".format(q)
        query = query.filter(
            and_(
                models.Event.tags.any(tag in tags),
                or_(models.Event.title.ilike(search),
                    models.Event.description.ilike(search))
            )
        )
    elif tags:
        query = query.filter(models.Event.tags.any(tag in tags))
    elif q:
        print(q)
        search = "%{}%".format(q)
        query = query.filter(or_(models.Event.title.ilike(
            search), models.Event.description.ilike(search)))

    results = query.order_by(desc("upvotes")).offset(skip).limit(limit).all()

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_event = models.Event(user_id=current_user.id, **event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@router.get("/{id}", response_model=schemas.EventOut)
def get_event(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    event = (db.query(models.Event, func.count(models.Upvote.event_id).label("upvotes"))
             .outerjoin(models.Upvote, models.Upvote.event_id == models.Event.id)
             .group_by(models.Event.id)
             .filter(models.Event.id == id).first())

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with id: {id} was not found")
    return event


@router.delete("/{id}")
def delete_event(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    event = db.query(models.Event).filter(models.Event.id == id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with id: {id} was not found")
    if event.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    db.delete(event)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Event)
def update_event(id: int, event: schemas.EventUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    existing_event = db.query(models.Event).filter(
        models.Event.id == id).first()
    if not existing_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with id: {id} was not found")
    if existing_event.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    event_dict = event.dict(exclude_unset=True)
    for key, value in event_dict.items():
        setattr(existing_event, key, value)
    db.commit()
    db.refresh(existing_event)
    return existing_event
