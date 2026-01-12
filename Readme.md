# 🔥 Yangın Güvenlik Protokolü Sistemi

Modern, JWT tabanlı authentication içeren full-stack yangın güvenlik kontrol paneli uygulaması.

## 📋 Özellikler

### Backend (Flask REST API)
- ✅ JWT Token tabanlı authentication
- ✅ Yangın protokolü yönetimi
- ✅ Alarm sistemi kontrolü
- ✅ Sprinkler sistemi kontrolü
- ✅ Sistem durumu sorgulama
- ✅ CORS desteği

### Frontend (Modern Web UI)
- ✅ Responsive ve modern tasarım
- ✅ Glassmorphism efektleri
- ✅ Gerçek zamanlı durum güncellemeleri
- ✅ JWT token yönetimi
- ✅ Aktivite günlüğü
- ✅ Toast bildirimleri

## 🚀 Hızlı Başlangıç

### Docker Compose ile Çalıştırma (Önerilen)

```bash
# Tüm servisleri başlat
docker-compose up -d

# Logları izle
docker-compose logs -f

# Servisleri durdur
docker-compose down
```

**Servis Adresleri:**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **Swagger UI:** http://localhost:5000/swagger.yaml (OpenAPI dokümantasyonu)
- **PostgreSQL:** localhost:5432 (myuser/mypassword)

**📚 Dokümantasyon:**
- **API Dokümantasyonu:** `swagger.yaml` - OpenAPI 3.0 formatında
- **Sistem Diyagramları:** `MERMAID.md` - MermaidJS ile görselleştirilmiş akışlar
- **Test Kılavuzu:** `TEST_GUIDE.md`

### Manuel Kurulum

#### Backend
```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı başlat
python app.py
```

#### Frontend
```bash
cd frontend

# Basit HTTP server ile çalıştır
python -m http.server 3000
# veya
npx serve -p 3000
```

## 🔐 Authentication

Sistem JWT (JSON Web Token) tabanlı authentication kullanır.

### Demo Kullanıcılar

| Kullanıcı Adı | Şifre | Rol |
|---------------|-------|-----|
| admin | admin123 | Yönetici |
| operator | operator123 | Operatör |

### Login İşlemi

**Endpoint:** `POST /api/login`

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "mesaj": "Giriş başarılı",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "kullanici": "admin"
}
```

## 📡 API Endpoints

### 🔓 Public Endpoints

#### Login
```bash
POST /api/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

#### Sistem Durumu
```bash
GET /api/durum
```

#### Sistem Sıfırlama
```bash
POST /api/sifirla
```

### 🔒 Protected Endpoints (JWT Token Gerekli)

#### Yangın Protokolü Başlatma
```bash
POST /api/yangin_uyarisi
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "kaynak": "Ana_Giris_Sensörü"
}
```

## 💻 Kullanım Örnekleri

### PowerShell ile Test

#### 1. Login ve Token Alma
```powershell
$loginResponse = Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/login -ContentType "application/json" -Body '{"username": "admin", "password": "admin123"}'
$token = $loginResponse.access_token
Write-Host "Token: $token"
```

#### 2. Sistem Durumu Sorgulama
```powershell
Invoke-RestMethod -Method Get -Uri http://localhost:5000/api/durum
```

#### 3. Yangın Protokolü Başlatma (JWT Token ile)
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/yangin_uyarisi -Headers $headers -Body '{"kaynak": "Ana_Giris_Sensörü"}'
```

#### 4. Sistem Sıfırlama
```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/sifirla
```

### cURL ile Test

#### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### Yangın Protokolü (Token ile)
```bash
curl -X POST http://localhost:5000/api/yangin_uyarisi \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"kaynak": "Ana_Giris_Sensörü"}'
```

## 🏗️ Proje Yapısı

```
YanginSistemi/
├── app.py                  # Backend Flask uygulaması
├── requirements.txt        # Python bağımlılıkları
├── Dockerfile             # Backend Docker image
├── docker-compose.yml     # Multi-container orchestration
├── swagger.yaml           # API dokümantasyonu
├── frontend/
│   ├── index.html        # Ana HTML dosyası
│   ├── styles.css        # Modern CSS tasarımı
│   ├── app.js            # Frontend JavaScript logic
│   ├── Dockerfile        # Frontend Docker image
│   └── nginx.conf        # Nginx yapılandırması
└── README.md             # Bu dosya
```

## 🔧 Teknoloji Stacki

### Backend
- **Flask** - Web framework
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5** - Yapı
- **CSS3** - Modern tasarım (Glassmorphism, Gradients, Animations)
- **Vanilla JavaScript** - İş mantığı
- **Nginx** - Web server (Docker)

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 🎨 Tasarım Özellikleri

- ✨ **Glassmorphism** efektleri
- 🌈 **Gradient** renk geçişleri
- 🎭 **Smooth animations** ve transitions
- 📱 **Responsive** tasarım
- 🌙 **Dark mode** tema
- 💫 **Micro-interactions**

## 🔒 Güvenlik Notları

⚠️ **Üretim Ortamı için Önemli:**

1. `app.py` içindeki `JWT_SECRET_KEY` değerini environment variable olarak ayarlayın
2. Gerçek bir veritabanı kullanın (şu an in-memory dictionary)
3. HTTPS kullanın
4. Rate limiting ekleyin
5. Güçlü şifreler kullanın
6. Token expiration sürelerini ihtiyaca göre ayarlayın

## 📝 Lisans

Bu proje eğitim amaçlıdır.

## 👨‍💻 Geliştirici Notları

### Backend Geliştirme
```bash
# Debug mode
python app.py

# Production mode
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Geliştirme
Frontend dosyalarını düzenledikten sonra tarayıcıyı yenileyin. Değişiklikler anında görünür.

### Docker İmajlarını Yeniden Oluşturma
```bash
docker-compose build --no-cache
docker-compose up -d
```

## 🐛 Sorun Giderme

### Backend'e bağlanılamıyor
- Backend servisinin çalıştığından emin olun: `docker-compose ps`
- Port 5000'in kullanılabilir olduğunu kontrol edin
- Firewall ayarlarını kontrol edin

### JWT Token hatası
- Token'ın süresi dolmuş olabilir (1 saat)
- Tekrar login olun

### CORS hatası
- Backend'de CORS ayarlarının doğru olduğundan emin olun
- Frontend'in doğru API URL'ini kullandığından emin olun

## 📞 İletişim

Sorularınız için issue açabilirsiniz.