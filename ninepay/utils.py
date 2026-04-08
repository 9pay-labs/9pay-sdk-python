"""
Utility functions for signature generation and verification
"""

import hmac
import hashlib
import base64
from typing import Union


class Signature:
    """
    Signature utility for generating and verifying HMAC signatures
    Uses HMAC-SHA256 with base64 encoding
    """
    
    @staticmethod
    def generate(data: str, secret_key: str) -> str:
        """
        Generate HMAC-SHA256 signature
        
        Args:
            data: Data to sign
            secret_key: Secret key for signing
            
        Returns:
            str: Base64 encoded signature
            
        Example:
            >>> signature = Signature.generate("data_to_sign", "secret_key")
        """
        # Create HMAC-SHA256 hash with binary output
        signature_bytes = hmac.new(
            secret_key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        # Base64 encode the binary signature
        return base64.b64encode(signature_bytes).decode('utf-8')
    
    @staticmethod
    def verify(data: str, signature: str, secret_key: str) -> bool:
        """
        Verify HMAC-SHA256 signature
        
        Args:
            data: Original data
            signature: Signature to verify
            secret_key: Secret key used for signing
            
        Returns:
            bool: True if signature is valid, False otherwise
            
        Example:
            >>> is_valid = Signature.verify("data", "signature", "secret_key")
        """
        expected_signature = Signature.generate(data, secret_key)
        return hmac.compare_digest(signature, expected_signature)
