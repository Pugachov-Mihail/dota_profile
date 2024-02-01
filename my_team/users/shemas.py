from pydantic import BaseModel


class User(BaseModel):
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreateProfile(BaseModel):
    email: str


class DotaProfileUser(BaseModel):
    account_id: int

    class Config:
        from_attributes = True


class DotaProfileCreate(BaseModel):
    account_id: DotaProfileUser
    email: UserCreateProfile


class UserProfile(BaseModel):
    account_id: DotaProfileUser

    class Config:
        from_attributes = True
