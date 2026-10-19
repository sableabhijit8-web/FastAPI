
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
    computed_field
)
from typing import List, Optional, Annotated


class Patient(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr
    age: int = Field(gt=0, lt=100)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Optional[bool] = None
    allergies: Optional[List[str]] = Field(default=None, max_length=5)
    contact_details: dict[str, str]
    height: float

    @field_validator("email")
    @classmethod
    def email_name(cls, value):
        allowed_domains = ["hdfc.com", "icici.com"]
        domain_name = value.split("@")[1].lower()

        if domain_name not in allowed_domains:
            raise ValueError("Invalid email domain")

        return value

    @field_validator("name")
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @model_validator(mode="after")
    def validate_emergency_contact(self):
        if self.age > 60 and not self.contact_details:
            raise ValueError(
                "Emergency contact details are required for patients over 60."
            )
        return self
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi =  round(self.weight / (self.height ** 2), 2)
        return bmi


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(f"Patient's BMI: {patient.bmi}")
    print("Patient data inserted successfully.")


patient_info = {
    "name": "Abhi",
    "email": "abcd@hdfc.com",
    "age": 70,
    "weight": 55.1,
    "married": False,
    "allergies": ["dust", "pollen"],
    "contact_details": {
        "email": "abcd2@example.com",
        "phone": "1234567890",
    },
    "height": 1.75
}

patient1 = Patient(**patient_info)
insert_patient_data(patient1)
