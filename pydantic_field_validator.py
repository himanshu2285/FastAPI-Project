# Pydantic model for custom field validation

from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Annotated, Optional

class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    
    # 1st use case: For specific email
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        
        valid_domains = ['hdfc.com', 'icici.com'] # we only pass the email which are corporate
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError("Not a valid domain")
        
        return value
    
    @field_validator('name')
    @staticmethod
    def transform_name(cls, value):
        return value.upper()
     

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print("Inserted into DB.")
    
patient_info = {"name":"Himanshu", "age":"21", "email": "abc@hdfc.com","weight": 55.5, "married":True, 
                "allergies":["pollen", "dust"], 
                "contact_details":{"email":"abc@gmail.com", "Phone":"1234456"}}


patient1 = Patient(**patient_info)

insert_patient_data(patient1)
        