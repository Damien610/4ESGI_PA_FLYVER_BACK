from fastapi import Request, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import traceback

from app.crud.exception import NotFound, BadRequest, AlreadyExist, CustomException,NotAuthorized


# === HANDLERS ===

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    print(traceback.format_exc())
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Une erreur interne est survenue : {str(exc)}"},
    )


async def not_found_exception_handler(request: Request, exc: NotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


async def forbidden_handler(request: Request, exc: NotAuthorized):
    return JSONResponse(
        status_code=403,
        content={"detail": f"Forbidden : {str(exc)}"},
    )


async def bad_request_handler(request: Request, exc: BadRequest):
    return JSONResponse(
        status_code=400,
        content={"detail": f"Bad Request : {str(exc)}"},
    )


async def already_exists_handler(request: Request, exc: AlreadyExist):
    return JSONResponse(
        status_code=409,
        content={"detail": f"Already Exists : {str(exc)}"},
    )


async def http_exception_handler(request: Request, exc: HTTPException):

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": f"{exc.status_code} Error : {exc.detail}"}
        )


# === ENREGISTREMENT AUTOMATIQUE ===

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(NotFound, not_found_exception_handler)
    app.add_exception_handler(BadRequest, bad_request_handler)
    app.add_exception_handler(AlreadyExist, already_exists_handler)
