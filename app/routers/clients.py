from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Client, Subscription
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.schemas.subscription import SubscriptionCreate, SubscriptionRead

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=list[ClientRead])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


@router.get("/{client_id}", response_model=ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/", response_model=ClientRead, status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.email == client.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    new_client = Client(**client.model_dump(), created_at=datetime.now(timezone.utc))
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@router.patch("/{client_id}", response_model=ClientRead)
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.id == client_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Client not found")
    for field, value in client.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()


@router.get("/{client_id}/subscriptions", response_model=list[SubscriptionRead])
def get_client_subscriptions(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client.subscriptions


@router.post("/{client_id}/subscriptions", response_model=SubscriptionRead, status_code=201)
def create_client_subscription(
    client_id: int, subscription: SubscriptionCreate, db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    new_sub = Subscription(
        **subscription.model_dump(),
        client_id=client_id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub
