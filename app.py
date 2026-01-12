import os
import time
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- KONFİGÜRASYON ---
# Docker-compose içindeki DATABASE_URL'i okur, yoksa yerel dener
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://myuser:mypassword@db:5432/mydatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'yangin-sistemi-super-secret-key-2024')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Eklentileri Başlat
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# --- VERİTABANI MODELLERİ ---
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)  # Not: Gerçek projede şifreler hash'lenmelidir!

# --- SİSTEM BİLEŞENLERİ (LOGIC) ---
class AlarmSistemi:
    def __init__(self):
        self.durum = "Hazır"
    
    def calistir(self):
        if self.durum == "Calisiyor":
            return {"mesaj": "Alarm zaten çalışıyor."}, 400
        self.durum = "Calisiyor"
        print("🚨 Alarm Sistemi: Yüksek sesli alarm çalıyor!")
        return {"mesaj": "Alarm başarıyla çalıştırıldı", "durum": self.durum}, 200

    def sifirla(self):
        self.durum = "Hazır"
        print("✅ Alarm Sistemi: Sıfırlandı.")

class SprinklerSistemi:
    def __init__(self):
        self.durum = "Hazır"
    
    def su_puskurtmeye_basla(self):
        if self.durum == "Calisiyor":
            return {"mesaj": "Sprinkler zaten su püskürtüyor."}, 400
        self.durum = "Calisiyor"
        print("💧 Sprinkler Sistemi: Vana açılıyor...")
        time.sleep(1)
        geri_bildirim = {"mesaj": "Su akışı başladı", "durum": self.durum}
        return geri_bildirim, 200

    def durdur_ve_sifirla(self):
        self.durum = "Hazır"
        print("✅ Sprinkler Sistemi: Durduruldu ve sıfırlandı.")

# Global örnekler
alarm_sistemi = AlarmSistemi()
sprinkler_sistemi = SprinklerSistemi()

# --- YARDIMCI FONKSİYONLAR ---
def yangin_protokolu_baslat(yangin_kaynagi="Sensör A"):
    sonuclar = {}
    print(f"\n🔥 Kontrol Paneli: {yangin_kaynagi}'dan 'Yangın Var' uyarısı alındı.")
    
    alarm_sonucu, _ = alarm_sistemi.calistir()
    sonuclar['alarm'] = alarm_sonucu
    
    sprinkler_komut, _ = sprinkler_sistemi.su_puskurtmeye_basla()
    sonuclar['sprinkler_komut'] = sprinkler_komut
    
    durum_mesaji = "İşlem tamamlandı: Alarm ve Sprinkler devreye alındı."
    sonuclar['kontrol_paneli_durumu'] = durum_mesaji
    return sonuclar

# --- API UÇ NOKTALARI (ROUTES) ---

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"mesaj": "Kullanıcı adı ve şifre gerekli"}), 400
    
    # PostgreSQL üzerinden kullanıcı kontrolü
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    
    if user:
        access_token = create_access_token(identity=user.username)
        return jsonify({
            "mesaj": "Giriş başarılı",
            "access_token": access_token,
            "kullanici": user.username
        }), 200
    return jsonify({"mesaj": "Geçersiz kullanıcı adı veya şifre"}), 401

@app.route('/api/yangin_uyarisi', methods=['POST'])
@jwt_required()
def yangin_uyarisi_al():
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
    alarm_sistemi.sifirla()
    sprinkler_sistemi.durdur_ve_sifirla()
    return jsonify({"mesaj": "Tüm yangın sistemleri sıfırlandı."}), 200

@app.route('/api/durum', methods=['GET'])
def durumu_al():
    return jsonify({
        "AlarmSistemi": {"durum": alarm_sistemi.durum},
        "SprinklerSistemi": {"durum": sprinkler_sistemi.durum}
    }), 200

@app.route('/swagger.yaml', methods=['GET'])
def swagger_yaml():
    """Swagger/OpenAPI dokümantasyonunu döner"""
    try:
        with open('swagger.yaml', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/yaml'}
    except FileNotFoundError:
        return jsonify({"mesaj": "Swagger dokümantasyonu bulunamadı"}), 404

# --- BAŞLATMA VE DB OLUŞTURMA ---
if __name__ == '__main__':
    with app.app_context():
        # Veritabanı tablolarını oluştur (Postgres konteyneri hazır olduğunda)
        db.create_all()
        # Varsayılan kullanıcıyı ekle
        if not User.query.filter_by(username='admin').first():
            db.session.add(User(username='admin', password='admin123'))
            db.session.add(User(username='operator', password='operator123'))
            db.session.commit()
            print("✅ Veritabanı hazırlandı ve kullanıcılar eklendi.")

    app.run(host="0.0.0.0", port=5000)