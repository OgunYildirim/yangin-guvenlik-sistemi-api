Yangın Güvenlik Protokolü (Flask REST Servisi)

Bu proje, bir Yangın Güvenlik Kontrol Paneli'nin temel mantığını simüle eden basit bir Flask RESTful servisidir. Sensörden gelen yangın uyarısını alır ve Alarm ile Sprinkler sistemlerini devreye sokar.

Kurulum ve Çalıştırma

Projenin Docker ve Docker Compose ile hızlıca kurulup çalıştırılması mümkündür.

1. Docker İmajı Oluşturma (Dockerfile Kullanımı)

Proje için Docker imajını aşağıdaki komut ile oluşturabilirsiniz:

docker build -t fire-safety-app .


2. Docker Compose ile Çalıştırma (Önerilen)

docker-compose up -d komutu, projeyi derleyip ayağa kaldırır ve 5000 portu üzerinden yayın yapmasını sağlar:

docker-compose up -d


Uygulama artık http://localhost:5000 adresinde erişilebilir durumdadır.

Kullanım Örnekleri (PowerShell/Invoke-RestMethod)

Uygulamanın API uç noktalarını (endpoints) test etmek için PowerShell'de (ya da VSC Terminalinde) aşağıdaki komutları kullanabilirsiniz:

A. Sistemi Sorgulama (GET /api/durum)

Sistem bileşenlerinin mevcut durumunu kontrol eder (Hazır veya Calisiyor).

curl http://localhost:5000/api/durum


B. Yangın Protokolünü Başlatma (POST /api/yangin_uyarisi)

Alarm ve Sprinkler sistemlerini devreye sokar.

Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/yangin_uyarisi -ContentType "application/json" -Body '{"kaynak": "Ana_Giris_Sensörü"}'


C. Sistemi Sıfırlama (POST /api/sifirla)

Sistemleri tekrar "Hazır" durumuna döndürür.

Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/sifirla