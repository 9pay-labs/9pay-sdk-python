import json
import base64
import requests
import time
import hmac
import hashlib
from typing import Optional, Dict, Any
from urllib.parse import urlencode

from ninepay.config import NinePayConfig
from ninepay.request import (
    CreatePaymentRequest,
    CreateRefundRequest,
    PayerAuthRequest,
    AuthorizeCardPaymentRequest,
    ReverseCardPaymentRequest,
    CapturePaymentRequest
)
from ninepay.response import BasicResponse
from ninepay.utils import Signature
from ninepay.enums import Environment
from ninepay.exceptions import PaymentException, APIException, SignatureException


class NinePayGateway:
    """
    Main gateway class for interacting with 9Pay Payment API
    """
    
    def __init__(self, config: NinePayConfig):
        """
        Initialize gateway with configuration
        
        Args:
            config: NinePayConfig instance with credentials
        """
        self.config = config
        self.endpoint = (config.endpoint or Environment.get_endpoint(config.env)).rstrip('/')
    
    def create_payment(self, request: CreatePaymentRequest) -> BasicResponse:
        """
        Create a payment request and get redirect URL (Portal flow)
        """
        try:
            # 1. Prepare data (Matching PHP sample keys)
            payload = request.to_dict()
            payload['merchantKey'] = self.config.merchant_id
            payload['time'] = str(int(time.time()))
            
            # 2. Build the Message to sign
            time_str = payload['time']
            # Sign URL usually matches the creation endpoint path
            url_to_sign = f"{self.endpoint}/payments/create"
            
            message = self._generate_v2_message(time_str, url_to_sign, payload, 'POST')
            signature = Signature.generate(message, self.config.secret_key)
            
            # 3. Build Redirect URL (Portal flow)
            json_data = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
            base_encode = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
            
            params = {
                'baseEncode': base_encode,
                'signature': signature
            }
            
            redirect_url = f"{self.endpoint}/portal?{urlencode(params)}"
            
            return BasicResponse.success_response(
                data={'redirect_url': redirect_url},
                message='OK'
            )
        except Exception as e:
            raise PaymentException(f"Payment creation error: {str(e)}")

    def inquiry(self, transaction_id: str) -> BasicResponse:
        """
        Query transaction status by ID
        """
        url = f"{self.endpoint}/v2/payments/{transaction_id}/inquire"
        return self._send_v2_request_internal(url, {}, method='GET')

    def refund(self, request: CreateRefundRequest) -> BasicResponse:
        """
        Create a refund request
        """
        url = f"{self.endpoint}/refunds/create"
        return self._send_v2_request_internal(url, request.to_dict())

    def payer_auth(self, request: PayerAuthRequest) -> BasicResponse:
        """
        Initiate payer authentication for card payment
        """
        url = f"{self.endpoint}/v2/payments/payer-auth"
        return self._send_v2_request_internal(url, request.to_dict())

    def authorize_card_payment(self, request: AuthorizeCardPaymentRequest) -> BasicResponse:
        """
        Authorize card payment
        """
        url = f"{self.endpoint}/v2/payments/authorize"
        return self._send_v2_request_internal(url, request.to_dict())

    def reverse_card_payment(self, request: ReverseCardPaymentRequest) -> BasicResponse:
        """
        Reverse card payment authorization
        """
        url = f"{self.endpoint}/v2/payments/reverse-auth"
        return self._send_v2_request_internal(url, request.to_dict())

    def capture(self, request: CapturePaymentRequest) -> BasicResponse:
        """
        Capture an authorized payment
        """
        url = f"{self.endpoint}/v2/payments/capture"
        return self._send_v2_request_internal(url, request.to_dict())

    def verify(self, result: str, checksum: str) -> bool:
        """
        Verify webhook/callback signature
        """
        try:
            hash_checksum = hashlib.sha256((result + self.config.checksum_key).encode('utf-8')).hexdigest().upper()
            return hmac.compare_digest(hash_checksum.encode('utf-8'), checksum.upper().encode('utf-8'))
        except Exception:
            return False

    def decode_result(self, result: str) -> str:
        """
        Decode base64 encoded result
        """
        try:
            return base64.b64decode(result).decode('utf-8')
        except Exception as e:
            raise PaymentException(f"Failed to decode result: {str(e)}")

    def _build_v2_headers(self, time_str: str, signature: str) -> Dict[str, str]:
        """
        Build V2 API headers
        """
        return {
            'Date': time_str,
            'Authorization': f"Signature Algorithm=HS256,Credential={self.config.merchant_id},SignedHeaders=,Signature={signature}"
        }

    def _generate_v2_message(self, time_str: str, url: str, params: Dict[str, Any], method: str = 'POST') -> str:
        """
        Generate message string for V2 signature
        """
        canonical_payload = ""
        if params:
            # Sort keys
            sorted_params = sorted(params.items())
            # Use default urlencode (RFC 1738, space as +) which worked for Create Payment and Refund
            canonical_payload = urlencode(sorted_params)

        components = [method, url, time_str]
        if canonical_payload:
            components.append(canonical_payload)
            
        return "\n".join(components)

    def _php_json_encode(self, data: Any) -> str:
        """
        Encode JSON in a way that matches V2 requirements
        (no spaces, no slash escaping)
        """
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)

    def _send_v2_request_internal(self, url: str, payload: Dict[str, Any], method: str = 'POST') -> BasicResponse:
        """
        Internal helper for sending V2 API requests
        """
        try:
            time_str = str(int(time.time()))
            
            # Preparation for signing
            if method == 'GET':
                message_params = {}
            elif '/refunds/create' in url:
                message_params = {k: (int(v) if isinstance(v, float) and v.is_integer() else v) for k, v in payload.items()}
            else:
                # Other POST requests use 'json' field
                clean_payload = {}
                for k, v in payload.items():
                    if isinstance(v, float) and v.is_integer():
                        clean_payload[k] = int(v)
                    elif isinstance(v, dict):
                        clean_payload[k] = {nk: (int(nv) if isinstance(nv, float) and nv.is_integer() else nv) for nk, nv in v.items()}
                    else:
                        clean_payload[k] = v
                message_params = {'json': self._php_json_encode(clean_payload)}

            # Generate signature
            message = self._generate_v2_message(time_str, url, message_params, method)
            
            # Uncomment for debugging signature issues:
            print(f"--- DEBUG SIGNATURE MESSAGE ---\n{message}\n--- END DEBUG ---")
            
            signature = Signature.generate(message, self.config.secret_key)
            headers = self._build_v2_headers(time_str, signature)
            
            if method == 'POST':
                # Use the EXACT same JSON formatting for the body that we might have used for signing
                # if the server validates raw body.
                json_body = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
                headers['Content-Type'] = 'application/json'
                response = requests.post(url, data=json_body.encode('utf-8'), headers=headers, timeout=30)
            else:
                response = requests.get(url, headers=headers, timeout=30)

            if 200 <= response.status_code < 300:
                result = response.json()
                return BasicResponse.success_response(
                    data=result,
                    message=result.get('message', 'Success')
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
            raise PaymentException(f"API operation error: {str(e)}")

    def __repr__(self):
        return f"NinePayGateway(merchant_id='{self.config.merchant_id}', env='{self.config.env}')"
