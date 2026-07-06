class OCRPlatformError(Exception):
    """Base exception for the OCR platform."""


class UnsupportedDocumentError(OCRPlatformError):
    """Raised when the uploaded document type is not supported."""

class ScannedPageError(ValueError):
    """Raised when a page is scanned/image-only or contains embedded images.

    Catch this specifically to route the file to an OCR pipeline.
    """