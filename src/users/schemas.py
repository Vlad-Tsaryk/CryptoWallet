import re
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, EmailStr, validator, Field

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]+$")


class UserBase(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_image: Optional[dict] = None


class UserOut(UserBase):
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True


# class UserIn(UserBase):
#     profile_image: UploadFile | None = None
#     password: str | None = Field(min_length=8,
#                                  max_length=20,
#                                  regex=STRONG_PASSWORD_PATTERN, default=None)
#     password_repeat: str | None
#
#     @validator('password_repeat')
#     def passwords_match(cls, v, values, **kwargs):
#         if v and 'password' in values:
#             if v != values['password']:
#                 raise ValueError('passwords do not match')
#         return v
#
#     @validator('profile_image')
#     def check_image(cls, v, values, **kwargs):
#         if v:
#             try:
#                 v = Image.open(v.file)
#                 v.close()
#             except IOError:
#                 raise ValueError('File is not image')
#         return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = True


class UserRegistration(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str = Field(min_length=8, max_length=20)
    password_repeat: str

    @validator("password")
    def valid_password(cls, password: str) -> str:
        if password and not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character "
            )

        return password

    @validator("password_repeat")
    def passwords_match(cls, password: str, values):
        if password and "password" in values and password != values["password"]:
            raise ValueError("Password do not match")
        return password


class UserUpdate(UserRegistration):
    email: None = None
    profile_image: UploadFile | None = None
    password: str | None = Field(min_length=8, max_length=20, default=None)
    password_repeat: str | None


class UserResponse(UserBase):
    id: int
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True
