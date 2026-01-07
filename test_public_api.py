#!/usr/bin/env python3
"""
Public API Test Script
Open-Meteo API kullanarak hava durumu verilerini çeker ve yangın risk analizi yapar.
"""

import requests
import json

def test_weather_api():
    """
    Open-Meteo Public API'sini test eder.
    """
    print("=" * 60)
    print("PUBLIC API TEST - Open-Meteo Hava Durumu API")
    print("=" * 60)
    
    # Test konumları
    locations = [
        {"name": "İstanbul", "lat": 41.0082, "lon": 28.9784},
        {"name": "Ankara", "lat": 39.9334, "lon": 32.8597},
        {"name": "İzmir", "lat": 38.4237, "lon": 27.1428},
    ]
    
    for location in locations:
        print(f"\n📍 {location['name']} için hava durumu:")
        print("-" * 60)
        
        try:
            # Public API'ye istek at
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": location["lat"],
                    "longitude": location["lon"],
                    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                    "timezone": "auto"
                },
                timeout=10
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Veriyi parse et
            current = data.get("current", {})
            temperature = current.get("temperature_2m", 0)
            humidity = current.get("relative_humidity_2m", 0)
            wind_speed = current.get("wind_speed_10m", 0)
            
            print(f"🌡️  Sıcaklık: {temperature}°C")
            print(f"💧 Nem: {humidity}%")
            print(f"💨 Rüzgar: {wind_speed} km/h")
            
            # Basit yangın risk hesaplama
            risk_score = 0
            
            if temperature > 35:
                risk_score += 30
            elif temperature > 30:
                risk_score += 20
            elif temperature > 25:
                risk_score += 10
            
            if humidity < 30:
                risk_score += 25
            elif humidity < 50:
                risk_score += 15
            
            if wind_speed > 40:
                risk_score += 20
            elif wind_speed > 25:
                risk_score += 15
            
            if risk_score >= 70:
                risk_level = "🔴 KRİTİK"
            elif risk_score >= 50:
                risk_level = "🟠 YÜKSEK"
            elif risk_score >= 30:
                risk_level = "🟡 ORTA"
            else:
                risk_level = "🟢 DÜŞÜK"
            
            print(f"\n🔥 Yangın Risk Skoru: {risk_score}/100")
            print(f"📊 Risk Seviyesi: {risk_level}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Hatası: {e}")
        except Exception as e:
            print(f"❌ Genel Hata: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Test tamamlandı!")
    print("=" * 60)

def test_multiple_apis():
    """
    Farklı public API'leri test eder.
    """
    print("\n" + "=" * 60)
    print("EK PUBLIC API TESTLER")
    print("=" * 60)
    
    # 1. JSONPlaceholder - Fake REST API
    print("\n1️⃣ JSONPlaceholder API Testi:")
    print("-" * 60)
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=5)
        user = response.json()
        print(f"✅ Kullanıcı: {user.get('name')}")
        print(f"   Email: {user.get('email')}")
        print(f"   Şehir: {user.get('address', {}).get('city')}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    # 2. IP API - IP bilgisi
    print("\n2️⃣ IP API Testi:")
    print("-" * 60)
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        ip_data = response.json()
        print(f"✅ Public IP: {ip_data.get('ip')}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    # 3. Random User API
    print("\n3️⃣ Random User API Testi:")
    print("-" * 60)
    try:
        response = requests.get("https://randomuser.me/api/", timeout=5)
        user_data = response.json()
        user = user_data.get('results', [{}])[0]
        name = user.get('name', {})
        print(f"✅ Random Kullanıcı: {name.get('first')} {name.get('last')}")
        print(f"   Email: {user.get('email')}")
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    # Ana hava durumu API testi
    test_weather_api()
    
    # Ek API testleri
    test_multiple_apis()
    
    print("\n🎉 Tüm testler tamamlandı!")
    print("\n💡 Not: Bu script MCP server olmadan çalışır.")
    print("   Sadece Python 'requests' kütüphanesi kullanır.")
