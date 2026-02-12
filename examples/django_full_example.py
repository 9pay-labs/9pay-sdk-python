"""
Ví dụ thực tế: Tích hợp 9Pay vào Django project
Real example: Integrating 9Pay into Django project
"""

# ============================================================================
# File: myproject/settings.py
# ============================================================================

import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(env_path)

# 9Pay Configuration - Load từ .env
NINEPAY_CONFIG = {
    'merchant_id': os.getenv('NINEPAY_MERCHANT_ID'),
    'secret_key': os.getenv('NINEPAY_SECRET_KEY'),
    'checksum_key': os.getenv('NINEPAY_CHECKSUM_KEY'),
    'env': os.getenv('NINEPAY_ENV', 'SANDBOX'),
}

# Callback URLs
NINEPAY_CALLBACK_URL = os.getenv('NINEPAY_CALLBACK_URL', 'http://localhost:8000/payment/callback/')
NINEPAY_RETURN_URL = os.getenv('NINEPAY_RETURN_URL', 'http://localhost:8000/payment/return/')
NINEPAY_BACK_URL = os.getenv('NINEPAY_BACK_URL', 'http://localhost:8000/payment/cancel/')


# ============================================================================
# File: myproject/payment/services.py
# ============================================================================

from django.conf import settings
from ninepay import NinePayConfig, NinePayGateway, CreatePaymentRequest, PaymentMethod, Currency, Language
import time


