# 🔐 Python Authentication Örnekleri

Bu klasör, Python ile **Bearer Token** ve **JWT Token** authentication örneklerini içerir.

## 📁 İçerik

### 1. Bearer Token (API Token) Örneği
```
bearer_token_example/
├── server.py          # Bearer token server
├── client.py          # Bearer token client
├── requirements.txt   # Gerekli paketler
└── README.md         # Detaylı açıklama
```

**Port**: 5001  
**Özellikler**: Statik API token'lar, basit ve hızlı

### 2. JWT Token Örneği
```
jwt_token_example/
├── server.py          # JWT token server
├── client.py          # JWT token client
├── requirements.txt   # Gerekli paketler
└── README.md         # Detaylı açıklama
```

**Port**: 5002  
**Özellikler**: Login tabanlı, süre sınırlı, refresh token

---

## 🚀 Hızlı Başlangıç

### Bearer Token Örneği

```bash
# 1. Klasöre git
cd bearer_token_example

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. Server'ı başlat
python server.py

# 4. Başka bir terminalde client'ı çalıştır
python client.py
```

### JWT Token Örneği

```bash
# 1. Klasöre git
cd jwt_token_example

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. Server'ı başlat
python server.py

# 4. Başka bir terminalde client'ı çalıştır
python client.py
```

---

## 🔍 Bearer Token vs JWT Token

### Bearer Token (API Token)

**Avantajlar:**
- ✅ Basit ve anlaşılır
- ✅ Hızlı implementasyon
- ✅ Düşük overhead
- ✅ API key'ler için ideal

**Dezavantajlar:**
- ❌ Süre sınırı yok
- ❌ Manuel iptal gerekir
- ❌ Kullanıcı bilgisi taşımaz
- ❌ Yenileme mekanizması yok

**Kullanım Alanları:**
- API key'ler
- Servis hesapları
- IoT cihazlar
- Webhook'lar
- Mikroservisler arası iletişim

---

### JWT Token

**Avantajlar:**
- ✅ Güvenli ve esnek
- ✅ Otomatik süre sınırı
- ✅ Refresh mekanizması
- ✅ Kullanıcı bilgisi taşır
- ✅ Stateless

**Dezavantajlar:**
- ❌ Daha karmaşık
- ❌ Token boyutu büyük
- ❌ Secret key yönetimi gerekir

**Kullanım Alanları:**
- Web uygulamaları
- Mobile apps
- SPA (Single Page Apps)
- Kullanıcı login sistemleri
- Session yönetimi

---

## 📊 Karşılaştırma Tablosu

| Özellik | Bearer Token | JWT Token |
|---------|--------------|-----------|
| **Yapı** | Rastgele string | JSON payload |
| **Süre** | Sınırsız | 15 dakika (access) |
| **Yenileme** | ❌ Yok | ✅ Refresh token |
| **Logout** | Manuel iptal | Otomatik iptal |
| **Kullanıcı Bilgisi** | ❌ Yok | ✅ Token içinde |
| **Karmaşıklık** | Düşük | Orta |
| **Güvenlik** | Orta | Yüksek |
| **Performans** | Yüksek | Orta |
| **Kullanım** | API keys | User sessions |

---

## 🎯 Hangi Yöntemi Seçmeliyim?

### Bearer Token Kullan:
- ✅ Basit API key sistemi gerekiyorsa
- ✅ Servisler arası iletişim için
- ✅ Uzun süreli erişim gerekiyorsa
- ✅ Hız kritikse

### JWT Token Kullan:
- ✅ Kullanıcı login sistemi gerekiyorsa
- ✅ Güvenlik öncelikse
- ✅ Token yenileme mekanizması gerekiyorsa
- ✅ Kullanıcı bilgisi taşınacaksa

---

## 🔒 Güvenlik En İyi Uygulamaları

### Her İki Yöntem İçin:
1. **HTTPS Kullan** - Token'ları şifreli ilet
2. **Rate Limiting** - Brute force saldırılarını önle
3. **Input Validation** - Girdi doğrulama yap
4. **Logging** - Tüm authentication işlemlerini logla

### Bearer Token İçin:
1. Token'ları environment variable'da sakla
2. Düzenli olarak rotate et
3. Veritabanında şifreli sakla
4. IP whitelist kullan

### JWT Token İçin:
1. Güçlü secret key kullan
2. Token süresini kısa tut
3. Refresh token rotation uygula
4. Token iptal listesi kullan (Redis)
5. httpOnly cookies kullan

---

## 📚 Ek Kaynaklar

- [RFC 6750 - Bearer Token](https://tools.ietf.org/html/rfc6750)
- [RFC 7519 - JWT](https://tools.ietf.org/html/rfc7519)
- [Flask-JWT-Extended Docs](https://flask-jwt-extended.readthedocs.io/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

---

## 🎓 Öğrenme Yolu

1. **Başlangıç**: Bearer Token örneğini incele
2. **Orta**: JWT Token örneğini incele
3. **İleri**: İki yöntemi karşılaştır
4. **Uygulama**: Kendi projenizde kullan

---

## 💡 İpuçları

- Her iki server'ı aynı anda çalıştırabilirsiniz (farklı portlarda)
- Client kodlarını kendi ihtiyaçlarınıza göre düzenleyin
- Production'da mutlaka HTTPS kullanın
- Token'ları güvenli saklayın

---

## 🤝 Katkıda Bulunma

Bu örnekleri geliştirmek için:
1. Kodu inceleyin
2. Testleri çalıştırın
3. İyileştirmeler yapın
4. Dokümantasyonu güncelleyin

---

**Not**: Bu örnekler eğitim amaçlıdır. Production ortamında ek güvenlik önlemleri alın.
