# 9PAY Payment Gateway Python SDK

Official Python SDK for integrating 9PAY Payment Gateway.

[English](#english) | [Tiếng Việt](#tiếng-việt)

---

## English

### 🚀 Quick Start (Recommended)

1. **Install SDK:**
   ```bash
   pip install ninepay-sdk python-dotenv
   ```

2. **Configure Environment:**
   Copy `.env.example` to `.env` and fill in your credentials.
   ```bash
   cp .env.example .env
   ```

   ```env
   NINEPAY_MERCHANT_ID=your_merchant_id
   NINEPAY_SECRET_KEY=your_secret_key
   NINEPAY_CHECKSUM_KEY=your_checksum_key
   NINEPAY_ENV=SANDBOX
   ```

3. **Usage:**
   ```python
   from ninepay import NinePayConfig, NinePayGateway
   
   # Load config automatically from .env
   config = NinePayConfig.from_env()
   gateway = NinePayGateway(config)
   ```

### 📦 Features
- ✅ **Dynamic Config**: Managed via `.env` files
- ✅ **Secure**: Signature generation and verification
- ✅ **Complete**: Payment creation, inquiry, and webhook handlers
- ✅ **Framework Friendly**: Ready for Django, Flask, FastAPI

### 🛠 Installation
```bash
pip install ninepay-sdk
```

### 💡 Example: Create Payment
```python
from ninepay import CreatePaymentRequest, PaymentMethod, Currency, Language
import time

request = CreatePaymentRequest(
    invoice_no=f'INV_{int(time.time())}',
    amount='50000',
    description='Order #12345',
    back_url='https://yoursite.com/cancel',
    return_url='https://yoursite.com/success'
).with_method(PaymentMethod.ATM_CARD).with_lang(Language.EN)

response = gateway.create_payment(request)
if response.is_success():
    print(f"Redirect URL: {response.get_data()['redirect_url']}")
```

---

## Tiếng Việt

### 🚀 Bắt đầu nhanh (Khuyên dùng)

1. **Cài đặt:**
   ```bash
   pip install ninepay-sdk python-dotenv
   ```

2. **Cấu hình môi trường:**
   Copy `.env.example` thành `.env` và điền thông tin của bạn.
   ```bash
   cp .env.example .env
   ```

3. **Sử dụng:**
   ```python
   from ninepay import NinePayConfig, NinePayGateway
   
   # Tự động load cấu hình từ file .env
   config = NinePayConfig.from_env()
   gateway = NinePayGateway(config)
   ```

### ✨ Tính năng chính
- ✅ **Cấu hình tập trung**: Quản lý qua file `.env` (giống Laravel/PHP)
- ✅ **Bảo mật**: Tự động tạo và xác thực chữ ký (checksum)
- ✅ **Đầy đủ**: Hỗ trợ tạo thanh toán, truy vấn đơn hàng và Webhook
- ✅ **Dễ tích hợp**: Tương thích tốt với Django, Flask, FastAPI

### 💡 Ví dụ: Tạo thanh toán
```python
from ninepay import CreatePaymentRequest, PaymentMethod, Language
import time

request = CreatePaymentRequest(
    invoice_no=f'INV_{int(time.time())}',
    amount='100000',
    description='Thanh toán đơn hàng #123',
    back_url='https://site.com/cancel',
    return_url='https://site.com/success'
).with_method(PaymentMethod.ATM_CARD).with_lang(Language.VI)

response = gateway.create_payment(request)
if response.is_success():
    print(f"URL Thanh toán: {response.get_data()['redirect_url']}")
```

### 🖥 Chạy Demo
Bạn có thể chạy script demo để kiểm tra nhanh:
```bash
python demo.py
```

### 🧪 Chạy Test
```bash
python -m unittest discover tests -v
```

Licensed under MIT.
