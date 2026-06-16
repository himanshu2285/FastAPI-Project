from fastapi import FastAPI, Path
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
def get_patient(patient_id: str):
    data = load_data()
    if patient_id in data:
        return {"patient": data[patient_id]}
    return {"error": "Patient not found"}