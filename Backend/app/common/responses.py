from typing import Any
from fastapi.responses import JSONResponse

class APIResponse:
    """
    Standard Response Factory.
    Enforces a strict client contract for both success and error responses.
    """

    @staticmethod
    def success(message: str, data: Any = None, status_code: int = 200) -> JSONResponse:
        """
        Builds a standard success APIResponse.
        """
        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "data": data
            }
        )

    @staticmethod
    def error(message: str, error_code: str, status_code: int = 400, data: Any = None) -> JSONResponse:
        """
        Builds a standard failure APIResponse.
        """
        content = {
            "success": False,
            "message": message,
            "errorCode": error_code
        }
        if data is not None:
            content["data"] = data
        return JSONResponse(
            status_code=status_code,
            content=content
        )
