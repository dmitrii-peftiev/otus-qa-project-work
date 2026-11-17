from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


class SingleUserResponse(BaseModel):
    data: UserData


class UsersListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[UserData]


class CreateUserResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: str


class UpdateUserResponse(BaseModel):
    name: str | None = None
    job: str | None = None
    updatedAt: str


class RegisterSuccessResponse(BaseModel):
    id: int
    token: str


class LoginSuccessResponse(BaseModel):
    token: str


class ErrorResponse(BaseModel):
    error: str


class ResourceData(BaseModel):
    id: int
    name: str
    year: int
    color: str
    pantone_value: str


class SingleResourceResponse(BaseModel):
    data: ResourceData


class ResourcesListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[ResourceData]
