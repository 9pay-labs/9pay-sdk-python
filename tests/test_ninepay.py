"""
Unit tests for NinePay SDK
"""

import unittest
from ninepay import (
    NinePayConfig,
    NinePayGateway,
    CreatePaymentRequest,
    PaymentMethod,
    Currency,
    Language
)
from ninepay.exceptions import ValidationException
from ninepay.utils import Signature


class TestNinePayConfig(unittest.TestCase):
    """Test NinePayConfig class"""
    
    def test_config_creation(self):
        """Test creating config with valid parameters"""
        config = NinePayConfig(
            merchant_id='TEST_MERCHANT',
            secret_key='TEST_SECRET',
            checksum_key='TEST_CHECKSUM',
            env='SANDBOX'
        )
        
        self.assertEqual(config.merchant_id, 'TEST_MERCHANT')
        self.assertEqual(config.secret_key, 'TEST_SECRET')
        self.assertEqual(config.checksum_key, 'TEST_CHECKSUM')
        self.assertEqual(config.env, 'SANDBOX')
    
    def test_config_from_dict(self):
        """Test creating config from dictionary"""
        config_dict = {
            'merchant_id': 'TEST_MERCHANT',
            'secret_key': 'TEST_SECRET',
            'checksum_key': 'TEST_CHECKSUM',
            'env': 'PRODUCTION'
        }
        
        config = NinePayConfig.from_dict(config_dict)
        
        self.assertEqual(config.merchant_id, 'TEST_MERCHANT')
        self.assertEqual(config.env, 'PRODUCTION')
    
    def test_config_validation(self):
        """Test config validation"""
        with self.assertRaises(ValueError):
            NinePayConfig('', 'secret', 'checksum', 'SANDBOX')
        
        with self.assertRaises(ValueError):
            NinePayConfig('merchant', '', 'checksum', 'SANDBOX')
        
        with self.assertRaises(ValueError):
            NinePayConfig('merchant', 'secret', '', 'SANDBOX')
        
        with self.assertRaises(ValueError):
            NinePayConfig('merchant', 'secret', 'checksum', 'INVALID')

    def test_config_from_env(self):
        """Test creating config from environment variables"""
        import os
        from unittest.mock import patch
        
        env_vars = {
            'NINEPAY_MERCHANT_ID': 'ENV_MERCHANT',
            'NINEPAY_SECRET_KEY': 'ENV_SECRET',
            'NINEPAY_CHECKSUM_KEY': 'ENV_CHECKSUM',
            'NINEPAY_ENV': 'PRODUCTION'
        }
        
        with patch.dict(os.environ, env_vars):
            # Also patch load_dotenv to avoid reading real .env file
            with patch('dotenv.load_dotenv', return_value=True):
                config = NinePayConfig.from_env()
                
                self.assertEqual(config.merchant_id, 'ENV_MERCHANT')
                self.assertEqual(config.secret_key, 'ENV_SECRET')
                self.assertEqual(config.checksum_key, 'ENV_CHECKSUM')
                self.assertEqual(config.env, 'PRODUCTION')
    
    def test_config_from_env_defaults(self):
        """Test config from env with defaults"""
        import os
        from unittest.mock import patch
        
        env_vars = {
            'NINEPAY_MERCHANT_ID': 'ENV_MERCHANT',
            'NINEPAY_SECRET_KEY': 'ENV_SECRET',
            'NINEPAY_CHECKSUM_KEY': 'ENV_CHECKSUM'
            # NINEPAY_ENV is missing
        }
        
        # Ensure NINEPAY_ENV is not in environment
        if 'NINEPAY_ENV' in os.environ:
            del os.environ['NINEPAY_ENV']
            
        with patch.dict(os.environ, env_vars):
            with patch('dotenv.load_dotenv', return_value=True):
                config = NinePayConfig.from_env()
                
                self.assertEqual(config.merchant_id, 'ENV_MERCHANT')
                self.assertEqual(config.env, 'SANDBOX')  # Default value


class TestCreatePaymentRequest(unittest.TestCase):
    """Test CreatePaymentRequest class"""
    
    def test_request_creation(self):
        """Test creating payment request"""
        request = CreatePaymentRequest(
            invoice_no='INV_123',
            amount='50000',
            description='Test payment',
            back_url='https://example.com/cancel',
            return_url='https://example.com/success'
        )
        
        data = request.to_dict()
        
        self.assertEqual(data['invoiceNo'], 'INV_123')
        self.assertEqual(data['amount'], '50000')
        self.assertEqual(data['description'], 'Test payment')
    
    def test_request_fluent_interface(self):
        """Test fluent interface"""
        request = CreatePaymentRequest(
            invoice_no='INV_123',
            amount='50000',
            description='Test payment',
            back_url='https://example.com/cancel',
            return_url='https://example.com/success'
        )
        
        request.with_method(PaymentMethod.ATM_CARD) \
               .with_currency(Currency.VND) \
               .with_lang(Language.VI) \
               .with_expires_time(1440)
        
        data = request.to_dict()
        
        self.assertEqual(data['method'], PaymentMethod.ATM_CARD)
        self.assertEqual(data['currency'], Currency.VND)
        self.assertEqual(data['lang'], Language.VI)
        self.assertEqual(data['expiresTime'], 1440)
    
    def test_request_validation(self):
        """Test request validation"""
        with self.assertRaises(ValidationException):
            CreatePaymentRequest('', '50000', 'desc', 'back', 'return')
        
        with self.assertRaises(ValidationException):
            CreatePaymentRequest('inv', '', 'desc', 'back', 'return')


class TestSignature(unittest.TestCase):
    """Test Signature utility"""
    
    def test_signature_generation(self):
        """Test signature generation"""
        data = "test_data"
        secret = "test_secret"
        
        signature = Signature.generate(data, secret)
        
        self.assertIsInstance(signature, str)
        self.assertTrue(len(signature) > 0)
    
    def test_signature_verification(self):
        """Test signature verification"""
        data = "test_data"
        secret = "test_secret"
        
        signature = Signature.generate(data, secret)
        
        # Valid signature
        self.assertTrue(Signature.verify(data, signature, secret))
        
        # Invalid signature
        self.assertFalse(Signature.verify(data, "invalid_signature", secret))
        
        # Wrong secret
        self.assertFalse(Signature.verify(data, signature, "wrong_secret"))
    
    def test_signature_consistency(self):
        """Test that same input produces same signature"""
        data = "test_data"
        secret = "test_secret"
        
        sig1 = Signature.generate(data, secret)
        sig2 = Signature.generate(data, secret)
        
        self.assertEqual(sig1, sig2)


class TestNinePayGateway(unittest.TestCase):
    """Test NinePayGateway class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = NinePayConfig(
            merchant_id='TEST_MERCHANT',
            secret_key='TEST_SECRET',
            checksum_key='TEST_CHECKSUM',
            env='SANDBOX'
        )
        self.gateway = NinePayGateway(self.config)
    
    def test_gateway_initialization(self):
        """Test gateway initialization"""
        self.assertIsNotNone(self.gateway)
        self.assertEqual(self.gateway.config.merchant_id, 'TEST_MERCHANT')
    
    def test_decode_result(self):
        """Test decoding base64 result"""
        import base64
        
        original_data = '{"invoice_no": "INV_123", "status": "success"}'
        encoded_data = base64.b64encode(original_data.encode('utf-8')).decode('utf-8')
        
        decoded = self.gateway.decode_result(encoded_data)
        
        self.assertEqual(decoded, original_data)


if __name__ == '__main__':
    unittest.main()
