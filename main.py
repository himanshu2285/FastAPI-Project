from fastapi import FastAPI, HTTPException, Path, Query
import json

app = FastAPI()

# Function to load patient data from a JSON file
def load_data():
    with open("patients.json","r") as f:
        data = json.load(f)
    return data

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