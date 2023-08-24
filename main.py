from fastapi import Depends, FastAPI, Request, status
import models
from database import engine
from routers import auth, todos, users
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request, user = Depends(auth.get_current_user)):
    if not user:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
