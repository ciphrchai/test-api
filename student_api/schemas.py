from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(gt=0, le=150)
    email: EmailStr | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        name = value.strip()
        if not name:
            raise ValueError("Name must not be blank.")
        return name


class StudentRead(StudentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
