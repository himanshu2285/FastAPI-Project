# Pydantic: For type validation and data validation
from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    # name: str = Field(max_length=50)  # Field() also helps in adding Metadata, custom data validation, default values
    name: str = Annotated[str, Field(max_length=50, title="Name of patients", description="Give the name of patient less than 50 char")]
    age: int = Field(gt=0, lt=120)
    email: EmailStr
    weight: Annotated[float, Field(gt=0, strict=True)] # Strict don't allow pydantic for type conversion
    married: Optional[bool] = Annotated[bool, Field(default=None, description="Is person married?")]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=10)]
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
    

patient_info = {"name":"Himanshu", "age":"21", "email": "abc@gmail.com","weight": 55.5, "married":True, 
                "allergies":["pollen", "dust"], 
                "contact_details":{"email":"abc@gmail.com", "Phone":"1234456"}}

patient1 = Patient(**patient_info)

# insert_patient_data(patient1)
update_patient_data(patient1) 