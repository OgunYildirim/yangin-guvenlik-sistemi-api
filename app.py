import time
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'yangin-sistemi-super-secret-key-2024'  # Üretimde environment variable kullanın!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)
CORS(app)  # Frontend'den gelen isteklere izin ver

# Basit kullanıcı veritabanı (gerçek uygulamada database kullanın)
USERS = {
    "admin": "admin123",
    "operator": "operator123"
}

# --- Sistem Bileşenleri (Sınıflar) ---

class AlarmSistemi:
    """Alarm sistemini temsil eder."""
    def __init__(self):
        self.durum = "Hazır"
    
    def calistir(self):
        """Alarmı aktive eder."""
        if self.durum == "Calisiyor":
            return {"mesaj": "Alarm zaten çalışıyor."}, 400
        
        self.durum = "Calisiyor"
        print("🚨 Alarm Sistemi: Yüksek sesli alarm çalıyor!")
        return {"mesaj": "Alarm başarıyla çalıştırıldı", "durum": self.durum}, 200

    def sifirla(self):
        """Alarmı sıfırlar."""
        self.durum = "Hazır"
        print("✅ Alarm Sistemi: Sıfırlandı.")

class SprinklerSistemi:
    """Su püskürtme/sprinkler sistemini temsil eder."""
    def __init__(self):
        self.durum = "Hazır"
    
    def su_puskurtmeye_basla(self):
        """Su püskürtme işlemini başlatır ve geri bildirim sağlar."""
        if self.durum == "Calisiyor":
            return {"mesaj": "Sprinkler zaten su püskürtüyor."}, 400
        
        self.durum = "Calisiyor"
        print("💧 Sprinkler Sistemi: Vana açılıyor...")
        time.sleep(1)  # Su akışının başlamasını simüle et
        
        geri_bildirim = {"mesaj": "Su akışı başladı", "durum": self.durum}
        print(f"💧 Sprinkler Sistemi -> Kontrol Paneli: {geri_bildirim['mesaj']}")
        
        return geri_bildirim, 200

    def durdur_ve_sifirla(self):
        """Sprinkler sistemini durdurur ve sıfırlar."""
        self.durum = "Hazır"
        print("✅ Sprinkler Sistemi: Durduruldu ve sıfırlandı.")

# Global bileşen örnekleri
alarm_sistemi = AlarmSistemi()
sprinkler_sistemi = SprinklerSistemi()

# --- Kontrol Paneli Mantığı ---

def yangin_protokolu_baslat(yangin_kaynagi="Sensör A"):
    """
    Kontrol Paneli'nin temel iş mantığını çalıştırır.
    """
    sonuclar = {}
    
    print(f"\n🔥 Kontrol Paneli: {yangin_kaynagi}'dan 'Yangın Var' uyarısı alındı.")
    
    # Alarmı etkinleştir
    alarm_sonucu, alarm_status = alarm_sistemi.calistir()
    sonuclar['alarm'] = alarm_sonucu
    
    # Sprinkler sistemini başlat
    sprinkler_komut = sprinkler_sistemi.su_puskurtmeye_basla()
    sonuclar['sprinkler_komut'] = sprinkler_komut[0]
    sonuclar['sprinkler_geri_bildirim'] = sprinkler_komut[0]
    
    # Kontrol paneli durumu
    durum_mesaji = "İşlem tamamlandı: Alarm ve Sprinkler devreye alındı."
    sonuclar['kontrol_paneli_durumu'] = durum_mesaji
    print(f"✅ Kontrol Paneli -> {yangin_kaynagi}: {durum_mesaji}")
    
    return sonuclar

# --- Flask REST Servis Uç Noktaları ---

@app.route('/api/login', methods=['POST'])
def login():
    """Kullanıcı girişi yapar ve JWT token döner."""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"mesaj": "Kullanıcı adı ve şifre gerekli"}), 400
    
    username = data['username']
    password = data['password']
    
    # Kullanıcı doğrulama
    if username in USERS and USERS[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify({
            "mesaj": "Giriş başarılı",
            "access_token": access_token,
            "kullanici": username
        }), 200
    else:
        return jsonify({"mesaj": "Geçersiz kullanıcı adı veya şifre"}), 401

@app.route('/api/yangin_uyarisi', methods=['POST'])
@jwt_required()  # Bu endpoint artık JWT token gerektirir
def yangin_uyarisi_al():
    """Sensörden gelen yangın uyarısını alır. (JWT Korumalı)"""
    current_user = get_jwt_identity()
    data = request.get_json(silent=True)
    kaynak = data.get('kaynak', 'Bilinmeyen Sensör') if data else 'Bilinmeyen Sensör'
    
    try:
        protokol_sonuclari = yangin_protokolu_baslat(kaynak)
        return jsonify({
            "status": "OK",
            "protokol_baslatildi": True,
            "kaynak_sensör": kaynak,
            "islem_yapan_kullanici": current_user,
            "protokol_akisi": protokol_sonuclari
        }), 200
    except Exception as e:
        return jsonify({"status": "Hata", "mesaj": str(e)}), 500

@app.route('/api/sifirla', methods=['POST'])
def sistemi_sifirla():
    """Sistemi manuel olarak sıfırlar."""
    alarm_sistemi.sifirla()
    sprinkler_sistemi.durdur_ve_sifirla()
    return jsonify({"mesaj": "Tüm yangın sistemleri sıfırlandı ve 'Hazır' durumuna getirildi."}), 200

@app.route('/api/durum', methods=['GET'])
def durumu_al():
    """Sistem bileşenlerinin durumunu gösterir."""
    return jsonify({
        "AlarmSistemi": {"durum": alarm_sistemi.durum},
        "SprinklerSistemi": {"durum": sprinkler_sistemi.durum}
    }), 200

# --- Uygulamayı başlatma ---

if __name__ == '__main__':
    print("--------------------------------------------------")
    print("🔥 Yangın Güvenlik Protokolü (Flask REST Servisi)")
    print("--------------------------------------------------")
    print("Servisler:")
    print("* POST /api/yangin_uyarisi: Protokolü başlatır.")
    print("* POST /api/sifirla: Sistemi sıfırlar.")
    print("* GET /api/durum: Sistemlerin durumunu sorgular.")
    print("--------------------------------------------------")
    
    # Kayıtlı tüm route'ları ve metodları yazdır
    print("\n🌐 Kayıtlı Uç Noktalar:")
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods - {"HEAD", "OPTIONS"})
        print(f"{rule.rule} [{methods}]")
    
    # Flask uygulamasını başlat
    app.run(host="0.0.0.0", port=5000, debug=True)
