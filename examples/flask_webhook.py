"""
Example: Flask webhook handler
"""

from flask import Flask, request, jsonify
import json
from ninepay import NinePayConfig, NinePayGateway

app = Flask(__name__)

# Initialize 9Pay gateway from .env file
# Make sure you have a .env file with:
# NINEPAY_MERCHANT_ID=your_merchant_id
# NINEPAY_SECRET_KEY=your_secret_key
# NINEPAY_CHECKSUM_KEY=your_checksum_key
# NINEPAY_ENV=SANDBOX
config = NinePayConfig.from_env()
gateway = NinePayGateway(config)


@app.route('/payment/callback', methods=['POST'])
def payment_callback():
    """
    Handle payment callback from 9Pay
    """
    try:
        # Get data from POST request
        result = request.form.get('result', '')
        checksum = request.form.get('checksum', '')
        
        if not result or not checksum:
            return 'Missing parameters', 400
        
        # Verify signature
        if not gateway.verify(result, checksum):
            print("✗ Invalid signature!")
            return 'Invalid signature', 400
        
        # Decode result
        json_result = gateway.decode_result(result)
        data = json.loads(json_result)
        
        # Extract payment information
        invoice_no = data.get('invoice_no')
        status = data.get('status')
        amount = data.get('amount')
        transaction_id = data.get('transactionId')
        
        print(f"✓ Webhook received and verified!")
        print(f"  Invoice No: {invoice_no}")
        print(f"  Status: {status}")
        print(f"  Amount: {amount}")
        print(f"  Transaction ID: {transaction_id}")
        
        # Process based on status
        if status == 'success':
            # Update order status in database
            print(f"  → Processing successful payment for {invoice_no}")
            # TODO: Update your database here
            
        elif status == 'failure':
            # Handle failed payment
            print(f"  → Processing failed payment for {invoice_no}")
            # TODO: Update your database here
        
        # Return success to 9Pay
        return 'OK', 200
        
    except Exception as e:
        print(f"✗ Error processing callback: {str(e)}")
        return 'Internal error', 500


@app.route('/payment/return', methods=['GET'])
def payment_return():
    """
    Handle user return from payment page
    """
    # Get parameters from query string
    invoice_no = request.args.get('invoice_no')
    status = request.args.get('status')
    
    if status == 'success':
        return f"""
        <h1>Payment Successful!</h1>
        <p>Invoice: {invoice_no}</p>
        <p>Thank you for your payment.</p>
        """
    else:
        return f"""
        <h1>Payment Failed</h1>
        <p>Invoice: {invoice_no}</p>
        <p>Please try again.</p>
        """


if __name__ == '__main__':
    print("Starting Flask webhook server...")
    print("Callback URL: http://localhost:5000/payment/callback")
    print("Return URL: http://localhost:5000/payment/return")
    app.run(debug=True, port=5000)
