"""
Моніторинг сайту ОРЕЕ
"""
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.config import settings
from app.scraper.parser import oree_parser
from app.database.firebase import db

logger = logging.getLogger(__name__)


class OREEMonitor:
    """Моніторинг сайту ОРЕЕ"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    async def check_prices(self):
        """Перевіряє ціни на ОРЕЕ сайту"""
        try:
            logger.info("🔍 Перевіряю ціни на ОРЕЕ...")
            
            prices_data = await oree_parser.parse_prices()
            
            if prices_data:
                today = datetime.now().strftime("%Y-%m-%d")
                
                # Зберігаємо в Firebase
                db.save_price_data(today, prices_data)
                
                # Логуємо в журнал
                db.log_monitoring_event(
                    event_type="price_check",
                    message="Ціни успішно отримані",
                    data=prices_data
                )
                
                logger.info(f"✅ Ціни для {today} збережені")
            else:
                db.log_monitoring_event(
                    event_type="price_check_error",
                    message="Не вдалось отримати ціни"
                )
                logger.warning("⚠️ Не вдалось отримати ціни")
        
        except Exception as e:
            logger.error(f"❌ Помилка при перевірці цін: {e}")
            db.log_monitoring_event(
                event_type="monitor_error",
                message=f"Помилка моніторингу: {str(e)}"
            )
    
    async def start(self):
        """Запускає моніторинг"""
        if self.is_running:
            logger.warning("⚠️ Моніторинг вже запущений")
            return
        
        try:
            # Одна перевірка при запуску
            await self.check_prices()
            
            # Додаємо періодичну задачу
            self.scheduler.add_job(
                self.check_prices,
                trigger=IntervalTrigger(seconds=settings.monitor_interval),
                id="oree_monitor",
                name="OREE Price Monitor",
                replace_existing=True
            )
            
            self.scheduler.start()
            self.is_running = True
            logger.info(f"✅ Моніторинг запущений (кожні {settings.monitor_interval} сек)")
        
        except Exception as e:
            logger.error(f"❌ Помилка при запуску моніторингу: {e}")
    
    async def stop(self):
        """Зупиняє моніторинг"""
        if not self.is_running:
            logger.warning("⚠️ Моніторинг не запущений")
            return
        
        try:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("✅ Моніторинг зупинений")
        except Exception as e:
            logger.error(f"❌ Помилка при зупинці моніторингу: {e}")


# Глобальний екземпляр монітору
monitor = OREEMonitor()
