from fastapi import FastAPI
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


@app.get("/view")
def view():
    data = load_data()
    return {"patients": data}