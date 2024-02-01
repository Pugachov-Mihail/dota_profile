import uvicorn
from fastapi import FastAPI
from users.routers import users_routers


app = FastAPI()

app.include_router(users_routers.users_router)

# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port=8000)