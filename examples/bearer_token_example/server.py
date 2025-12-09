"""
Bearer Token (API Token) Authentication Server
Basit API token tabanlı authentication örneği
"""

from flask import Flask, request, jsonify
from functools import wraps
import secrets

app = Flask(__name__)

# Statik API token'ları (gerçek uygulamada database'de saklanır)
API_TOKENS = {
    "api_token_admin_12345": {"user": "admin", "role": "admin"},
    "api_token_user_67890": {"user": "user1", "role": "user"},
    "api_token_service_abcde": {"user": "service_account", "role": "service"}
}

# Decorator: Bearer token kontrolü
def require_bearer_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Authorization header'ı kontrol et
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Authorization header eksik"}), 401
        
        # Bearer token formatını kontrol et
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                return jsonify({"error": "Geçersiz authentication scheme"}), 401
        except ValueError:
            return jsonify({"error": "Geçersiz Authorization header formatı"}), 401
        
        # Token'ı doğrula
        if token not in API_TOKENS:
            return jsonify({"error": "Geçersiz API token"}), 401
        
        # Token bilgilerini request'e ekle
        request.current_user = API_TOKENS[token]
        
        return f(*args, **kwargs)
    
    return decorated_function

# Public endpoint - Token gerektirmez
@app.route('/api/public', methods=['GET'])
def public_endpoint():
    """Herkese açık endpoint"""
    return jsonify({
        "message": "Bu endpoint herkese açık",
        "info": "Bearer token gerektirmez"
    }), 200

# Protected endpoint - Bearer token gerektirir
@app.route('/api/protected', methods=['GET'])
@require_bearer_token
def protected_endpoint():
    """Bearer token ile korunan endpoint"""
    user_info = request.current_user
    return jsonify({
        "message": "Bearer token ile korunan endpoint'e erişildi",
        "user": user_info['user'],
        "role": user_info['role']
    }), 200

# Admin endpoint - Bearer token gerektirir
@app.route('/api/admin', methods=['GET'])
@require_bearer_token
def admin_endpoint():
    """Admin rolü gerektiren endpoint"""
    user_info = request.current_user
    
    # Admin kontrolü
    if user_info['role'] != 'admin':
        return jsonify({"error": "Bu endpoint için admin yetkisi gerekli"}), 403
    
    return jsonify({
        "message": "Admin endpoint'ine erişildi",
        "user": user_info['user'],
        "sensitive_data": "Bu veri sadece admin'ler görebilir"
    }), 200

# Yeni token oluşturma endpoint'i (demo amaçlı)
@app.route('/api/generate-token', methods=['POST'])
def generate_token():
    """Yeni API token oluşturur (demo amaçlı)"""
    data = request.get_json()
    
    if not data or 'user' not in data:
        return jsonify({"error": "Kullanıcı adı gerekli"}), 400
    
    # Yeni token oluştur
    new_token = f"api_token_{secrets.token_urlsafe(16)}"
    
    # Token'ı kaydet
    API_TOKENS[new_token] = {
        "user": data['user'],
        "role": data.get('role', 'user')
    }
    
    return jsonify({
        "message": "Yeni API token oluşturuldu",
        "token": new_token,
        "user": data['user'],
        "role": data.get('role', 'user'),
        "usage": f"Authorization: Bearer {new_token}"
    }), 201

# Token listesi (demo amaçlı)
@app.route('/api/list-tokens', methods=['GET'])
def list_tokens():
    """Mevcut token'ları listeler (demo amaçlı - üretimde olmamalı!)"""
    return jsonify({
        "message": "Mevcut API token'ları",
        "tokens": [
            {
                "token": token,
                "user": info['user'],
                "role": info['role']
            }
            for token, info in API_TOKENS.items()
        ]
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("🔑 Bearer Token (API Token) Authentication Server")
    print("=" * 60)
    print("\n📋 Mevcut API Token'ları:")
    for token, info in API_TOKENS.items():
        print(f"  • {info['user']} ({info['role']}): {token}")
    
    print("\n🌐 Endpoints:")
    print("  • GET  /api/public         - Public (token gerektirmez)")
    print("  • GET  /api/protected      - Protected (bearer token gerekli)")
    print("  • GET  /api/admin          - Admin (admin token gerekli)")
    print("  • POST /api/generate-token - Yeni token oluştur")
    print("  • GET  /api/list-tokens    - Token'ları listele")
    
    print("\n💡 Kullanım:")
    print('  curl -H "Authorization: Bearer api_token_admin_12345" http://localhost:5001/api/protected')
    
    print("\n" + "=" * 60)
    print("🚀 Server başlatılıyor: http://localhost:5001")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
