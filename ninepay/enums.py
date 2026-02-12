"""
Enums and constants for 9Pay SDK
"""

from enum import Enum


class PaymentMethod:
    """Payment methods supported by 9Pay"""
    ATM_CARD = "ATM_CARD"
    CREDIT_CARD = "CREDIT_CARD"
    NINE_PAY = "9PAY"
    COLLECTION = "COLLECTION"
    APPLE_PAY = "APPLE_PAY"
    VNPAY_PORTONE = "vNPAY_PORTONE"
    ZALOPAY_WALLET = "ZALOPAY_WALLET"
    GOOGLE_PAY = "GOOGLE_PAY"
    QR_PAY = "QR_PAY"
    BUY_NOW_PAY_LATER = "BUY_NOW_PAY_LATER"


class Currency:
    """Supported currencies"""
    VND = "VND"
    USD = "USD"
    IDR = "IDR"
    EUR = "EUR"
    GBP = "GBP"
    CNY = "CNY"
    JPY = "JPY"
    AUD = "AUD"
    KRW = "KRW"
    CAD = "CAD"
    HKD = "HKD"
    INR = "INR"


class Language:
    """Supported languages"""
    VI = "vi"  # Vietnamese
    EN = "en"  # English


class TransactionType:
    """Transaction types"""
    INSTALLMENT = "INSTALLMENT"
    CARD_AUTHORIZATION = "CARD_AUTHORIZATION"


class Environment:
    """API Environments"""
    SANDBOX = "SANDBOX"
    PRODUCTION = "PRODUCTION"
    
    # API Endpoints
    ENDPOINTS = {
        SANDBOX: "https://sandbox.9pay.vn/payments",
        PRODUCTION: "https://api.9pay.vn/payments"
    }
    
    # Query Endpoints
    QUERY_ENDPOINTS = {
        SANDBOX: "https://sandbox.9pay.vn/payments/inquiry",
        PRODUCTION: "https://api.9pay.vn/payments/inquiry"
    }
    
    @classmethod
    def get_endpoint(cls, env: str) -> str:
        """Get payment endpoint for environment"""
        return cls.ENDPOINTS.get(env, cls.ENDPOINTS[cls.SANDBOX])
    
    @classmethod
    def get_query_endpoint(cls, env: str) -> str:
        """Get query endpoint for environment"""
        return cls.QUERY_ENDPOINTS.get(env, cls.QUERY_ENDPOINTS[cls.SANDBOX])
