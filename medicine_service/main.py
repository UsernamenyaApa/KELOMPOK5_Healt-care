import strawberry
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import database
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

@strawberry.type
class MedicineType:
    id: int
    name: str
    price: float
    description: str

@strawberry.type
class AppointmentMedicineType:
    id: int
    appointment_id: int
    medicine_id: int
    quantity: int

@strawberry.type
class MedicineReceiptType:
    name: str
    quantity: int
    price_per_unit: float
    total: float

@strawberry.type
class ReceiptType:
    appointment_id: int
    total_amount: float
    medicines: List[MedicineReceiptType]

@strawberry.type
class Query:
    @strawberry.field
    def medicines(self, info) -> List[MedicineType]:
        with get_db() as db:
            return [MedicineType(id=m.id, name=m.name, price=m.price, description=m.description) for m in db.query(models.Medicine).all()]

    @strawberry.field
    def getReceipt(self, info, appointmentId: int) -> ReceiptType:
        with get_db() as db:
            appointment_medicines = db.query(models.AppointmentMedicine).filter(
                models.AppointmentMedicine.appointment_id == appointmentId
            ).all()
            total_amount = 0
            medicines_list = []
            for am in appointment_medicines:
                medicine = db.query(models.Medicine).filter(models.Medicine.id == am.medicine_id).first()
                if medicine:
                    amount = medicine.price * am.quantity
                    total_amount += amount
                    medicines_list.append(MedicineReceiptType(
                        name=medicine.name,
                        quantity=am.quantity,
                        price_per_unit=medicine.price,
                        total=amount
                    ))
            return ReceiptType(
                appointment_id=appointmentId,
                total_amount=total_amount,
                medicines=medicines_list
            )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_medicine(self, name: str, price: float, description: str) -> MedicineType:
        with get_db() as db:
            db_medicine = models.Medicine(name=name, price=price, description=description)
            db.add(db_medicine)
            db.commit()
            db.refresh(db_medicine)
            return MedicineType(id=db_medicine.id, name=db_medicine.name, price=db_medicine.price, description=db_medicine.description)

    @strawberry.mutation
    def add_medicines_to_appointment(self, appointment_id: int, medicines: List[int], quantities: List[int]) -> bool:
        with get_db() as db:
            for medicine_id, quantity in zip(medicines, quantities):
                db_appointment_medicine = models.AppointmentMedicine(
                    appointment_id=appointment_id,
                    medicine_id=medicine_id,
                    quantity=quantity
                )
                db.add(db_appointment_medicine)
            db.commit()
        return True

from contextlib import contextmanager
@contextmanager
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

schema = strawberry.Schema(query=Query, mutation=Mutation)
from strawberry.fastapi import GraphQLRouter
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/appointments/{appointment_id}/receipt")
def get_receipt(appointment_id: int, db: Session = Depends(get_db)):
    appointment_medicines = db.query(models.AppointmentMedicine).filter(
        models.AppointmentMedicine.appointment_id == appointment_id
    ).all()
    
    total_amount = 0
    medicines_list = []
    
    for am in appointment_medicines:
        medicine = db.query(models.Medicine).filter(models.Medicine.id == am.medicine_id).first()
        if medicine:
            amount = medicine.price * am.quantity
            total_amount += amount
            medicines_list.append({
                "name": medicine.name,
                "quantity": am.quantity,
                "price_per_unit": medicine.price,
                "total": amount
            })
    
    return Receipt(
        appointment_id=appointment_id,
        total_amount=total_amount,
        medicines=medicines_list
    )