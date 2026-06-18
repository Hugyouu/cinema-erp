from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Invoice, InvoiceStatus
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceUpdate

router = APIRouter(prefix="/invoices", tags=["Factures"])


@router.get("/", response_model=list[InvoiceRead])
def get_invoices(db: Session = Depends(get_db)):
    return db.query(Invoice).all()


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/", response_model=InvoiceRead, status_code=201)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    existing = db.query(Invoice).filter(Invoice.invoice_number == invoice.invoice_number).first()
    if existing:
        raise HTTPException(status_code=409, detail="Invoice number already exists")
    new_invoice = Invoice(
        **invoice.model_dump(),
        invoice_number=f"FAC-{datetime.now().year}-{str(uuid.uuid4())[:5].upper()}"
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice


@router.patch("/{invoice_id}", response_model=InvoiceRead)
def update_invoice(invoice_id: int, invoice: InvoiceUpdate, db: Session = Depends(get_db)):
    existing = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Invoice not found")
    for field, value in invoice.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


@router.post("/{invoice_id}/mark-paid", response_model=InvoiceRead)
def mark_invoice_paid(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if invoice.status == InvoiceStatus.PAID:
        raise HTTPException(status_code=400, detail="Invoice is already paid")
    if invoice.status == InvoiceStatus.CANCELLED:
        raise HTTPException(status_code=400, detail="Cannot pay a cancelled invoice")
    invoice.status = InvoiceStatus.PAID
    db.commit()
    db.refresh(invoice)
    return invoice
