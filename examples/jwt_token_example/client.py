"""
JWT Token Authentication Client
Login yaparak JWT token alan ve kullanan client örneği
"""

import requests
import json
from datetime import datetime

# Server URL
BASE_URL = "http://localhost:5002/api"

# Global token storage
access_token = None
refresh_token = None

def print_separator(title=""):
    """Ayırıcı çizgi yazdır"""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)

def print_response(response):
    """HTTP response'u güzel formatta yazdır"""
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)

def test_public_endpoint():
    """Public endpoint'i test et"""
    print_separator("1. PUBLIC ENDPOINT (Token Gerektirmez)")
    
    try:
        response = requests.get(f"{BASE_URL}/public")
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_login(username, password):
    """Login yaparak JWT token al"""
    global access_token, refresh_token
    
    print_separator(f"2. LOGIN - {username}")
    
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            json=data
        )
        print_response(response)
        
        if response.status_code == 200:
            result = response.json()
            access_token = result.get('access_token')
            refresh_token = result.get('refresh_token')
            
            print(f"\n✅ Login başarılı!")
            print(f"Access Token: {access_token[:50]}...")
            print(f"Refresh Token: {refresh_token[:50]}...")
            
            return True
        else:
            print(f"\n❌ Login başarısız!")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_protected_endpoint_without_token():
    """Protected endpoint'e token olmadan erişmeyi dene"""
    print_separator("3. PROTECTED ENDPOINT - Token Olmadan (Başarısız)")
    
    try:
        response = requests.get(f"{BASE_URL}/protected")
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_protected_endpoint_with_token():
    """Protected endpoint'e JWT token ile eriş"""
    print_separator("4. PROTECTED ENDPOINT - JWT Token ile (Başarılı)")
    
    if not access_token:
        print("❌ Access token yok! Önce login yapın.")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/protected", headers=headers)
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_profile_endpoint():
    """Kullanıcı profil bilgilerini al"""
    print_separator("5. PROFILE ENDPOINT - Kullanıcı Bilgileri")
    
    if not access_token:
        print("❌ Access token yok! Önce login yapın.")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_token_info():
    """Token bilgilerini al"""
    print_separator("6. TOKEN INFO - Token Detayları")
    
    if not access_token:
        print("❌ Access token yok! Önce login yapın.")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/token-info", headers=headers)
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_admin_endpoint():
    """Admin endpoint'e erişmeyi dene"""
    print_separator("7. ADMIN ENDPOINT - Admin Yetkisi Gerekli")
    
    if not access_token:
        print("❌ Access token yok! Önce login yapın.")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/admin", headers=headers)
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_refresh_token():
    """Refresh token kullanarak yeni access token al"""
    global access_token
    
    print_separator("8. REFRESH TOKEN - Yeni Access Token Al")
    
    if not refresh_token:
        print("❌ Refresh token yok! Önce login yapın.")
        return
    
    headers = {
        "Authorization": f"Bearer {refresh_token}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/refresh", headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            result = response.json()
            old_token = access_token
            access_token = result.get('access_token')
            
            print(f"\n✅ Token yenilendi!")
            print(f"Eski Token: {old_token[:50]}...")
            print(f"Yeni Token: {access_token[:50]}...")
            
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_logout():
    """Logout yaparak token'ı iptal et"""
    global access_token, refresh_token
    
    print_separator("9. LOGOUT - Token İptali")
    
    if not access_token:
        print("❌ Access token yok! Önce login yapın.")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/logout", headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            print(f"\n✅ Logout başarılı! Token iptal edildi.")
            
            # Token'ları temizle
            old_access = access_token
            access_token = None
            refresh_token = None
            
            # İptal edilen token ile tekrar erişmeyi dene
            print("\n📝 İptal edilen token ile tekrar erişmeyi deniyoruz...")
            headers = {"Authorization": f"Bearer {old_access}"}
            test_response = requests.get(f"{BASE_URL}/protected", headers=headers)
            print_response(test_response)
            
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_expired_token_scenario():
    """Token süresi dolma senaryosu (simülasyon)"""
    print_separator("10. EXPIRED TOKEN SENARYOSU")
    
    print("💡 Gerçek senaryoda:")
    print("  1. Access token 15 dakika sonra sona erer")
    print("  2. Refresh token ile yeni access token alınır")
    print("  3. Refresh token 30 gün sonra sona erer")
    print("  4. Refresh token da sona ererse tekrar login gerekir")
    
    print("\n📝 Token yenileme akışı:")
    print("  Client → Server: Refresh Token")
    print("  Server → Client: Yeni Access Token")
    print("  Client: Yeni token ile isteklere devam eder")

def main():
    """Ana test fonksiyonu"""
    print("\n" + "🔐" * 35)
    print("  JWT Token Authentication Client")
    print("🔐" * 35)
    
    # Test senaryoları
    test_public_endpoint()
    test_protected_endpoint_without_token()
    
    # Admin kullanıcısı ile login
    print("\n" + "🔹" * 35)
    print("  SENARYO 1: Admin Kullanıcısı")
    print("🔹" * 35)
    
    if test_login("admin", "admin123"):
        test_protected_endpoint_with_token()
        test_profile_endpoint()
        test_token_info()
        test_admin_endpoint()
        test_refresh_token()
        test_logout()
    
    # Normal kullanıcı ile login
    print("\n" + "🔹" * 35)
    print("  SENARYO 2: Normal Kullanıcı")
    print("🔹" * 35)
    
    if test_login("user1", "user123"):
        test_protected_endpoint_with_token()
        test_profile_endpoint()
        test_admin_endpoint()  # Başarısız olmalı (yetkisiz)
        test_logout()
    
    # Token yenileme senaryosu
    test_expired_token_scenario()
    
    print_separator("TEST TAMAMLANDI")
    print("\n✅ Tüm testler tamamlandı!")
    
    print("\n💡 JWT Token Özellikleri:")
    print("  • Login tabanlı (kullanıcı adı/şifre)")
    print("  • Süre sınırlı (15 dakika access, 30 gün refresh)")
    print("  • Refresh token ile yenilenebilir")
    print("  • Logout ile iptal edilebilir")
    print("  • Token içinde kullanıcı bilgisi taşır")
    print("  • Stateless (server'da session tutmaz)")
    
    print("\n🔄 Bearer Token vs JWT Token:")
    print("  Bearer Token:")
    print("    ✓ Basit ve hızlı")
    print("    ✓ API key'ler için ideal")
    print("    ✗ Süre sınırı yok")
    print("    ✗ Manuel iptal gerekir")
    
    print("\n  JWT Token:")
    print("    ✓ Güvenli ve esnek")
    print("    ✓ Otomatik süre sınırı")
    print("    ✓ Refresh mekanizması")
    print("    ✓ Kullanıcı bilgisi taşır")
    print("    ✗ Daha karmaşık")

if __name__ == "__main__":
    main()
