# 🔐 JWT Token Authentication Örneği

## Açıklama

Bu örnek, **JWT (JSON Web Token)** kullanarak login tabanlı authentication gösterir.

### JWT Token Nedir?

- Login tabanlı (kullanıcı adı/şifre)
- Süre sınırlı token'lar
- Refresh token ile yenilenebilir
- Token içinde kullanıcı bilgisi taşır
- Stateless (server'da session tutmaz)
- Logout ile iptal edilebilir

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

Server `http://localhost:5002` adresinde çalışacak.

### 2. Client'ı Çalıştır (Başka bir terminalde)

```bash
python client.py
```

## Kullanıcılar

| Kullanıcı Adı | Şifre | Role |
|---------------|-------|------|
| admin | admin123 | admin |
| user1 | user123 | user |
| operator | operator123 | operator |

## Token Süreleri

- **Access Token**: 15 dakika
- **Refresh Token**: 30 gün

## Endpoints

### Public (Token Gerektirmez)
- `GET /api/public` - Herkese açık endpoint
- `POST /api/login` - Login (JWT token al)
- `GET /api/users` - Kullanıcı listesi

### Protected (JWT Token Gerekli)
- `GET /api/protected` - Token ile korunan endpoint
- `GET /api/profile` - Kullanıcı profili
- `GET /api/token-info` - Token bilgisi
- `POST /api/logout` - Logout (token iptal)

### Admin Only
- `GET /api/admin` - Admin yetkisi gerektirir

### Token Management
- `POST /api/refresh` - Refresh token ile yeni access token al

## Örnek Kullanım

### PowerShell

```powershell
# 1. Login
$loginBody = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Method Post -Uri http://localhost:5002/api/login -ContentType "application/json" -Body $loginBody

$accessToken = $loginResponse.access_token
$refreshToken = $loginResponse.refresh_token

# 2. Protected endpoint'e erişim
$headers = @{
    "Authorization" = "Bearer $accessToken"
}

Invoke-RestMethod -Uri http://localhost:5002/api/protected -Headers $headers

# 3. Token yenileme
$refreshHeaders = @{
    "Authorization" = "Bearer $refreshToken"
}

$newTokenResponse = Invoke-RestMethod -Method Post -Uri http://localhost:5002/api/refresh -Headers $refreshHeaders

# 4. Logout
Invoke-RestMethod -Method Post -Uri http://localhost:5002/api/logout -Headers $headers
```

### cURL

```bash
# 1. Login
curl -X POST http://localhost:5002/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 2. Protected endpoint (token ile)
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:5002/api/protected

# 3. Token yenileme
curl -X POST http://localhost:5002/api/refresh \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN"

# 4. Logout
curl -X POST http://localhost:5002/api/logout \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## JWT Token Akışı

```
1. Login
   Client → Server: username + password
   Server → Client: access_token + refresh_token

2. Protected Endpoint Erişimi
   Client → Server: Authorization: Bearer <access_token>
   Server → Client: Protected data

3. Token Yenileme (15 dakika sonra)
   Client → Server: Authorization: Bearer <refresh_token>
   Server → Client: new access_token

4. Logout
   Client → Server: Authorization: Bearer <access_token>
   Server: Token'ı iptal listesine ekle
```

## Özellikler

✅ Login tabanlı authentication  
✅ Access ve Refresh token sistemi  
✅ Token süre sınırı (15 dk / 30 gün)  
✅ Token yenileme mekanizması  
✅ Logout ve token iptali  
✅ Role-based access control  
✅ Token bilgisi sorgulama  

## Kullanım Senaryoları

- **Web Uygulamaları**: Kullanıcı login sistemi
- **Mobile Apps**: Güvenli API erişimi
- **SPA (Single Page Apps)**: Frontend authentication
- **Microservices**: Servisler arası güvenli iletişim

## Bearer Token vs JWT Token

| Özellik | Bearer Token | JWT Token |
|---------|--------------|-----------|
| Yapı | Statik string | JSON payload |
| Süre | Sınırsız | Sınırlı (15 dk) |
| Yenileme | Yok | Refresh token ile |
| Logout | Manuel iptal | Otomatik iptal |
| Kullanıcı Bilgisi | Yok | Token içinde |
| Kullanım | API keys | User sessions |

## Güvenlik Notları

⚠️ **Üretim ortamı için:**
- `JWT_SECRET_KEY`'i güçlü yapın ve environment variable kullanın
- HTTPS kullanın
- Token'ları güvenli saklayın (httpOnly cookies)
- Refresh token rotation uygulayın
- Rate limiting ekleyin
- Token iptal listesini Redis'te tutun

## Token Yapısı

JWT token 3 bölümden oluşur:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzOTU4MjQwMCwianRpIjoiYWJjZGVmIiwibmJmIjoxNjM5NTgyNDAwLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiYWRtaW4iLCJleHAiOjE2Mzk1ODMyMDB9.signature

Header.Payload.Signature
```

- **Header**: Token tipi ve algoritma
- **Payload**: Kullanıcı bilgileri ve claims
- **Signature**: Doğrulama imzası
