"""
Example: Basic payment creation
"""

from ninepay import (
    NinePayConfig,
    NinePayGateway,
    CreatePaymentRequest,
    PaymentMethod,
    Currency,
    Language
)
import time


def main():
    # Initialize configuration from .env file
    # Make sure you have a .env file with:
    # NINEPAY_MERCHANT_ID=your_merchant_id
    # NINEPAY_SECRET_KEY=your_secret_key
    # NINEPAY_CHECKSUM_KEY=your_checksum_key
    # NINEPAY_ENV=SANDBOX
    config = NinePayConfig.from_env()
    
    # Create gateway instance
    gateway = NinePayGateway(config)
    
    # Create payment request
    invoice_no = f'INV_{int(time.time())}'
    
    request = CreatePaymentRequest(
        invoice_no=invoice_no,
        amount='50000',
        description='Payment for Order #123',
        back_url='https://yoursite.com/payment/cancel',
        return_url='https://yoursite.com/payment/success'
    )
    
    # Add optional parameters
    request.with_method(PaymentMethod.ATM_CARD) \
           .with_client_ip('127.0.0.1') \
           .with_currency(Currency.VND) \
           .with_lang(Language.VI) \
           .with_expires_time(1440)
    
    # Send payment request
    try:
        response = gateway.create_payment(request)
        
        if response.is_success():
            data = response.get_data()
            redirect_url = data.get('redirect_url')
            print(f"✓ Payment created successfully!")
            print(f"  Invoice No: {invoice_no}")
            print(f"  Redirect URL: {redirect_url}")
            print(f"\nPlease redirect user to: {redirect_url}")
        else:
            print(f"✗ Payment creation failed!")
            print(f"  Error: {response.get_message()}")
            print(f"  Error Code: {response.get_error_code()}")
            
    except Exception as e:
        print(f"✗ Exception occurred: {str(e)}")


if __name__ == '__main__':
    main()
