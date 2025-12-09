# Temel imaj olarak resmi Python imajını kullan
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Bağımlılıklar dosyasını kopyala
COPY requirements.txt .

# Gerekli Python paketlerini kur
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY app.py .

# Uygulamanın çalışacağı portu belirle
EXPOSE 5000

# Uygulamayı çalıştır
CMD ["python", "app.py"]