from fastapi import Request, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import traceback
from app.utils.exceptions import CustomException

# === HANDLERS ===

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def unhandled_exception_handler(request: Request, exc: str):
    print(traceback.format_exc())  # ou log via logging
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Une erreur interne est survenue : {exc}"},
    )

async def not_found_handler(request: Request, exc: str):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Not Found : {exc}"},
    )

async def forbidden_handler(request: Request, exc: str):
    return JSONResponse(
        status_code=403,
        content={"detail": f"Forbidden : {exc}"},
    )

async def bad_request_handler(request: Request, exc: str):
    return JSONResponse(
        status_code=400,
        content={"detail": f"Bad Request : {exc}"},
    )

async def already_exists_handler(request: Request, exc: str):
    return JSONResponse(
        status_code=409,
        content={"detail": f"Already Exists : {exc}"},
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 400:
        return await bad_request_handler(request, exc.detail)
    elif exc.status_code == 404:
        return await not_found_handler(request, exc.detail)
    elif exc.status_code == 409:
        return await already_exists_handler(request, exc.detail)
    elif exc.status_code == 403:
        return await forbidden_handler(request, exc.detail)
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": f"{exc.status_code} Error : {exc.detail}"}
        )



# === ENREGISTREMENT AUTOMATIQUE ===

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
