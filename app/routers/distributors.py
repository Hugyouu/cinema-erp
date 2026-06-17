from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Distributor
from app.schemas.distributor import DistributorCreate, DistributorRead, DistributorUpdate

router = APIRouter(prefix="/distributors", tags=["Distributeurs"])


@router.get("/", response_model=list[DistributorRead])
def get_distributors(db: Session = Depends(get_db)):
    return db.query(Distributor).all()


@router.get("/{distributor_id}", response_model=DistributorRead)
def get_distributor(distributor_id: int, db: Session = Depends(get_db)):
    distributor = db.query(Distributor).filter(Distributor.id == distributor_id).first()
    if not distributor:
        raise HTTPException(status_code=404, detail="Distributor not found")
    return distributor


@router.post("/", response_model=DistributorRead, status_code=201)
def create_distributor(distributor: DistributorCreate, db: Session = Depends(get_db)):
    new_distributor = Distributor(**distributor.model_dump())
    db.add(new_distributor)
    db.commit()
    db.refresh(new_distributor)
    return new_distributor


@router.patch("/{distributor_id}", response_model=DistributorRead)
def update_distributor(distributor_id: int, distributor: DistributorUpdate, db: Session = Depends(get_db)):
    existing = db.query(Distributor).filter(Distributor.id == distributor_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Distributor not found")
    for field, value in distributor.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{distributor_id}", status_code=204)
def delete_distributor(distributor_id: int, db: Session = Depends(get_db)):
    distributor = db.query(Distributor).filter(Distributor.id == distributor_id).first()
    if not distributor:
        raise HTTPException(status_code=404, detail="Distributor not found")
    db.delete(distributor)
    db.commit()
