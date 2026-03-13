#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
9Pay SDK Demo (Comprehensive Examples)
Ví dụ đầy đủ các tính năng của 9Pay SDK
"""

import time
import json
from ninepay import (
    NinePayConfig,
    NinePayGateway,
    CreatePaymentRequest,
    CreateRefundRequest,
    PayerAuthRequest,
    AuthorizeCardPaymentRequest,
    ReverseCardPaymentRequest,
    CapturePaymentRequest,
    PaymentMethod,
    Currency,
    Language,
    TransactionType
)

def run_demo():
    print("=" * 60)
    print("  9PAY SDK - COMPREHENSIVE DEMO")
    print("=" * 60)
    
    try:
        # 1. Load configuration (Prioritize .env file)
        config = NinePayConfig.from_env()
        
        # Check if config is configured
        if not config.merchant_id or config.merchant_id == 'YOUR_MERCHANT_ID':
            print("\n[!] Please configure .env file with your actual credentials")
            print("    Continuing with dummy values for demonstration...")
            config = NinePayConfig(
                merchant_id='F0cA8a',
                secret_key='BhJdW4lV5MctJW7jlzLkvdx5n14LniMxFJD',
                checksum_key='hTlzTKrpNKO9ZXe1QwEOhcnrUttVo4Cb',
                env='SANDBOX'
            )
        
        gateway = NinePayGateway(config)
        print(f"\n[✓] Configured for: {config.env}")
        print(f"[✓] Endpoint: {gateway.endpoint}")

        # --- EXAMPLE 1: CREATE PORTAL PAYMENT ---
        print("\n" + "-"*40)
        print("1. CREATE PAYMENT (PORTAL FLOW)")
        print("-"*40)
        invoice_no = f'INV_DEMO_{int(time.time())}'
        request = CreatePaymentRequest(
            invoice_no=invoice_no,
            amount='100000',
            description='Demo Payment from Python SDK',
            back_url='https://example.com/cancel',
            return_url='https://example.com/success'
        ).with_method(PaymentMethod.CREDIT_CARD).with_lang(Language.EN)
        
        response = gateway.create_payment(request)
        if response.is_success():
            print(f"✅ Success! Redirect URL:\n{response.get_data()['redirect_url']}")
        else:
            print(f"❌ Error: {response.get_message()}")

        # --- EXAMPLE 2: INQUIRY (TRUY VẤN) ---
        print("\n" + "-"*40)
        print("2. TRANSACTION INQUIRY")
        print("-"*40)
        # Bỏ comment dòng dưới để chạy test inquiry với mã thật
        # transaction_id = "454518005824417"
        # try:
        #     response = gateway.inquiry(transaction_id)
        #     print(f"✅ Status: {response.get_data().get('status')}")
        #     print(f"✅ Full Data: {json.dumps(response.get_data(), indent=2)}")
        # except Exception as e:
        #     print(f"ℹ Skipping Inquiry: {str(e)}")
        print("ℹ (Set transaction_id and uncomment in demo.py to test)")

        # --- EXAMPLE 3: REFUND (HOÀN TIỀN) ---
        print("\n" + "-"*40)
        print("3. REFUND REQUEST")
        print("-"*40)
        # refund_req = CreateRefundRequest(
        #     request_code=f'REF_{int(time.time())}',
        #     payment_no=454518005824417,
        #     amount=10000,
        #     description="Demo Refund"
        # )
        # try:
        #     response = gateway.refund(refund_req)
        #     print(f"✅ Response: {json.dumps(response.get_data(), indent=2)}")
        # except Exception as e:
        #     print(f"ℹ Skipping Refund: {str(e)}")
        print("ℹ (Configure refund parameters and uncomment in demo.py to test)")

        # --- EXAMPLE 4: ADVANCED CARD PAYMENT (AUTH/CAPTURE) ---
        print("\n" + "-"*40)
        print("4. CARD AUTHENTICATION & AUTHORIZATION")
        print("-"*40)
        print("ℹ This flow requires real-time interaction (Payer Auth -> 3DS -> Authorize).")
        print("  Check 'test_all_apis.py' for step-by-step logic.")

        print("\n" + "=" * 60)
        print("  ✅ Demo processing finished!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")

if __name__ == '__main__':
    run_demo()
