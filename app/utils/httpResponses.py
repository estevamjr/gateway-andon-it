from enum import IntEnum
from typing import Any, Optional, Tuple, Dict


class HttpStatus(IntEnum):
    # 1xx Informational
    CONTINUE = 100
    SWITCHING_PROTOCOLS = 101
    PROCESSING = 102
    EARLY_HINTS = 103

    # 2xx Success
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 226

    # 3xx Redirection
    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308

    # 4xx Client Error
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    TOO_EARLY = 425
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451

    # 5xx Server Error
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511


HTTP_MESSAGES: Dict[int, str] = {
    status.value: status.name.replace("_", " ").title() for status in HttpStatus
}


def send_response(
    status_code: int | HttpStatus,
    data: Optional[Any] = None,
    message: Optional[str] = None
) -> Tuple[Dict[str, Any], int]:
    """
    Retorno RFC 9110 estrito em formato de dicionário puro para o Flask-RESTful:
    { "status": "success|error", "code": <int>, "data|message": <content> }
    """
    code_val = int(status_code)
    default_msg = HTTP_MESSAGES.get(code_val, "Unknown Status")
    is_success = 100 <= code_val < 400

    payload: Dict[str, Any] = {
        "status": "success" if is_success else "error",
        "code": code_val
    }

    if is_success:
        payload["data"] = data if data is not None else {"message": message or default_msg}
    else:
        payload["message"] = message or default_msg

    return payload, code_val


# Helpers semânticos
def success_200(data=None, message=None): return send_response(HttpStatus.OK, data=data, message=message)
def success_201(data=None, message=None): return send_response(HttpStatus.CREATED, data=data, message=message)
def accepted_202(data=None, message=None): return send_response(HttpStatus.ACCEPTED, data=data, message=message)
def error_400(message="Bad Request"): return send_response(HttpStatus.BAD_REQUEST, message=message)
def bad_request_400(message="Bad Request"): return send_response(HttpStatus.BAD_REQUEST, message=message)
def error_401(message="Unauthorized access"): return send_response(HttpStatus.UNAUTHORIZED, message=message)
def error_404(message="Resource not found"): return send_response(HttpStatus.NOT_FOUND, message=message)
def error_409(message="Resource already exists"): return send_response(HttpStatus.CONFLICT, message=message)
def error_422(message="Unprocessable Entity"): return send_response(HttpStatus.UNPROCESSABLE_ENTITY, message=message)
def error_500(message="Internal Server Error"): return send_response(HttpStatus.INTERNAL_SERVER_ERROR, message=message)
def error_504(message="Gateway Timeout"): return send_response(HttpStatus.GATEWAY_TIMEOUT, message=message)