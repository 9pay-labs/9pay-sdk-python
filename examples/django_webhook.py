"""
Example: Django webhook handler
"""

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from ninepay import NinePayConfig, NinePayGateway

# Initialize 9Pay gateway from .env file
# Make sure you have a .env file with:
# NINEPAY_MERCHANT_ID=your_merchant_id
# NINEPAY_SECRET_KEY=your_secret_key
# NINEPAY_CHECKSUM_KEY=your_checksum_key
# NINEPAY_ENV=SANDBOX
config = NinePayConfig.from_env()
gateway = NinePayGateway(config)



@csrf_exempt
@require_http_methods(["POST"])
def payment_callback(request):
    """
    Handle payment callback from 9Pay
    
    Add this to your urls.py:
        path('payment/callback/', payment_callback, name='payment_callback'),
    """
    try:
        # Get data from POST request
        result = request.POST.get('result', '')
        checksum = request.POST.get('checksum', '')
        
        if not result or not checksum:
            return HttpResponseBadRequest('Missing parameters')
        
        # Verify signature
        if not gateway.verify(result, checksum):
            print("✗ Invalid signature!")
            return HttpResponseBadRequest('Invalid signature')
        
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
            # Example:
            # Order.objects.filter(invoice_no=invoice_no).update(
            #     status='paid',
            #     transaction_id=transaction_id
            # )
            
        elif status == 'failure':
            # Handle failed payment
            print(f"  → Processing failed payment for {invoice_no}")
            # TODO: Update your database here
        
        # Return success to 9Pay
        return HttpResponse('OK', status=200)
        
    except Exception as e:
        print(f"✗ Error processing callback: {str(e)}")
        return HttpResponse('Internal error', status=500)


def payment_return(request):
    """
    Handle user return from payment page
    
    Add this to your urls.py:
        path('payment/return/', payment_return, name='payment_return'),
    """
    # Get parameters from query string
    invoice_no = request.GET.get('invoice_no')
    status = request.GET.get('status')
    
    if status == 'success':
        html = f"""
        <h1>Payment Successful!</h1>
        <p>Invoice: {invoice_no}</p>
        <p>Thank you for your payment.</p>
        """
    else:
        html = f"""
        <h1>Payment Failed</h1>
        <p>Invoice: {invoice_no}</p>
        <p>Please try again.</p>
        """
    
    return HttpResponse(html)
