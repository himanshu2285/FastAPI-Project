# Model Validator
# Here what we're going to do: if age is greater than 60, there should be an amergency contact details

from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Annotated, Optional

class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    
    @model_validator(mode='after')
    def validate_emergency_details(cls, model):
        if model.age > 60 and 'Emergency' not in model.contact_details:
            raise ValueError("Patient older than 60 must have Emergency contacts")
        return model
    
    
def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print("Updated DB.")
    

patient_info = {"name":"Himanshu", "age":"66", "email": "abc@gmail.com","weight": 55.5, "married":True, 
                "allergies":["pollen", "dust"], 
                "contact_details":{"Phone":"1234456", "Emergency":"123456"}}


patient1 = Patient(**patient_info)

update_patient_data(patient1) 