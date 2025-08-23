from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import firebase_admin
import logging
from firebase_admin import credentials
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from common.exception_handlers import global_exception_handler, validation_exception_handler, http_exception_handler

from endpoints import login, register, example, google_login, profile
from endpoints.generate import instant

cred = credentials.Certificate("firebase-service-account.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)



# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("franjojo_backend")

app = FastAPI()

# Allow all CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

# Include routers
app.include_router(login.router)
app.include_router(google_login.router)
app.include_router(register.router)
app.include_router(example.router)
app.include_router(profile.router)
app.include_router(instant.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)