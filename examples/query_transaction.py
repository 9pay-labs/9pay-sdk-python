"""
Example: Query transaction status
"""

from ninepay import NinePayConfig, NinePayGateway


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
    
    # Invoice number to query
    invoice_no = 'INV_1234567890'
    
    try:
        response = gateway.inquiry(invoice_no)
        
        if response.is_success():
            data = response.get_data()
            print(f"✓ Transaction found!")
            print(f"  Invoice No: {data.get('invoice_no')}")
            print(f"  Status: {data.get('status')}")
            print(f"  Amount: {data.get('amount')}")
            print(f"  Currency: {data.get('currency')}")
            print(f"  Transaction ID: {data.get('transactionId')}")
            print(f"  Payment Method: {data.get('method')}")
            print(f"  Created At: {data.get('createdAt')}")
        else:
            print(f"✗ Query failed!")
            print(f"  Error: {response.get_message()}")
            print(f"  Error Code: {response.get_error_code()}")
            
    except Exception as e:
        print(f"✗ Exception occurred: {str(e)}")


if __name__ == '__main__':
    main()
