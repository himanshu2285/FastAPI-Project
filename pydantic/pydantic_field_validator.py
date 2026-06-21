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
    # field validator type -> Before, After 
    # (Before: validation will be before type casting, After: First typecasting then validation)
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        
        valid_domains = ['hdfc.com', 'icici.com'] # we only pass the email which are corporate
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError("Not a valid domain")
        
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode='after') #by_default: after
    @classmethod
    def validate_age(cls, value):
        if 0<value<=100:
            return value
        else:
            raise ValueError("Age should be in between 0 and 100")
    
     


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
        