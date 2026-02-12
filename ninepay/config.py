"""
Configuration class for 9Pay SDK
"""
import os
from typing import Optional


class NinePayConfig:
    """
    Configuration for 9Pay Payment Gateway
    
    Attributes:
        merchant_id (str): Your merchant ID from 9Pay
        secret_key (str): Your secret key for API authentication
        checksum_key (str): Your checksum key for signature verification
        env (str): Environment - 'SANDBOX' or 'PRODUCTION'
    """
    
    def __init__(self, merchant_id: str, secret_key: str, checksum_key: str, env: str = 'SANDBOX'):
        """
        Initialize 9Pay configuration
        
        Args:
            merchant_id: Your merchant ID from 9Pay
            secret_key: Your secret key for API authentication
            checksum_key: Your checksum key for signature verification
            env: Environment - 'SANDBOX' or 'PRODUCTION' (default: 'SANDBOX')
            
        Raises:
            ValueError: If any required parameter is empty or env is invalid
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
    
    @classmethod
    def from_dict(cls, config_dict: dict):
        """
        Create configuration from dictionary
        
        Args:
            config_dict: Dictionary containing configuration keys
            
        Returns:
            NinePayConfig: Configuration instance
            
        Example:
            >>> config = NinePayConfig.from_dict({
            ...     'merchant_id': 'YOUR_MERCHANT_ID',
            ...     'secret_key': 'YOUR_SECRET_KEY',
            ...     'checksum_key': 'YOUR_CHECKSUM_KEY',
            ...     'env': 'SANDBOX'
            ... })
        """
        return cls(
            merchant_id=config_dict.get('merchant_id', ''),
            secret_key=config_dict.get('secret_key', ''),
            checksum_key=config_dict.get('checksum_key', ''),
            env=config_dict.get('env', 'SANDBOX')
        )
    
    @classmethod
    def from_env(cls, env_file: Optional[str] = None):
        """
        Create configuration from environment variables or .env file
        
        This method loads configuration from:
        1. A .env file (if env_file is specified or .env exists in current directory)
        2. System environment variables
        
        Args:
            env_file: Optional path to .env file. If not specified, looks for .env in current directory
            
        Returns:
            NinePayConfig: Configuration instance
            
        Environment variables:
            NINEPAY_MERCHANT_ID: Your merchant ID from 9Pay
            NINEPAY_SECRET_KEY: Your secret key for API authentication
            NINEPAY_CHECKSUM_KEY: Your checksum key for signature verification
            NINEPAY_ENV: Environment - 'SANDBOX' or 'PRODUCTION' (default: 'SANDBOX')
            
        Example:
            >>> # Load from .env file in current directory
            >>> config = NinePayConfig.from_env()
            
            >>> # Load from specific .env file
            >>> config = NinePayConfig.from_env('/path/to/.env')
            
            >>> # Load from system environment variables only
            >>> config = NinePayConfig.from_env(env_file=False)
        """
        # Try to load from .env file
        if env_file is not False:
            try:
                from dotenv import load_dotenv
                if env_file:
                    load_dotenv(env_file)
                else:
                    load_dotenv()  # Load from .env in current directory
            except ImportError:
                # python-dotenv not installed, fall back to system env vars
                pass
        
        return cls(
            merchant_id=os.getenv('NINEPAY_MERCHANT_ID', ''),
            secret_key=os.getenv('NINEPAY_SECRET_KEY', ''),
            checksum_key=os.getenv('NINEPAY_CHECKSUM_KEY', ''),
            env=os.getenv('NINEPAY_ENV', 'SANDBOX')
        )
    
    def to_dict(self) -> dict:
        """
        Convert configuration to dictionary
        
        Returns:
            dict: Configuration as dictionary
        """
        return {
            'merchant_id': self.merchant_id,
            'secret_key': self.secret_key,
            'checksum_key': self.checksum_key,
            'env': self.env
        }
    
    def __repr__(self):
        return f"NinePayConfig(merchant_id='{self.merchant_id}', env='{self.env}')"
