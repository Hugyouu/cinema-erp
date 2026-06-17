from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import DistributionContract, RoyaltyTier
from app.schemas.distribution_contract import (
    DistributionContractCreate,
    DistributionContractRead,
    DistributionContractUpdate,
)
from app.schemas.royalty_tier import RoyaltyTierCreate, RoyaltyTierRead

router = APIRouter(prefix="/contracts", tags=["Contrats de distribution"])


@router.get("/", response_model=list[DistributionContractRead])
def get_contracts(db: Session = Depends(get_db)):
    return db.query(DistributionContract).all()


@router.get("/{contract_id}", response_model=DistributionContractRead)
def get_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = db.query(DistributionContract).filter(DistributionContract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


@router.post("/", response_model=DistributionContractRead, status_code=201)
def create_contract(contract: DistributionContractCreate, db: Session = Depends(get_db)):
    new_contract = DistributionContract(**contract.model_dump())
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    return new_contract


@router.patch("/{contract_id}", response_model=DistributionContractRead)
def update_contract(contract_id: int, contract: DistributionContractUpdate, db: Session = Depends(get_db)):
    existing = db.query(DistributionContract).filter(DistributionContract.id == contract_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Contract not found")
    for field, value in contract.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{contract_id}", status_code=204)
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = db.query(DistributionContract).filter(DistributionContract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    db.delete(contract)
    db.commit()


@router.get("/{contract_id}/royalty-tiers", response_model=list[RoyaltyTierRead])
def get_royalty_tiers(contract_id: int, db: Session = Depends(get_db)):
    contract = db.query(DistributionContract).filter(DistributionContract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract.royalty_tiers


@router.post("/{contract_id}/royalty-tiers", response_model=RoyaltyTierRead, status_code=201)
def create_royalty_tier(contract_id: int, tier: RoyaltyTierCreate, db: Session = Depends(get_db)):
    contract = db.query(DistributionContract).filter(DistributionContract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    new_tier = RoyaltyTier(**tier.model_dump(), contract_id=contract_id)
    db.add(new_tier)
    db.commit()
    db.refresh(new_tier)
    return new_tier
