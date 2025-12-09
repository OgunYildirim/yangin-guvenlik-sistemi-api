# 🧪 Test Dokümantasyonu

## Sistem Bilgileri

### Servisler
- **Backend (Flask API)**: http://localhost:5000
- **Frontend (Web UI)**: http://localhost:3000

### Demo Kullanıcılar
| Kullanıcı | Şifre | Açıklama |
|-----------|-------|----------|
| admin | admin123 | Yönetici hesabı |
| operator | operator123 | Operatör hesabı |

---

## 🚀 Sistemi Başlatma

### Docker Compose ile
```powershell
# Servisleri başlat
docker-compose up -d

# Durumu kontrol et
docker-compose ps

# Logları görüntüle
docker-compose logs -f

# Servisleri durdur
docker-compose down
```

---

## 🧪 API Test Senaryoları

### 1. Sistem Durumu Kontrolü (Public Endpoint)

**Endpoint:** `GET /api/durum`

```powershell
curl http://localhost:5000/api/durum
```

**Beklenen Yanıt:**
```json
{
  "AlarmSistemi": {
    "durum": "Hazır"
  },
  "SprinklerSistemi": {
    "durum": "Hazır"
  }
}
```

---

### 2. Kullanıcı Girişi (Login)

**Endpoint:** `POST /api/login`

```powershell
$body = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/login -ContentType "application/json" -Body $body
```

**Beklenen Yanıt:**
```json
{
  "mesaj": "Giriş başarılı",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "kullanici": "admin"
}
```

---

### 3. JWT Token ile Yangın Protokolü Başlatma (Protected Endpoint)

**Endpoint:** `POST /api/yangin_uyarisi`  
**Authentication:** Bearer Token gerekli ✅

#### Adım 1: Login ve Token Alma
```powershell
$loginResponse = Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/login -ContentType "application/json" -Body (@{username="admin"; password="admin123"} | ConvertTo-Json)

$token = $loginResponse.access_token
Write-Host "Token alındı: $token"
```