class PaymentService:
    """Service class để xử lý payment với 9Pay"""
    
    def __init__(self):
        # Cách 1: Load từ .env trực tiếp
        self.config = NinePayConfig.from_env()
        
        # Cách 2: Load từ Django settings
        # self.config = NinePayConfig.from_dict(settings.NINEPAY_CONFIG)
        
        self.gateway = NinePayGateway(self.config)
    
    def create_payment(self, order):
        """
        Tạo payment request cho đơn hàng
        
        Args:
            order: Order object từ database
            
        Returns:
            dict: {'success': bool, 'redirect_url': str, 'error': str}
        """
        try:
            # Tạo invoice number unique
            invoice_no = f'ORD_{order.id}_{int(time.time())}'
            
            # Tạo payment request
            request = CreatePaymentRequest(
                invoice_no=invoice_no,
                amount=str(int(order.total_amount)),  # Convert to string
                description=f'Thanh toán đơn hàng #{order.id}',
                back_url=settings.NINEPAY_BACK_URL,
                return_url=settings.NINEPAY_RETURN_URL
            )
            
            # Thêm thông tin optional
            request.with_method(PaymentMethod.ATM_CARD) \
                   .with_currency(Currency.VND) \
                   .with_lang(Language.VI) \
                   .with_expires_time(1440)  # 24 hours
            
            # Gửi request
            response = self.gateway.create_payment(request)
            
            if response.is_success():
                data = response.get_data()
                
                # Lưu invoice_no vào order
                order.invoice_no = invoice_no
                order.payment_status = 'pending'
                order.save()
                
                return {
                    'success': True,
                    'redirect_url': data.get('redirect_url'),
                    'invoice_no': invoice_no
                }
            else:
                return {
                    'success': False,
                    'error': response.get_message()
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_callback(self, result, checksum):
        """
        Xác thực callback từ 9Pay
        
        Args:
            result: Base64 encoded result từ 9Pay
            checksum: Signature từ 9Pay
            
        Returns:
            dict: Payment data nếu hợp lệ, None nếu không hợp lệ
        """
        try:
            # Verify signature
            if not self.gateway.verify(result, checksum):
                return None
            
            # Decode result
            import json
            json_result = self.gateway.decode_result(result)
            data = json.loads(json_result)
            
            return data
            
        except Exception as e:
            print(f"Error verifying callback: {e}")
            return None
    
    def query_transaction(self, invoice_no):
        """
        Truy vấn trạng thái giao dịch
        
        Args:
            invoice_no: Invoice number cần query
            
        Returns:
            dict: Transaction data
        """
        try:
            response = self.gateway.inquiry(invoice_no)
            
            if response.is_success():
                return {
                    'success': True,
                    'data': response.get_data()
                }
            else:
                return {
                    'success': False,
                    'error': response.get_message()
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# ============================================================================
# File: myproject/payment/views.py
# ============================================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .services import PaymentService
from .models import Order


def create_payment_view(request, order_id):
    """View để tạo payment"""
    order = get_object_or_404(Order, id=order_id)
    
    # Khởi tạo payment service
    payment_service = PaymentService()
    
    # Tạo payment
    result = payment_service.create_payment(order)
    
    if result['success']:
        # Redirect user đến trang thanh toán 9Pay
        return redirect(result['redirect_url'])
    else:
        # Hiển thị lỗi
        return render(request, 'payment/error.html', {
            'error': result['error']
        })


@csrf_exempt
@require_http_methods(["POST"])
def payment_callback_view(request):
    """
    Webhook callback từ 9Pay
    URL: /payment/callback/
    """
    # Get data từ POST request
    result = request.POST.get('result', '')
    checksum = request.POST.get('checksum', '')
    
    if not result or not checksum:
        return HttpResponse('Missing parameters', status=400)
    
    # Verify và decode
    payment_service = PaymentService()
    data = payment_service.verify_callback(result, checksum)
    
    if not data:
        return HttpResponse('Invalid signature', status=400)
    
    # Extract thông tin
    invoice_no = data.get('invoice_no')
    status = data.get('status')
    amount = data.get('amount')
    transaction_id = data.get('transactionId')
    
    # Tìm order
    try:
        order = Order.objects.get(invoice_no=invoice_no)
        
        if status == 'success':
            # Cập nhật order thành công
            order.payment_status = 'paid'
            order.transaction_id = transaction_id
            order.save()
            
            # TODO: Gửi email xác nhận, cập nhật inventory, etc.
            
        elif status == 'failure':
            # Cập nhật order thất bại
            order.payment_status = 'failed'
            order.save()
        
        return HttpResponse('OK', status=200)
        
    except Order.DoesNotExist:
        return HttpResponse('Order not found', status=404)
    except Exception as e:
        print(f"Error processing callback: {e}")
        return HttpResponse('Internal error', status=500)


def payment_return_view(request):
    """
    User return từ trang thanh toán
    URL: /payment/return/
    """
    invoice_no = request.GET.get('invoice_no')
    status = request.GET.get('status')
    
    try:
        order = Order.objects.get(invoice_no=invoice_no)
        
        return render(request, 'payment/result.html', {
            'order': order,
            'status': status
        })
        
    except Order.DoesNotExist:
        return render(request, 'payment/error.html', {
            'error': 'Order not found'
        })


def payment_cancel_view(request):
    """
    User cancel payment
    URL: /payment/cancel/
    """
    return render(request, 'payment/cancelled.html')


# ============================================================================
# File: myproject/payment/urls.py
# ============================================================================

from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('create/<int:order_id>/', views.create_payment_view, name='create'),
    path('callback/', views.payment_callback_view, name='callback'),
    path('return/', views.payment_return_view, name='return'),
    path('cancel/', views.payment_cancel_view, name='cancel'),
]


# ============================================================================
# File: .env (trong thư mục gốc của Django project)
# ============================================================================

"""
# Django Settings
DEBUG=True
SECRET_KEY=your-django-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname

# 9Pay Configuration
NINEPAY_MERCHANT_ID=MERCHANT123456
NINEPAY_SECRET_KEY=sk_test_abc123xyz
NINEPAY_CHECKSUM_KEY=ck_test_def456uvw
NINEPAY_ENV=SANDBOX

# 9Pay URLs
NINEPAY_CALLBACK_URL=https://yourdomain.com/payment/callback/
NINEPAY_RETURN_URL=https://yourdomain.com/payment/return/
NINEPAY_BACK_URL=https://yourdomain.com/payment/cancel/
"""


# ============================================================================
# Cách sử dụng:
# ============================================================================

"""
1. Cài đặt dependencies:
   pip install ninepay-sdk python-dotenv

2. Tạo file .env trong thư mục gốc Django project và điền thông tin

3. Trong template, tạo button thanh toán:
   <a href="{% url 'payment:create' order.id %}" class="btn btn-primary">
       Thanh toán
   </a>

4. Khi user click, sẽ:
   - Tạo payment request với 9Pay
   - Redirect user đến trang thanh toán
   - User thanh toán
   - 9Pay gọi callback webhook
   - Cập nhật order status
   - Redirect user về trang return

5. Tất cả config được quản lý tập trung trong file .env
"""
