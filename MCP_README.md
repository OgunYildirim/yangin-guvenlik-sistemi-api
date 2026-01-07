# Yangın Risk MCP Servisi

Bu MCP (Model Context Protocol) servisi yangın risk analizi yapar ve hava durumu verilerini kullanır.

## Özellikler

### 1. Tool Fonksiyonları

#### `add_numbers`
Basit toplama işlemi yapar.
```json
{
  "a": 5,
  "b": 3
}
```

#### `calculate_fire_risk`
Verilen parametrelere göre yangın risk skorunu hesaplar (0-100).
```json
{
  "temperature": 35,
  "humidity": 25,
  "wind_speed": 30,
  "building_type": "industrial",
  "has_fire_system": false
}
```

#### `get_weather_fire_risk`
**Public API Kullanımı**: Open-Meteo API'sinden gerçek zamanlı hava durumu verilerini çeker ve yangın risk analizi yapar.
```json
{
  "latitude": 41.0082,
  "longitude": 28.9784,
  "building_type": "commercial",
  "has_fire_system": true
}
```

### 2. Public API Entegrasyonu

Servis, **Open-Meteo API** kullanarak gerçek zamanlı hava durumu verilerini çeker:
- API URL: `https://api.open-meteo.com/v1/forecast`
- Ücretsiz, API key gerektirmez
- Python `requests` kütüphanesi kullanılır
- Sıcaklık, nem ve rüzgar hızı bilgilerini alır

## Kurulum

### 1. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 2. MCP Server'ı Çalıştır

```bash
python mcp_server.py
```

### 3. Claude Desktop ile Kullanım

Claude Desktop yapılandırma dosyasını düzenleyin:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "yangin-risk": {
      "command": "python",
      "args": ["C:\\Users\\oguny\\Desktop\\YanginSistemi\\mcp_server.py"]
    }
  }
}
```

### 4. Claude Desktop'ı Yeniden Başlatın

Yapılandırma değişikliklerinin etkili olması için Claude Desktop'ı kapatıp yeniden açın.

## Kullanım Örnekleri

### Örnek 1: Basit Toplama
```
İki sayıyı topla: 15 + 27
```

### Örnek 2: Yangın Risk Hesaplama
```
Sıcaklık 38°C, nem %20, rüzgar 35 km/h olan bir endüstriyel binada 
yangın söndürme sistemi yoksa yangın riski nedir?
```

### Örnek 3: Gerçek Zamanlı Hava Durumu + Risk Analizi
```
İstanbul (41.0082, 28.9784) için şu anki hava durumuna göre 
ticari bir binadaki yangın riskini hesapla.
```

## Risk Seviyeleri

- **LOW (0-29)**: Düşük risk - Standart güvenlik protokolleri
- **MODERATE (30-49)**: Orta risk - Rutin kontroller gerekli
- **HIGH (50-69)**: Yüksek risk - Önlemler gözden geçirilmeli
- **CRITICAL (70-100)**: Kritik risk - Acil önlem gerekli

## Teknik Detaylar

### Risk Hesaplama Faktörleri

1. **Sıcaklık**: 30°C üzeri yüksek risk
2. **Nem**: %30 altı yüksek risk
3. **Rüzgar**: 25 km/h üzeri yüksek risk
4. **Bina Tipi**: 
   - Residential (Konut): +5 puan
   - Commercial (Ticari): +10 puan
   - Industrial (Endüstriyel): +20 puan
5. **Yangın Sistemi**: Varsa %40 risk azaltma

### API Endpoint

```
GET https://api.open-meteo.com/v1/forecast
Parameters:
  - latitude: float
  - longitude: float
  - current: temperature_2m,relative_humidity_2m,wind_speed_10m
  - timezone: auto
```

## Test

### Manuel Test (Python)

```python
import requests

# Hava durumu API testi
response = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": 41.0082,
        "longitude": 28.9784,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto"
    }
)
print(response.json())
```

## Notlar

- MCP servisi stdio (standard input/output) üzerinden çalışır
- Claude Desktop ile entegre çalışır
- Public API kullanımı için internet bağlantısı gereklidir
- API rate limiting yoktur (Open-Meteo ücretsiz tier)

## Gereksinimler

- Python 3.8+
- mcp==0.9.0
- requests==2.31.0
- İnternet bağlantısı (Public API için)
