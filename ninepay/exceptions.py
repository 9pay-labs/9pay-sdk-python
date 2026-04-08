"""
Custom exceptions for 9Pay SDK
"""


class PaymentException(Exception):
    """Base exception for payment-related errors"""
    pass


class ValidationException(Exception):
    """Exception for validation errors"""
    pass


class SignatureException(Exception):
    """Exception for signature verification errors"""
    pass


class APIException(PaymentException):
    """Exception for API communication errors"""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data
