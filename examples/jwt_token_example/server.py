"""
JWT Token Authentication Server
Login tabanlı JWT token authentication örneği
"""

from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from datetime import timedelta
from functools import wraps

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'super-secret-jwt-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)  # 15 dakika
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)    # 30 gün

jwt = JWTManager(app)

# Kullanıcı veritabanı (gerçek uygulamada database kullanılır)
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "email": "admin@example.com"
    },
    "user1": {
        "password": "user123",
        "role": "user",
        "email": "user1@example.com"
    },
    "operator": {
        "password": "operator123",
        "role": "operator",
        "email": "operator@example.com"
    }
}

# Token iptal listesi (gerçek uygulamada Redis kullanılır)
REVOKED_TOKENS = set()

# JWT token iptal kontrolü
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in REVOKED_TOKENS

# Role-based access control decorator
def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            user_data = USERS.get(current_user)
            
            if not user_data:
                return jsonify({"error": "Kullanıcı bulunamadı"}), 404
            
            if user_data['role'] != required_role and user_data['role'] != 'admin':
                return jsonify({
                    "error": f"Bu endpoint için {required_role} rolü gerekli",
                    "your_role": user_data['role']
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Public endpoint
@app.route('/api/public', methods=['GET'])
def public_endpoint():
    """Herkese açık endpoint"""
    return jsonify({
        "message": "Bu endpoint herkese açık",
        "info": "JWT token gerektirmez"
    }), 200

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    """Kullanıcı girişi yapar ve JWT token döner"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Kullanıcı adı ve şifre gerekli"}), 400
    
    username = data['username']
    password = data['password']
    
    # Kullanıcı doğrulama
    if username not in USERS or USERS[username]['password'] != password:
        return jsonify({"error": "Geçersiz kullanıcı adı veya şifre"}), 401
    
    # JWT token oluştur
    access_token = create_access_token(
        identity=username,
        additional_claims={"role": USERS[username]['role']}
    )
    refresh_token = create_refresh_token(identity=username)
    
    return jsonify({
        "message": "Giriş başarılı",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "username": username,
            "role": USERS[username]['role'],
            "email": USERS[username]['email']
        },
        "token_info": {
            "access_token_expires_in": "15 minutes",
            "refresh_token_expires_in": "30 days"
        }
    }), 200

# Token yenileme endpoint'i
@app.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh token kullanarak yeni access token alır"""
    current_user = get_jwt_identity()
    new_access_token = create_access_token(
        identity=current_user,
        additional_claims={"role": USERS[current_user]['role']}
    )
    
    return jsonify({
        "message": "Token yenilendi",
        "access_token": new_access_token
    }), 200

# Protected endpoint
@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected_endpoint():
    """JWT token ile korunan endpoint"""
    current_user = get_jwt_identity()
    user_data = USERS.get(current_user)
    
    return jsonify({
        "message": "JWT token ile korunan endpoint'e erişildi",
        "user": current_user,
        "role": user_data['role'],
        "email": user_data['email']
    }), 200

# Admin endpoint
@app.route('/api/admin', methods=['GET'])
@jwt_required()
@require_role('admin')
def admin_endpoint():
    """Admin rolü gerektiren endpoint"""
    current_user = get_jwt_identity()
    
    return jsonify({
        "message": "Admin endpoint'ine erişildi",
        "user": current_user,
        "sensitive_data": "Bu veri sadece admin'ler görebilir",
        "all_users": list(USERS.keys())
    }), 200

# User profil endpoint'i
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Kullanıcı profil bilgilerini döner"""
    current_user = get_jwt_identity()
    user_data = USERS.get(current_user)
    
    return jsonify({
        "username": current_user,
        "email": user_data['email'],
        "role": user_data['role']
    }), 200

# Logout endpoint'i
@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    """JWT token'ı iptal eder"""
    jti = get_jwt()["jti"]
    REVOKED_TOKENS.add(jti)
    
    return jsonify({
        "message": "Başarıyla çıkış yapıldı",
        "info": "Token iptal edildi"
    }), 200

# Token bilgisi endpoint'i
@app.route('/api/token-info', methods=['GET'])
@jwt_required()
def token_info():
    """Mevcut token hakkında bilgi döner"""
    current_user = get_jwt_identity()
    jwt_data = get_jwt()
    
    return jsonify({
        "user": current_user,
        "token_type": jwt_data.get("type"),
        "jti": jwt_data.get("jti"),
        "exp": jwt_data.get("exp"),
        "role": jwt_data.get("role")
    }), 200

# Kullanıcı listesi (demo amaçlı)
@app.route('/api/users', methods=['GET'])
def list_users():
    """Kullanıcı listesini döner (demo amaçlı)"""
    return jsonify({
        "users": [
            {
                "username": username,
                "role": data['role'],
                "email": data['email']
            }
            for username, data in USERS.items()
        ]
    }), 200

if __name__ == '__main__':
    print("=" * 70)
    print("🔐 JWT Token Authentication Server")
    print("=" * 70)
    print("\n👥 Kullanıcılar:")
    for username, data in USERS.items():
        print(f"  • {username} / {data['password']} ({data['role']})")
    
    print("\n🌐 Endpoints:")
    print("  • GET  /api/public      - Public (token gerektirmez)")
    print("  • POST /api/login       - Login (JWT token al)")
    print("  • POST /api/refresh     - Token yenile")
    print("  • GET  /api/protected   - Protected (JWT gerekli)")
    print("  • GET  /api/admin       - Admin (admin JWT gerekli)")
    print("  • GET  /api/profile     - Profil bilgisi")
    print("  • POST /api/logout      - Logout (token iptal)")
    print("  • GET  /api/token-info  - Token bilgisi")
    print("  • GET  /api/users       - Kullanıcı listesi")
    
    print("\n⏱️  Token Süreleri:")
    print("  • Access Token: 15 dakika")
    print("  • Refresh Token: 30 gün")
    
    print("\n💡 Kullanım:")
    print('  1. Login: curl -X POST http://localhost:5002/api/login \\')
    print('       -H "Content-Type: application/json" \\')
    print('       -d \'{"username":"admin","password":"admin123"}\'')
    print('  2. Protected: curl -H "Authorization: Bearer <token>" \\')
    print('       http://localhost:5002/api/protected')
    
    print("\n" + "=" * 70)
    print("🚀 Server başlatılıyor: http://localhost:5002")
    print("=" * 70 + "\n")
    
    app.run(host='0.0.0.0', port=5002, debug=True)
