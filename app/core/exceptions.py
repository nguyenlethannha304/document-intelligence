class OCRPlatformError(Exception):
    """Base exception for the OCR platform."""


class UnsupportedDocumentError(OCRPlatformError):
    """Raised when the uploaded document type is not supported."""