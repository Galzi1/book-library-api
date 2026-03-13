from fastapi import FastAPI

from seed import lifespan


app = FastAPI(title="Book Library API", lifespan=lifespan)
