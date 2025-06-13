
class AppBaseError(Exception):
    """Base class for custom exceptions."""
    def __init__(self, message="An unexpected application error occurred."):
        super().__init__(message)


class ProcessingError(AppBaseError):
    """Raised when a processing step fails (e.g., PDF, audio, summarization)."""
    def __init__(self, message="Processing failed. Please check the input and try again."):
        super().__init__(message)


class ResourceNotFoundError(AppBaseError):
    """Raised when an expected file or resource is missing."""
    def __init__(self, message="Requested resource was not found."):
        super().__init__(message)
