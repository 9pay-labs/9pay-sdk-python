#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
9Pay SDK Demo (Prioritizing .env configuration)
Ví dụ sử dụng 9Pay SDK (Ưu tiên cấu hình từ file .env)
"""

import time
from ninepay import (
    NinePayConfig,
    NinePayGateway,
    CreatePaymentRequest,
    PaymentMethod,
    Currency,
    Language,
)

def main():
    print("=" * 60)
    print("  9PAY SDK - DEMO (Config via .env)")
    print("=" * 60)
    
    try:
        # Load configuration (Prioritize .env file)
        # Bắt đầu bằng cách load từ .env
        print("\n1. Loading configuration...")
        config = NinePayConfig.from_env()
        
        # Check if config is dummy/default
        if not config.merchant_id or config.merchant_id == 'YOUR_MERCHANT_ID':
            print("ℹ Using hardcoded DEMO values (No .env file found or not configured)")
            config = NinePayConfig(
                merchant_id='DEMO_MERCHANT',
                secret_key='DEMO_SECRET',
                checksum_key='DEMO_CHECKSUM',
                env='SANDBOX'
            )
            
        print(f"   ✓ Config active: {config}")
        
        # Initialize gateway
        print("\n2. Initializing gateway...")
        gateway = NinePayGateway(config)
        print(f"   ✓ Gateway initialized")
        
        # Create payment request
        print("\n3. Creating sample payment request...")
        invoice_no = f'INV_{int(time.time())}'
        
        request = CreatePaymentRequest(
            invoice_no=invoice_no,
            amount='100000',
            description='Demo Payment from Python SDK',
            back_url='https://example.com/cancel',
            return_url='https://example.com/success'
        )
        
        # Fluent interface to add options
        request.with_method(PaymentMethod.ATM_CARD) \
               .with_currency(Currency.VND) \
               .with_lang(Language.VI)
        
        print(f"   ✓ Request prepared for: {invoice_no}")
        print(f"   - Amount: 100,000 VND")
        
        # To actually send the request, uncomment below:
        """
        print("\n4. Executing payment request...")
        response = gateway.create_payment(request)
        if response.is_success():
            print(f"   ✅ Redirect URL: {response.get_data()['redirect_url']}")
        else:
            print(f"   ❌ Error: {response.get_message()}")
        """
        
        print("\n" + "=" * 60)
        print("  ✅ Demo executed successfully!")
        print("=" * 60)
        print("\nTiếp theo:")
        print("1. Copy .env.example sang .env")
        print("2. Điền thông tin thật của bạn vào .env")
        print("3. Chạy lại script này: python demo.py")
        print("4. Đọc README.md để xem hướng dẫn tích hợp Django/Flask")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == '__main__':
    main()
