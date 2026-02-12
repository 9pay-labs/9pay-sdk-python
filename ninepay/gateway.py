"""
9Pay Payment Gateway implementation
"""

import json
import base64
import requests
from typing import Optional, Dict, Any
from urllib.parse import urlencode

from ninepay.config import NinePayConfig
from ninepay.request import CreatePaymentRequest
from ninepay.response import BasicResponse
from ninepay.utils import Signature
from ninepay.enums import Environment
from ninepay.exceptions import PaymentException, APIException, SignatureException


class NinePayGateway:
    """
    Main gateway class for interacting with 9Pay Payment API
    
    Handles:
    - Creating payment requests
    - Querying transaction status
    - Verifying webhook/callback signatures
    """
    
    def __init__(self, config: NinePayConfig):
        """
        Initialize gateway with configuration
        
        Args:
            config: NinePayConfig instance with credentials
        """
        self.config = config
        self.payment_endpoint = Environment.get_endpoint(config.env)
        self.query_endpoint = Environment.get_query_endpoint(config.env)
    
    def create_payment(self, request: CreatePaymentRequest) -> BasicResponse:
        """
        Create a payment request and get redirect URL
        
        Args:
            request: CreatePaymentRequest instance with payment details
            
        Returns:
            BasicResponse: Response containing redirect_url in data
            
        Raises:
            PaymentException: If payment creation fails
            
        Example:
            >>> request = CreatePaymentRequest(
            ...     invoice_no="INV_123",
            ...     amount="50000",
            ...     description="Payment for order",
            ...     back_url="https://site.com/cancel",
            ...     return_url="https://site.com/success"
            ... )
            >>> response = gateway.create_payment(request)
            >>> if response.is_success():
            ...     redirect_url = response.get_data()['redirect_url']
        """
        try:
            # Get request data
            payment_data = request.to_dict()
            
            # Add merchant ID
            payment_data['merchantId'] = self.config.merchant_id
            
            # Convert to JSON and encode
            json_data = json.dumps(payment_data, separators=(',', ':'), ensure_ascii=False)
            encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
            
            # Generate signature
            signature = Signature.generate(encoded_data, self.config.secret_key)
            
            # Prepare request payload
            payload = {
                'baseEncode': encoded_data,
                'signature': signature
            }
            
            # Send request to API
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            response = requests.post(
                self.payment_endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            # Parse response
            if response.status_code == 200:
                result = response.json()
                
                if result.get('status') == 'success' or result.get('errorCode') == '00':
                    return BasicResponse.success_response(
                        data=result.get('data', {}),
                        message=result.get('message', 'Payment created successfully')
                    )
                else:
                    return BasicResponse.error_response(
                        message=result.get('message', 'Payment creation failed'),
                        error_code=result.get('errorCode')
                    )
            else:
                raise APIException(
                    f"API request failed with status {response.status_code}",
                    status_code=response.status_code,
                    response_data=response.text
                )
                
        except requests.RequestException as e:
            raise PaymentException(f"Network error: {str(e)}")
        except Exception as e:
            raise PaymentException(f"Payment creation error: {str(e)}")
    
    def inquiry(self, invoice_no: str) -> BasicResponse:
        """
        Query transaction status by invoice number
        
        Args:
            invoice_no: Invoice number to query
            
        Returns:
            BasicResponse: Response containing transaction details
            
        Raises:
            PaymentException: If query fails
            
        Example:
            >>> response = gateway.inquiry("INV_123")
            >>> if response.is_success():
            ...     status = response.get_data()['status']
        """
        try:
            # Prepare query data
            query_data = {
                'merchantId': self.config.merchant_id,
                'invoiceNo': invoice_no
            }
            
            # Convert to JSON and encode
            json_data = json.dumps(query_data, separators=(',', ':'), ensure_ascii=False)
            encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
            
            # Generate signature
            signature = Signature.generate(encoded_data, self.config.secret_key)
            
            # Prepare request payload
            payload = {
                'baseEncode': encoded_data,
                'signature': signature
            }
            
            # Send request
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            response = requests.post(
                self.query_endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            # Parse response
            if response.status_code == 200:
                result = response.json()
                
                if result.get('status') == 'success' or result.get('errorCode') == '00':
                    return BasicResponse.success_response(
                        data=result.get('data', {}),
                        message=result.get('message', 'Query successful')
                    )
                else:
                    return BasicResponse.error_response(
                        message=result.get('message', 'Query failed'),
                        error_code=result.get('errorCode')
                    )
            else:
                raise APIException(
                    f"API request failed with status {response.status_code}",
                    status_code=response.status_code,
                    response_data=response.text
                )
                
        except requests.RequestException as e:
            raise PaymentException(f"Network error: {str(e)}")
        except Exception as e:
            raise PaymentException(f"Query error: {str(e)}")
    
    def verify(self, result: str, checksum: str) -> bool:
        """
        Verify webhook/callback signature
        
        Args:
            result: Base64 encoded result data from callback
            checksum: Checksum signature from callback
            
        Returns:
            bool: True if signature is valid, False otherwise
            
        Example:
            >>> # From webhook POST data
            >>> result = request.form.get('result')
            >>> checksum = request.form.get('checksum')
            >>> if gateway.verify(result, checksum):
            ...     # Process payment
            ...     data = gateway.decode_result(result)
        """
        try:
            return Signature.verify(result, checksum, self.config.checksum_key)
        except Exception:
            return False
    
    def decode_result(self, result: str) -> str:
        """
        Decode base64 encoded result from callback
        
        Args:
            result: Base64 encoded result string
            
        Returns:
            str: Decoded JSON string
            
        Example:
            >>> decoded = gateway.decode_result(result)
            >>> data = json.loads(decoded)
            >>> invoice_no = data['invoice_no']
            >>> status = data['status']
        """
        try:
            decoded_bytes = base64.b64decode(result)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            raise PaymentException(f"Failed to decode result: {str(e)}")
    
    def __repr__(self):
        return f"NinePayGateway(merchant_id='{self.config.merchant_id}', env='{self.config.env}')"
