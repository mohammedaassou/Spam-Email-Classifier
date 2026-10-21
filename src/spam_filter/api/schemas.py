
from pydantic import BaseModel, ValidationInfo, field_validator


class EmailRequestValidation(BaseModel):

    subject: str
    body: str

    @field_validator("subject", "body")

    @classmethod
    def not_empty(cls, value: str , info : ValidationInfo ) -> str:  


        value  = value.strip()

        if not value:
            raise ValueError(f"{info.field_name} cannot be empty")

        return value
