"""
Bearer Token (API Token) Authentication Client
API token kullanarak server'a istek gönderen client örneği
"""

import requests
import json

# Server URL
BASE_URL = "http://localhost:5001/api"

# Mevcut API token'lar
TOKENS = {
    "admin": "api_token_admin_12345",
    "user": "api_token_user_67890",
    "service": "api_token_service_abcde"
}

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
    """Public endpoint'i test et (token gerektirmez)"""
    print_separator("1. PUBLIC ENDPOINT (Token Gerektirmez)")
    
    try:
        response = requests.get(f"{BASE_URL}/public")
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_protected_endpoint_without_token():
    """Protected endpoint'e token olmadan erişmeyi dene"""
    print_separator("2. PROTECTED ENDPOINT - Token Olmadan (Başarısız)")
    
    try:
        response = requests.get(f"{BASE_URL}/protected")
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_protected_endpoint_with_invalid_token():
    """Protected endpoint'e geçersiz token ile erişmeyi dene"""
    print_separator("3. PROTECTED ENDPOINT - Geçersiz Token (Başarısız)")
    
    headers = {
        "Authorization": "Bearer invalid_token_12345"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/protected", headers=headers)
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_protected_endpoint_with_valid_token():
    """Protected endpoint'e geçerli token ile eriş"""
    print_separator("4. PROTECTED ENDPOINT - Geçerli Token (Başarılı)")
    
    token = TOKENS['user']
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"Kullanılan Token: {token}")
    
    try:
        response = requests.get(f"{BASE_URL}/protected", headers=headers)
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_admin_endpoint_with_user_token():
    """Admin endpoint'e user token ile erişmeyi dene"""
    print_separator("5. ADMIN ENDPOINT - User Token (Yetkisiz)")
    
    token = TOKENS['user']
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"Kullanılan Token: {token} (user role)")
    
    try:
        response = requests.get(f"{BASE_URL}/admin", headers=headers)
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_admin_endpoint_with_admin_token():
    """Admin endpoint'e admin token ile eriş"""
    print_separator("6. ADMIN ENDPOINT - Admin Token (Başarılı)")
    
    token = TOKENS['admin']
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"Kullanılan Token: {token} (admin role)")
    
    try:
        response = requests.get(f"{BASE_URL}/admin", headers=headers)
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_generate_new_token():
    """Yeni API token oluştur"""
    print_separator("7. YENİ TOKEN OLUŞTURMA")
    
    data = {
        "user": "new_user",
        "role": "user"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-token",
            json=data
        )
        print_response(response)
        
        if response.status_code == 201:
            new_token = response.json().get('token')
            print(f"\n✅ Yeni token oluşturuldu!")
            print(f"Token: {new_token}")
            
            # Yeni token'ı test et
            print("\n📝 Yeni token'ı test ediyoruz...")
            headers = {"Authorization": f"Bearer {new_token}"}
            test_response = requests.get(f"{BASE_URL}/protected", headers=headers)
            print_response(test_response)
            
    except Exception as e:
        print(f"❌ Hata: {e}")

def test_list_tokens():
    """Mevcut token'ları listele"""
    print_separator("8. TOKEN LİSTESİ")
    
    try:
        response = requests.get(f"{BASE_URL}/list-tokens")
        print_response(response)
    except Exception as e:
        print(f"❌ Hata: {e}")

def main():
    """Ana test fonksiyonu"""
    print("\n" + "🔑" * 35)
    print("  Bearer Token (API Token) Authentication Client")
    print("🔑" * 35)
    
    print("\n📋 Kullanılacak Token'lar:")
    for role, token in TOKENS.items():
        print(f"  • {role}: {token}")
    
    # Testleri çalıştır
    test_public_endpoint()
    test_protected_endpoint_without_token()
    test_protected_endpoint_with_invalid_token()
    test_protected_endpoint_with_valid_token()
    test_admin_endpoint_with_user_token()
    test_admin_endpoint_with_admin_token()
    test_generate_new_token()
    test_list_tokens()
    
    print_separator("TEST TAMAMLANDI")
    print("\n✅ Tüm testler tamamlandı!")
    print("\n💡 Bearer Token Özellikleri:")
    print("  • Statik token'lar (değişmez)")
    print("  • Basit ve hızlı")
    print("  • Süre sınırı yok (manuel iptal gerekir)")
    print("  • API key'ler için ideal")
    print("  • Servisler arası iletişim için uygun")

if __name__ == "__main__":
    main()
