
from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field 
from typing import List, Optional, Annotated
from fastapi.responses import JSONResponse

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="Abhijeet Sable")]
    age: Annotated[int, Field(..., description="The age of the patient", example=20)]
    height: Annotated[float, Field(..., description="The height of the patient in meters", example=1.75)]
    weight: Annotated[float, Field(..., description="The weight of the patient in kilograms", example=70.5)]

    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obese"

class Patientupdate(BaseModel):
    id: Annotated[Optional[str], Field(description="The ID of the patient", example="P001")] = None
    name: Annotated[Optional[str], Field(description="The name of the patient", example="Abhijeet Sable")] = None
    age: Annotated[Optional[int], Field(description="The age of the patient", example=20)] = None
    height: Annotated[Optional[float], Field(description="The height of the patient in meters", example=1.75)] = None
    weight: Annotated[Optional[float], Field(description="The weight of the patient in kilograms", example=70.5)] = None
    
    
def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data


def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)
        
@app.get("/")
def hello():
    return {"message": "Patient management system API"}

@app.get('/about')
def about():
    return {"message": "A fully functional patient management system API built using FastAPI.)"}

@app.get('/view')
def view():
    data = load_data()
    
    return data
# find a individual patient by id
@app.get ('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve",example="P001")):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    
    #load existing data
    data  = load_data()
    
    # /check if patient id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    
    #add new patient data
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    # save into the json file
    save_data(data)
    
    return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient_id": patient.id}) 

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: Patientupdate):
    
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info  = data[patient_id]
            
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key ,value in updated_patient_info.items():
        existing_patient_info[key] = value

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})       