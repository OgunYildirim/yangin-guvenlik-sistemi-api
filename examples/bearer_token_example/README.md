# 🔑 Bearer Token (API Token) Authentication Örneği

## Açıklama

Bu örnek, **statik API token'lar** (Bearer Token) kullanarak basit authentication gösterir.

### Bearer Token Nedir?

- Statik, değişmeyen token'lar
- Genellikle API key olarak kullanılır
- Süre sınırı yoktur (manuel iptal gerekir)
- Basit ve hızlıdır
- Servisler arası iletişim için idealdir

## Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt
```

## Kullanım

### 1. Server'ı Başlat

```bash
python server.py
```

Server `http://localhost:5001` adresinde çalışacak.

### 2. Client'ı Çalıştır (Başka bir terminalde)

```bash
python client.py
```

## Mevcut API Token'lar

| Kullanıcı | Role | Token |
|-----------|------|-------|
| admin | admin | api_token_admin_12345 |
| user1 | user | api_token_user_67890 |
| service_account | service | api_token_service_abcde |

## Endpoints

### Public (Token Gerektirmez)
- `GET /api/public` - Herkese açık endpoint

### Protected (Bearer Token Gerekli)
- `GET /api/protected` - Token ile korunan endpoint
- `GET /api/admin` - Admin token gerektirir

### Utility
- `POST /api/generate-token` - Yeni token oluştur
- `GET /api/list-tokens` - Token'ları listele

## Örnek Kullanım

### PowerShell

```powershell
# Public endpoint
curl http://localhost:5001/api/public

# Protected endpoint (Bearer token ile)
$headers = @{
    "Authorization" = "Bearer api_token_admin_12345"
}
Invoke-RestMethod -Uri http://localhost:5001/api/protected -Headers $headers

# Yeni token oluştur
$body = @{
    user = "new_user"
    role = "user"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:5001/api/generate-token -ContentType "application/json" -Body $body
```

### cURL

```bash
# Public endpoint
curl http://localhost:5001/api/public

# Protected endpoint
curl -H "Authorization: Bearer api_token_admin_12345" http://localhost:5001/api/protected

# Admin endpoint
curl -H "Authorization: Bearer api_token_admin_12345" http://localhost:5001/api/admin
```

## Özellikler

✅ Basit ve hızlı authentication  
✅ Statik token'lar  
✅ Role-based access control  
✅ Yeni token oluşturma  
✅ Token listesi görüntüleme  

## Kullanım Senaryoları

- **API Key'ler**: Harici servislere API erişimi
- **Servis Hesapları**: Mikroservisler arası iletişim
- **IoT Cihazlar**: Cihaz authentication
- **Webhook'lar**: Webhook doğrulama

## Güvenlik Notları

⚠️ **Üretim ortamı için:**
- Token'ları environment variable'larda saklayın
- HTTPS kullanın
- Token'ları düzenli olarak rotate edin
- Token'ları veritabanında şifreli saklayın
- Rate limiting ekleyin
