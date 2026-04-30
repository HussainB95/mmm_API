from fastapi import FastAPI, APIRouter, HTTPException, Depends
from ..models import (CreateSlotRequest, BookSlotRequest)
from ..database_model import BookingSlot, Booking
from sqlalchemy.orm import Session
from ..database import get_db

app = FastAPI()

router = APIRouter(prefix= "/booking", tags= ["Booking System"])

# -- Create Slot --
@router.post("/create-slot")
def create_slot(
    data: CreateSlotRequest,
    db: Session = Depends(get_db)
):
    slot = BookingSlot(
        practitioner_id=data.practitioner_id,
        slot_date=data.slot_date,
        start_time=data.start_time,
        end_time=data.end_time,
        status="available"
    )

    db.add(slot)
    db.commit()
    db.refresh(slot)

    return {
        "message": "Slot created successfully",
        "slot_id": slot.id
    }


# -- Fetch Slot --
@router.get("/available-slots/{practitioner_id}")
def get_available_slots(
    practitioner_id: str,
    db: Session = Depends(get_db)
):
    slots = db.query(BookingSlot).filter(
        BookingSlot.practitioner_id == practitioner_id,
        BookingSlot.status == "available"
    ).all()

    return slots


# -- Book Slot --
@router.post("/book-slot")
def book_slot(
    data: BookSlotRequest,
    db: Session = Depends(get_db)
):
    slot = db.query(BookingSlot).filter(
        BookingSlot.id == data.slot_id
    ).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    if slot.status != "available":
        raise HTTPException(status_code=400, detail="Slot already booked")

    slot.status = "booked"

    booking = Booking(
        patient_id=data.patient_id,
        slot_id=data.slot_id,
        booking_status="confirmed"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "message": "Appointment booked successfully",
        "booking_id": booking.id
    }


# -- Delete Slot --
@router.delete("/cancel-booking/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    slot = db.query(BookingSlot).filter(
        BookingSlot.id == booking.slot_id
    ).first()

    if slot:
        slot.status = "available"

    db.delete(booking)
    db.commit()

    return {
        "message": "Booking cancelled successfully"
    }