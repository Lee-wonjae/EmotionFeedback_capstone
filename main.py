from fastapi import FastAPI
from api.routers import byProfile,byScenario,postVideo
from dotenv import load_dotenv


load_dotenv()

app=FastAPI()
app.include_router(byProfile.router)
app.include_router(byScenario.router)
app.include_router(postVideo.router)