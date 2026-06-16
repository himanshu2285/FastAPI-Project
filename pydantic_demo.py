# Pydantic: For type validation and data validation
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional

class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float
    married: Optional[bool] = False
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]


# def insert_patient_data(patient: Patient):
#     print(patient.name)
#     print(patient.age)
#     print(patient.weight)
#     print(patient.married)
#     print("Inserted into DB.")
    
def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print("Updated DB.")
    

patient_info = {"name":"Himanshu", "age":21, "email": "abc@gmail.com","weight": 55.5, "married":True, "allergies":["pollen", "dust"]
                , "contact_details":{"email":"abc@gmail.com", "Phone":"1234456"}}

patient1 = Patient(**patient_info)

# insert_patient_data(patient1)
update_patient_data(patient1) 