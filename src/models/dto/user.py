from fastapi_users import schemas


class GetUser(schemas.BaseUser[int]):
    pass


class CreateUser(schemas.BaseUserCreate):
    pass


class UpdateUser(schemas.BaseUserUpdate):
    pass
