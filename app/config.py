"""
Конфігурація додатку
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Основні налаштування боту"""
    
    # Telegram
    telegram_bot_token: str
    admin_id: Optional[int] = None
    
    # Firebase
    firebase_project_id: str
    firebase_private_key_id: str
    firebase_private_key: str
    firebase_client_email: str
    firebase_client_id: str
    firebase_auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
    firebase_token_uri: str = "https://oauth2.googleapis.com/token"
    firebase_auth_provider_x509_cert_url: str = "https://www.googleapis.com/oauth2/v1/certs"
    firebase_client_x509_cert_url: str
    
    # Website Monitoring
    oree_url: str = "https://oree.com.ua/index.php/pricectr"
    monitor_interval: int = 300  # Кожні 5 хвилин
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_firebase_config(self) -> dict:
        """Повертає конфіг Firebase для ініціалізації"""
        return {
            "type": "service_account",
            "project_id": self.firebase_project_id,
            "private_key_id": self.firebase_private_key_id,
            "private_key": self.firebase_private_key.replace("\\n", "\n"),
            "client_email": self.firebase_client_email,
            "client_id": self.firebase_client_id,
            "auth_uri": self.firebase_auth_uri,
            "token_uri": self.firebase_token_uri,
            "auth_provider_x509_cert_url": self.firebase_auth_provider_x509_cert_url,
            "client_x509_cert_url": self.firebase_client_x509_cert_url,
        }


# Глобальний екземпляр налаштувань
settings = Settings()
