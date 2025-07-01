import logging

logger = logging.getLogger(__name__)

class CustomException(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
