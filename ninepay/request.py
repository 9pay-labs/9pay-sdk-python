"""
Payment request classes
"""

import json
from typing import Optional, Dict, Any
from ninepay.exceptions import ValidationException
from ninepay.enums import PaymentMethod, Currency, Language, TransactionType


class AbstractRequest:
    """
    Base class for requests handling payload conversion
    """
    def __init__(self):
        self._data = {}

    def to_dict(self) -> dict:
        """
        Convert request parameters to array payload for API.
        Filters out None values.
        """
        return {k: v for k, v in self._data.items() if v is not None}


class CreatePaymentRequest(AbstractRequest):
    """
    Payment request builder with fluent interface
    """
    
    def __init__(
        self,
        invoice_no: str,
        amount: str,
        description: str,
        back_url: str,
        return_url: str
    ):
        super().__init__()
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
            'invoice_no': invoice_no,
            'amount': amount,
            'description': description,
            'back_url': back_url,
            'return_url': return_url,
        }
    
    def with_method(self, method: str) -> 'CreatePaymentRequest':
        self._data['method'] = method
        return self
    
    def with_client_ip(self, client_ip: str) -> 'CreatePaymentRequest':
        self._data['client_ip'] = client_ip
        return self
    
    def with_currency(self, currency: str) -> 'CreatePaymentRequest':
        self._data['currency'] = currency
        return self
    
    def with_lang(self, lang: str) -> 'CreatePaymentRequest':
        self._data['lang'] = lang
        return self
    
    def with_transaction_type(self, transaction_type: str) -> 'CreatePaymentRequest':
        self._data['transaction_type'] = transaction_type
        return self
    
    def with_expires_time(self, minutes: int) -> 'CreatePaymentRequest':
        self._data['expires_time'] = minutes
        return self
    
    def with_custom_field(self, key: str, value: str) -> 'CreatePaymentRequest':
        self._data[key] = value
        return self


class CreateRefundRequest(AbstractRequest):
    """
    Refund request data
    """
    def __init__(
        self,
        request_code: str,
        payment_no: int,
        amount: float,
        description: str
    ):
        super().__init__()
        if not all([request_code, payment_no, amount, description]):
            raise ValidationException("Missing required fields: request_code, payment_no, amount, description")
        if amount <= 0:
            raise ValidationException("Amount must be positive")
            
        self._data = {
            'request_id': request_code,
            'request_code': request_code, # PHP merged parent payload which has request_code
            'payment_no': str(payment_no),
            'amount': int(amount) if isinstance(amount, float) and amount.is_integer() else amount,
            'description': description
        }

    def with_currency(self, currency: str) -> 'CreateRefundRequest':
        self._data['currency'] = currency
        return self

    def with_bank(self, bank: str, account_no: str, account_name: str) -> 'CreateRefundRequest':
        self._data['bank'] = bank
        self._data['account_number'] = account_no
        self._data['customer_name'] = account_name
        return self


class PayerAuthRequest(AbstractRequest):
    """
    Payer authentication request data
    """
    def __init__(
        self,
        request_id: str,
        amount: float,
        return_url: str,
        currency: str = 'VND'
    ):
        super().__init__()
        if not all([request_id, amount, return_url]):
            raise ValidationException("Missing required fields")
        if len(request_id) > 30:
            raise ValidationException("request_id max length is 30")
        if amount < 3000000:
            raise ValidationException("Amount min is 3,000,000")
            
        self._data = {
            'request_id': request_id,
            'amount': amount,
            'return_url': return_url,
            'currency': currency
        }

    def with_installment(self, amount: float, bank_code: str, period: int = 12) -> 'PayerAuthRequest':
        self._data['installment'] = {
            'amount_original': amount,
            'bank_code': bank_code,
            'period': period
        }
        return self

    def with_card(self, card_number: str, hold_name: str, exp_month: int, exp_year: int, cvv: str) -> 'PayerAuthRequest':
        self._data['card'] = {
            'card_number': card_number,
            'hold_name': hold_name,
            'exp_month': exp_month,
            'exp_year': exp_year,
            'cvv': cvv
        }
        return self


class AuthorizeCardPaymentRequest(AbstractRequest):
    """
    Card authorization request data
    """
    def __init__(
        self,
        request_id: str,
        order_code: int,
        amount: float,
        currency: str = 'VND'
    ):
        super().__init__()
        if not all([request_id, order_code, amount, currency]):
            raise ValidationException("Missing required fields")
        if len(request_id) > 30:
            raise ValidationException("request_id max length is 30")
            
        self._data = {
            'request_id': request_id,
            'order_code': order_code,
            'amount': amount,
            'currency': currency
        }

    def with_card(self, card_number: str, hold_name: str, exp_month: int, exp_year: int, cvv: str) -> 'AuthorizeCardPaymentRequest':
        self._data['card'] = {
            'card_number': card_number,
            'hold_name': hold_name,
            'exp_month': exp_month,
            'exp_year': exp_year,
            'cvv': cvv
        }
        return self


class ReverseCardPaymentRequest(AbstractRequest):
    """
    Reverse card payment request data
    """
    def __init__(
        self,
        request_id: str,
        order_code: int
    ):
        super().__init__()
        if not all([request_id, order_code]):
            raise ValidationException("Missing required fields")
        if len(request_id) > 30:
            raise ValidationException("request_id max length is 30")
            
        self._data = {
            'request_id': request_id,
            'order_code': order_code
        }


class CapturePaymentRequest(AbstractRequest):
    """
    Capture payment request data
    """
    def __init__(
        self,
        request_id: str,
        order_code: int,
        amount: float,
        currency: str = 'VND'
    ):
        super().__init__()
        if not all([request_id, order_code, amount, currency]):
            raise ValidationException("Missing required fields")
        if len(request_id) > 30:
            raise ValidationException("request_id max length is 30")
        if amount <= 0:
            raise ValidationException("Amount must be positive")
            
        self._data = {
            'request_id': request_id,
            'order_code': order_code,
            'amount': amount,
            'currency': currency
        }
