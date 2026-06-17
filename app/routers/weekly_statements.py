from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import WeeklyStatement, StatementStatus
from app.schemas.weekly_statement import WeeklyStatementCreate, WeeklyStatementRead, WeeklyStatementUpdate

router = APIRouter(prefix="/statements", tags=["Relevés hebdomadaires"])


@router.get("/", response_model=list[WeeklyStatementRead])
def get_statements(db: Session = Depends(get_db)):
    return db.query(WeeklyStatement).all()


@router.get("/{statement_id}", response_model=WeeklyStatementRead)
def get_statement(statement_id: int, db: Session = Depends(get_db)):
    statement = db.query(WeeklyStatement).filter(WeeklyStatement.id == statement_id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    return statement


@router.post("/", response_model=WeeklyStatementRead, status_code=201)
def create_statement(statement: WeeklyStatementCreate, db: Session = Depends(get_db)):
    new_statement = WeeklyStatement(
        **statement.model_dump(),
        generated_at=datetime.now(timezone.utc),
    )
    db.add(new_statement)
    db.commit()
    db.refresh(new_statement)
    return new_statement


@router.patch("/{statement_id}", response_model=WeeklyStatementRead)
def update_statement(statement_id: int, statement: WeeklyStatementUpdate, db: Session = Depends(get_db)):
    existing = db.query(WeeklyStatement).filter(WeeklyStatement.id == statement_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Statement not found")
    for field, value in statement.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


@router.post("/{statement_id}/validate", response_model=WeeklyStatementRead)
def validate_statement(statement_id: int, db: Session = Depends(get_db)):
    statement = db.query(WeeklyStatement).filter(WeeklyStatement.id == statement_id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    if statement.status != StatementStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Only draft statements can be validated")
    statement.status = StatementStatus.VALIDATED
    db.commit()
    db.refresh(statement)
    return statement
