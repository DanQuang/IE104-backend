Dưới đây là hướng dẫn cho một README file để cài đặt môi trường ảo, cài đặt các yêu cầu và chạy server trong Django:

---

# Django Project Setup Guide

## 1. Cài đặt môi trường ảo

Để tách biệt các thư viện cần thiết cho dự án, hãy sử dụng môi trường ảo (virtual environment).

### Bước 1: Cài đặt `virtualenv`

Nếu bạn chưa cài `virtualenv`, bạn có thể cài bằng lệnh sau:

```bash
pip install virtualenv
```

### Bước 2: Tạo môi trường ảo

Tạo một thư mục cho môi trường ảo:

```bash
virtualenv venv
```

Hoặc nếu bạn dùng Python:

```bash
python -m venv venv
```

### Bước 3: Kích hoạt môi trường ảo

- Trên Windows:

```bash
venv\Scripts\activate
```

- Trên MacOS/Linux:

```bash
source venv/bin/activate
```

Sau khi kích hoạt môi trường ảo, bạn sẽ thấy tên môi trường (ví dụ `venv`) xuất hiện ở đầu dòng lệnh.

## 2. Cài đặt các thư viện yêu cầu

### Bước 1: Cài đặt các yêu cầu từ `requirements.txt`

Tạo một file `requirements.txt` chứa các thư viện cần thiết cho dự án (nếu chưa có). Bạn có thể sử dụng lệnh sau để cài đặt:

```bash
pip install -r requirements.txt
```

Nếu bạn chưa có `requirements.txt`, bạn có thể tạo một file thủ công hoặc tạo từ môi trường hiện tại với lệnh:

```bash
pip freeze > requirements.txt
```

## 3. Cấu hình Django Project

### Bước 1: Cài đặt Django (nếu chưa cài trong `requirements.txt`)

Nếu Django chưa có trong file `requirements.txt`, bạn có thể cài đặt trực tiếp:

```bash
pip install django
```

### Bước 2: Migrate database

Chạy lệnh migrate để tạo các bảng trong cơ sở dữ liệu:

```bash
python manage.py migrate
```

### Bước 3: Tạo Superuser (Tùy chọn)

Nếu bạn muốn tạo tài khoản admin cho Django admin panel, chạy lệnh sau và điền thông tin:

```bash
python manage.py createsuperuser
```

## 4. Chạy Server Django

Cuối cùng, để chạy server Django, bạn chỉ cần sử dụng lệnh:

```bash
python manage.py runserver
```

Server sẽ chạy trên `http://127.0.0.1:8000/`.

---
