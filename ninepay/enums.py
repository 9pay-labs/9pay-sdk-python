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
    
    # Base Endpoints
    # We can override these via NINEPAY_ENDPOINT environment variable
    BASE_URLS = {
        SANDBOX: "",
        PRODUCTION: ""
    }
    
    @classmethod
    def get_endpoint(cls, env: str) -> str:
        """Get base API endpoint for environment"""
        import os
        env_url = os.getenv('NINEPAY_ENDPOINT')
        if env_url:
            return env_url.rstrip('/')
        return cls.BASE_URLS.get(env, cls.BASE_URLS[cls.SANDBOX])