#### Adım 2: Token ile Protokol Başlatma
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$body = @{
    kaynak = "Ana_Giris_Sensörü"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/yangin_uyarisi -Headers $headers -Body $body
```

**Beklenen Yanıt:**
```json
{
  "status": "OK",
  "protokol_baslatildi": true,
  "kaynak_sensör": "Ana_Giris_Sensörü",
  "islem_yapan_kullanici": "admin",
  "protokol_akisi": {
    "alarm": {
      "mesaj": "Alarm başarıyla çalıştırıldı",
      "durum": "Calisiyor"
    },
    "sprinkler_geri_bildirim": {
      "mesaj": "Su akışı başladı",
      "durum": "Calisiyor"
    },
    "kontrol_paneli_durumu": "İşlem tamamlandı: Alarm ve Sprinkler devreye alındı."
  }
}
```

---

### 4. Sistem Sıfırlama

**Endpoint:** `POST /api/sifirla`

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/sifirla
```

**Beklenen Yanıt:**
```json
{
  "mesaj": "Tüm yangın sistemleri sıfırlandı ve 'Hazır' durumuna getirildi."
}
```

---

## 🌐 Frontend Test Senaryoları

### 1. Login Testi

1. Tarayıcıda http://localhost:3000 adresini aç
2. Kullanıcı adı: `admin`
3. Şifre: `admin123`
4. "Giriş Yap" butonuna tıkla
5. ✅ Dashboard'a yönlendirilmeli

### 2. Sistem Durumu Görüntüleme

1. Dashboard'da iki kart görünmeli:
   - 🚨 Alarm Sistemi: ✅ Hazır
   - 💧 Sprinkler Sistemi: ✅ Hazır

### 3. Yangın Protokolü Başlatma

1. "Sensör Kaynağı" alanına bir isim gir (örn: `Test_Sensörü`)
2. "🔥 Yangın Protokolünü Başlat" butonuna tıkla
3. ✅ Toast bildirimi görünmeli
4. ✅ Aktivite günlüğünde kayıt oluşmalı
5. ✅ Sistem durumları "Çalışıyor" olarak güncellenmeli

### 4. Sistem Sıfırlama

1. "🔄 Sistemi Sıfırla" butonuna tıkla
2. ✅ Toast bildirimi görünmeli
3. ✅ Sistem durumları "Hazır" olarak güncellenmeli

### 5. Çıkış Yapma

1. Sağ üst köşedeki "Çıkış" butonuna tıkla
2. ✅ Login ekranına yönlendirilmeli
3. ✅ Token localStorage'dan silinmeli

---

## 🔒 JWT Token Testi

### Token Olmadan Protected Endpoint'e Erişim

```powershell
# Token olmadan istek gönder
Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/yangin_uyarisi -ContentType "application/json" -Body (@{kaynak="Test"} | ConvertTo-Json)
```

**Beklenen Sonuç:** ❌ 401 Unauthorized hatası

### Geçersiz Token ile Erişim

```powershell
$headers = @{
    "Authorization" = "Bearer invalid_token_here"
    "Content-Type" = "application/json"
}

Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/yangin_uyarisi -Headers $headers -Body (@{kaynak="Test"} | ConvertTo-Json)
```

**Beklenen Sonuç:** ❌ 422 Unprocessable Entity hatası

---

## 🐛 Hata Senaryoları

### 1. Yanlış Kullanıcı Adı/Şifre

```powershell
$body = @{
    username = "wrong_user"
    password = "wrong_pass"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/login -ContentType "application/json" -Body $body
```

**Beklenen Yanıt:** ❌ 401 Unauthorized
```json
{
  "mesaj": "Geçersiz kullanıcı adı veya şifre"
}
```

### 2. Eksik Parametreler

```powershell
# Şifre olmadan login denemesi
$body = @{
    username = "admin"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/login -ContentType "application/json" -Body $body
```

**Beklenen Yanıt:** ❌ 400 Bad Request
```json
{
  "mesaj": "Kullanıcı adı ve şifre gerekli"
}
```

---

## 📊 Performans Testleri

### Çoklu İstek Testi

```powershell
# 10 ardışık istek gönder
1..10 | ForEach-Object {
    $response = Invoke-RestMethod -Method Get -Uri http://localhost:5000/api/durum
    Write-Host "İstek $_: $($response.AlarmSistemi.durum)"
}
```

---

## 🔍 Docker Container Logları

### Backend Logları
```powershell
docker logs fire_safety_backend -f
```

### Frontend Logları
```powershell
docker logs fire_safety_frontend -f
```

### Tüm Loglar
```powershell
docker-compose logs -f
```

---

## ✅ Test Checklist

### Backend API
- [ ] GET /api/durum - Sistem durumu alınabiliyor
- [ ] POST /api/login - Başarılı login yapılabiliyor
- [ ] POST /api/login - Hatalı giriş reddediliyor
- [ ] POST /api/yangin_uyarisi - Token ile protokol başlatılabiliyor
- [ ] POST /api/yangin_uyarisi - Token olmadan erişim engelleniyor
- [ ] POST /api/sifirla - Sistem sıfırlanabiliyor

### Frontend UI
- [ ] Login sayfası düzgün görüntüleniyor
- [ ] Autocomplete devre dışı (otomatik doldurma yok)
- [ ] Başarılı login sonrası dashboard açılıyor
- [ ] Sistem durumları görüntüleniyor
- [ ] Yangın protokolü başlatılabiliyor
- [ ] Aktivite günlüğü çalışıyor
- [ ] Toast bildirimleri görünüyor
- [ ] Çıkış yapılabiliyor
- [ ] Responsive tasarım çalışıyor

### Docker & DevOps
- [ ] docker-compose up -d ile servisler başlıyor
- [ ] Her iki container da çalışıyor
- [ ] Port 5000 (backend) erişilebilir
- [ ] Port 3000 (frontend) erişilebilir
- [ ] Container'lar restart sonrası ayağa kalkıyor

---

## 📝 Notlar

- JWT token'ların geçerlilik süresi: **1 saat**
- Token süresi dolarsa otomatik olarak login ekranına yönlendirilir
- Sistem durumu her **5 saniyede** bir otomatik güncellenir
- Aktivite günlüğü maksimum **50 kayıt** tutar

---

## 🎯 Sonuç

Tüm testler başarılı olduğunda:
✅ Backend API çalışıyor  
✅ JWT Authentication aktif  
✅ Frontend UI çalışıyor  
✅ Docker servisleri stabil  
✅ Sistem production-ready!
