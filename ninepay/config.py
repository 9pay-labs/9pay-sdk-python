"""
Configuration management for 9Pay SDK
"""

import os
from typing import Optional


class NinePayConfig:
    """
    Configuration for 9Pay SDK
    
    Attributes:
        merchant_id (str): Your merchant ID from 9Pay
        secret_key (str): Your secret key for API authentication
        checksum_key (str): Your checksum key for signature verification
        env (str): Environment - 'SANDBOX' or 'PRODUCTION'
        endpoint (str, optional): Custom base API endpoint URL
    """
    
    def __init__(self, merchant_id: str, secret_key: str, checksum_key: str, 
                 env: str = 'SANDBOX', endpoint: str = None):
        """
        Initialize 9Pay configuration
        """
        if not merchant_id:
            raise ValueError("merchant_id is required")
        if not secret_key:
            raise ValueError("secret_key is required")
        if not checksum_key:
            raise ValueError("checksum_key is required")
        if env not in ['SANDBOX', 'PRODUCTION']:
            raise ValueError("env must be 'SANDBOX' or 'PRODUCTION'")
            
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.checksum_key = checksum_key
        self.env = env
        self.endpoint = endpoint
    
    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(
            merchant_id=config_dict.get('merchant_id', ''),
            secret_key=config_dict.get('secret_key', ''),
            checksum_key=config_dict.get('checksum_key', ''),
            env=config_dict.get('env', 'SANDBOX'),
            endpoint=config_dict.get('endpoint')
        )
    
    @classmethod
    def from_env(cls, env_file: Optional[str] = None):
        if env_file is not False:
            try:
                from dotenv import load_dotenv
                if env_file:
                    load_dotenv(env_file)
                else:
                    load_dotenv()
            except ImportError:
                pass
        
        return cls(
            merchant_id=os.getenv('NINEPAY_MERCHANT_ID', ''),
            secret_key=os.getenv('NINEPAY_SECRET_KEY', ''),
            checksum_key=os.getenv('NINEPAY_CHECKSUM_KEY', ''),
            env=os.getenv('NINEPAY_ENV', 'SANDBOX'),
            endpoint=os.getenv('NINEPAY_ENDPOINT')
        )
    
    def to_dict(self) -> dict:
        return {
            'merchant_id': self.merchant_id,
            'secret_key': self.secret_key,
            'checksum_key': self.checksum_key,
            'env': self.env,
            'endpoint': self.endpoint
        }
    
    def __repr__(self):
        return f"NinePayConfig(merchant_id='{self.merchant_id}', env='{self.env}')"
