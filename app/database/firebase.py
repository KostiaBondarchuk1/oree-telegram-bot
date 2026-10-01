"""
Firebase Firestore integration module
"""
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from typing import Any, Dict, List, Optional
from datetime import datetime
from app.config import settings

logger = logging.getLogger(__name__)


class FirebaseDB:
    """Клас для роботи з Firebase Firestore"""
    
    def __init__(self):
        """Ініціалізація Firebase"""
        self.db = None
        self.init_firebase()
    
    def init_firebase(self):
        """Ініціалізує Firebase Admin SDK"""
        try:
            cred = credentials.Certificate(settings.get_firebase_config())
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            logger.info("✅ Firebase успішно ініціалізовано")
        except Exception as e:
            logger.error(f"❌ Помилка ініціалізації Firebase: {e}")
            raise
    
    # ==================== Ціни ====================
    def save_price_data(self, date: str, data: Dict[str, Any]) -> bool:
        """Зберігає дані цін для конкретної дати"""
        try:
            self.db.collection('prices').document(date).set({
                'data': data,
                'timestamp': datetime.now(),
                'date': date
            })
            logger.info(f"💾 Дані цін збережені для {date}")
            return True
        except Exception as e:
            logger.error(f"❌ Помилка при збереженні цін: {e}")
            return False
    
    def get_price_data(self, date: str) -> Optional[Dict]:
        """Отримує дані цін для конкретної дати"""
        try:
            doc = self.db.collection('prices').document(date).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"❌ Помилка при отриманні цін: {e}")
            return None
    
    def get_all_prices(self, limit: int = 30) -> List[Dict]:
        """Отримує останні ціни"""
        try:
            docs = self.db.collection('prices').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            logger.error(f"❌ Помилка при отриманні всіх цін: {e}")
            return []
    
    # ==================== Розрахунки ====================
    def save_calculation(self, date: str, calculation_data: Dict[str, Any]) -> bool:
        """Зберігає результати розрахунків"""
        try:
            self.db.collection('calculations').document(date).set({
                'data': calculation_data,
                'timestamp': datetime.now(),
                'date': date
            })
            logger.info(f"💾 Розрахунки збережені для {date}")
            return True
        except Exception as e:
            logger.error(f"❌ Помилка при збереженні розрахунків: {e}")
            return False
    
    def get_calculation(self, date: str) -> Optional[Dict]:
        """Отримує розрахунки для конкретної дати"""
        try:
            doc = self.db.collection('calculations').document(date).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"❌ Помилка при отриманні розрахунків: {e}")
            return None
    
    # ==================== Користувачі ====================
    def save_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """Зберігає дані користувача"""
        try:
            user_ref = self.db.collection('users').document(str(user_id))
            user_ref.set(user_data, merge=True)
            logger.info(f"💾 Користувач {user_id} збережений")
            return True
        except Exception as e:
            logger.error(f"❌ Помилка при збереженні користувача: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Отримує дані користувача"""
        try:
            doc = self.db.collection('users').document(str(user_id)).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"❌ Помилка при отриманні користувача: {e}")
            return None
    
    # ==================== Журнал моніторингу ====================
    def log_monitoring_event(self, event_type: str, message: str, data: Optional[Dict] = None) -> bool:
        """Логує подію моніторингу"""
        try:
            self.db.collection('monitoring_logs').add({
                'type': event_type,
                'message': message,
                'data': data or {},
                'timestamp': datetime.now()
            })
            return True
        except Exception as e:
            logger.error(f"❌ Помилка при логуванні événення: {e}")
            return False


# Глобальний екземпляр Firebase БД
db = FirebaseDB()
