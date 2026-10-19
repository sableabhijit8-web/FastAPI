from pydantic import BaseModel

class Address(BaseModel):
    
    city: str
    state: str
    pin: str
    

class Patient(BaseModel):
    
    name: str
    gender: str
    age: int
    address: Address
    
address_dict  = {
    "city": "Jalna",
    "state": "Maharashtra",
    "pin": "431211"
}

address1 = Address(**address_dict)

patient_dict  = {
    "name": "Abhijit",
    "gender": "Male",
    "age": 20,
    "address": address1
}

patient1  = Patient(**patient_dict)

print(patient1.name)
print(patient1.gender)
print(patient1.age)
print(patient1.address.city)
print(patient1.address.state)
print(patient1.address.pin)

temp  = patient1.model_dump()
# temp  = patient1.model_dump_json()

temp  = patient1.model_dump(include=["name", "gender"])
temp  = patient1.model_dump(exclude=["age"])
temp  = patient1.model_dump(exclude={'address': ['state']})




print(temp)
print(type(temp))