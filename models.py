from pydantic import BaseModel


class SignUpSchema(BaseModel):
    email: str
    password: str
    username: str
    address: str

    class Config:
        schema_extra = {
            "example": {
                "email": "sample@gmail.com",
                "password": "samplepass123",
                "username": "hi",
                "address": "hi"
            }
        }


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "sample@gmail.com",
                "password": "samplepass123"
            }
        }

