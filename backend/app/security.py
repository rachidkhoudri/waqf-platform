"""
خدمات الأمان والمصادقة وتشفير كلمات المرور والتحقق الثنائي (2FA)
"""
import hashlib
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

# نظام حفظ رموز التحقق 2FA في الذاكرة المؤقتة
_otp_storage: Dict[str, Dict] = {}

def hash_password(password: str) -> str:
    """تشفير كلمة المرور باستخدام PBKDF2 المعتمد مع الملح العشوائي"""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """التحقق من كلمة المرور"""
    try:
        salt, stored_hash = hashed_password.split('$')
        computed_hash = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return secrets.compare_digest(stored_hash, computed_hash)
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """إنشاء رمز وصول JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """فك تشفير رمز الوصول"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def generate_otp(destination: str) -> str:
    """توليد رمز تحقق 2FA (6 أرقام) صالح لمدة 10 دقائق"""
    code = f"{secrets.randbelow(900000) + 100000}"
    _otp_storage[destination] = {
        "code": code,
        "expires_at": datetime.utcnow() + timedelta(minutes=10)
    }
    return code

def verify_otp(destination: str, code: str) -> bool:
    """التحقق من رمز 2FA المدخل"""
    entry = _otp_storage.get(destination)
    if not entry:
        return False
    if datetime.utcnow() > entry["expires_at"]:
        del _otp_storage[destination]
        return False
    if entry["code"] == code:
        del _otp_storage[destination]
        return True
    return False

