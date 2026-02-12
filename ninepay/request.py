"""
Payment request classes
"""

from typing import Optional
from ninepay.exceptions import ValidationException
from ninepay.enums import PaymentMethod, Currency, Language, TransactionType


class CreatePaymentRequest:
    """
    Payment request builder with fluent interface
    
    Required fields:
        - invoice_no: Unique invoice number
        - amount: Payment amount
        - description: Payment description
        - back_url: URL for cancel/back action
        - return_url: URL for successful payment return
    """
    
    def __init__(
        self,
        invoice_no: str,
        amount: str,
        description: str,
        back_url: str,
        return_url: str
    ):
        """
        Initialize payment request with required fields
        
        Args:
            invoice_no: Unique invoice number
            amount: Payment amount (as string)
            description: Payment description
            back_url: URL for cancel/back action
            return_url: URL for successful payment return
            
        Raises:
            ValidationException: If any required field is empty
        """
        if not invoice_no:
            raise ValidationException("invoice_no is required")
        if not amount:
            raise ValidationException("amount is required")
        if not description:
            raise ValidationException("description is required")
        if not back_url:
            raise ValidationException("back_url is required")
        if not return_url:
            raise ValidationException("return_url is required")
            
        self._data = {
            'invoiceNo': invoice_no,
            'amount': amount,
            'description': description,
            'backUrl': back_url,
            'returnUrl': return_url,
        }
    
    def with_method(self, method: str) -> 'CreatePaymentRequest':
        """Set payment method"""
        self._data['method'] = method
        return self
    
    def with_client_ip(self, client_ip: str) -> 'CreatePaymentRequest':
        """Set client IP address"""
        self._data['clientIp'] = client_ip
        return self
    
    def with_currency(self, currency: str) -> 'CreatePaymentRequest':
        """Set currency"""
        self._data['currency'] = currency
        return self
    
    def with_lang(self, lang: str) -> 'CreatePaymentRequest':
        """Set language"""
        self._data['lang'] = lang
        return self
    
    def with_transaction_type(self, transaction_type: str) -> 'CreatePaymentRequest':
        """Set transaction type"""
        self._data['transactionType'] = transaction_type
        return self
    
    def with_expires_time(self, minutes: int) -> 'CreatePaymentRequest':
        """Set expiration time in minutes"""
        self._data['expiresTime'] = minutes
        return self
    
    def with_custom_field(self, key: str, value: str) -> 'CreatePaymentRequest':
        """Add custom field to request"""
        self._data[key] = value
        return self
    
    def to_dict(self) -> dict:
        """
        Convert request to dictionary
        
        Returns:
            dict: Request data as dictionary
        """
        return self._data.copy()
    
    def __repr__(self):
        return f"CreatePaymentRequest(invoice_no='{self._data.get('invoiceNo')}')"
