"""
Response classes for API responses
"""

from typing import Optional, Any


class BasicResponse:
    """
    Basic response wrapper for API responses
    
    Attributes:
        success (bool): Whether the request was successful
        message (str): Response message
        data (dict): Response data
        error_code (str): Error code if failed
    """
    
    def __init__(
        self,
        success: bool,
        message: str = "",
        data: Optional[dict] = None,
        error_code: Optional[str] = None
    ):
        """
        Initialize response
        
        Args:
            success: Whether the request was successful
            message: Response message
            data: Response data dictionary
            error_code: Error code if failed
        """
        self.success = success
        self.message = message
        self.data = data or {}
        self.error_code = error_code
    
    def is_success(self) -> bool:
        """Check if response is successful"""
        return self.success
    
    def get_message(self) -> str:
        """Get response message"""
        return self.message
    
    def get_data(self) -> dict:
        """Get response data"""
        return self.data
    
    def get_error_code(self) -> Optional[str]:
        """Get error code"""
        return self.error_code
    
    @classmethod
    def success_response(cls, data: dict, message: str = "Success") -> 'BasicResponse':
        """
        Create successful response
        
        Args:
            data: Response data
            message: Success message
            
        Returns:
            BasicResponse: Success response instance
        """
        return cls(success=True, message=message, data=data)
    
    @classmethod
    def error_response(cls, message: str, error_code: Optional[str] = None) -> 'BasicResponse':
        """
        Create error response
        
        Args:
            message: Error message
            error_code: Error code
            
        Returns:
            BasicResponse: Error response instance
        """
        return cls(success=False, message=message, error_code=error_code)
    
    def to_dict(self) -> dict:
        """Convert response to dictionary"""
        return {
            'success': self.success,
            'message': self.message,
            'data': self.data,
            'error_code': self.error_code
        }
    
    def __repr__(self):
        status = "Success" if self.success else "Error"
        return f"BasicResponse({status}: {self.message})"
