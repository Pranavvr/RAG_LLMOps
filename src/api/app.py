from __future__ import annotations


# from fastapi import FastAPI
# from src.api.routes import router
# from src.config.logging import setup_logging

# setup_logging()


# app = FastAPI(title = "Smart Investor Agent")

# app.include_router(router)


from fastapi import FastAPI

from src.config.logging import setup_logging
from src.api.routes import router

setup_logging()

app = FastAPI(title="smart-investor-agent", version="0.1.0")
app.include_router(router)
