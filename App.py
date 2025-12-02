import time
from flask import Flask, jsonify, request

app = Flask(__name__)

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
        time.sleep(1)
        
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
    
    # 2. Alarmı başlat
    alarm_sonucu, alarm_status = alarm_sistemi.calistir()
    sonuclar['alarm'] = alarm_sonucu
    
    # 3. Sprinkler sistemi başlasın
    sprinkler_komut = sprinkler_sistemi.su_puskurtmeye_basla()
    sonuclar['sprinkler_komut'] = sprinkler_komut[0]
    
    # 4. Sprinkler geri bildirim
    sonuclar['sprinkler_geri_bildirim'] = sprinkler_komut[0]
    
    # 5. Genel durum
    durum_mesaji = "İşlem tamamlandı: Alarm ve Sprinkler devreye alındı."
    sonuclar['kontrol_paneli_durumu'] = durum_mesaji
    print(f"✅ Kontrol Paneli -> {yangin_kaynagi}: {durum_mesaji}")
    
    return sonuclar

# --- Flask REST Servis Uç Noktaları ---

@app.route('/api/yangin_uyarisi', methods=['POST'])
def yangin_uyarisi_al():
    """Sensörün kontrol paneline yangın uyarısı gönderdiği uç nokta."""
    data = request.get_json(silent=True)
    kaynak = data.get('kaynak', 'Bilinmeyen Sensör') if data else 'Bilinmeyen Sensör'
    
    try:
        protokol_sonuclari = yangin_protokolu_baslat(kaynak)
        return jsonify({
            "status": "OK",
            "protokol_baslatildi": True,
            "kaynak_sensör": kaynak,
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
    """Sistem bileşenlerinin mevcut durumunu gösterir."""
    return jsonify({
        "AlarmSistemi": {"durum": alarm_sistemi.durum},
        "SprinklerSistemi": {"durum": sprinkler_sistemi.durum}
    }), 200

# --- YENİ EKLENEN ENDPOINT (ÖDEV İÇİN) ---
@app.route('/api/ping', methods=['GET'])
def ping():
    """Servisin ayakta olup olmadığını kontrol eder."""
    return jsonify({
        "status": "running",
        "message": "Yangın Güvenlik Sistemi API çalışıyor."
    }), 200

# Uygulamayı başlatma
if __name__ == '__main__':
    print("--------------------------------------------------")
    print("🔥 Yangın Güvenlik Protokolü (Flask REST Servisi)")
    print("--------------------------------------------------")
    print("Servisler:")
    print("* POST /api/yangin_uyarisi: Protokolü başlatır.")
    print("* POST /api/sifirla: Sistemi sıfırlar.")
    print("* GET /api/durum: Sistemlerin durumunu sorgular.")
    print("* GET /api/ping: Health check endpointi.")
    print("--------------------------------------------------")
    
    app.run(debug=True, port=5000)
