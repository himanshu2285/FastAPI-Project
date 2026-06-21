from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description='City of the patient')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male','female','others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25 and self.bmi >= 18.5:
            return 'Normal'
        elif self.bmi < 30 and self.bmi >= 25:
            return 'Overweight'
        else:
            return 'Obese'

# Function to load patient data from a JSON file
def load_data():
    with open("patients.json","r") as f:
        data = json.load(f)
    return data

# Function to save the data into json
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data, f)
        

####### GET METHOD #######
@app.get("/")
def display():
    return {"message": "Patients Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API for managing patient records"}


@app.get("/patient")
def view_patients():
    data = load_data()
    return {"patients": data}


# Path Params: Path parameters are dynamic segments of a URL path used to identify a specific resources.
# Example: /patients/{patient_id} where {patient_id} is a path parameter that can be replaced with an actual patient ID to retrieve specific patient information.

# Path(): to provide additional validation and metadata for path parameters.

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient in DB", example="P001")):
    data = load_data()
    if patient_id in data:
        return {"patient": data[patient_id]}
    # return {"error": "Patient not found"}
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get('/sort')
def sort_patient(sort_by: str = Query(..., description='Sort on the basis of Height, Weight and BMI'),
                order: str = Query('asc', description='sort on asc or desc order')):
    valid_fields = ['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field, select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f'Invalid order select asc or desc order')
    
    data = load_data()
    
    sort_order = True if order=='desc' else False
    
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)
    
    return sorted_data


##### POST METHOD #####
@app.post('/create')
def create_patient(patient: Patient): # Data come from request body goes to pydantic model for validation
    # 1. load existing data
    data = load_data()
    
    # 2. check if the patient alredy exist
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exist')
    
    # 3. add new patient to the database
    # conerting pydantic data into from of dictionary
    data[patient.id] =  patient.model_dump(exclude=['id']) # Here is our python dictionary
    
    # save file from python dict to json file
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message:':'patient created successfully'})