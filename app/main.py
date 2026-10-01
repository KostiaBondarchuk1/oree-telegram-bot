"""
Головна точка входу додатку
"""
import asyncio
import logging
import sys
from app.config import settings
from app.bot.bot import TelegramBot
from app.scraper.monitor import monitor

# Налаштування логування
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Головна функція"""
    logger.info("="*50)
    logger.info("🚀 Запускаю OREE Telegram Bot")
    logger.info("="*50)
    
    try:
        # Ініціалізуємо бота
        bot = TelegramBot()
        logger.info("✅ Telegram бот ініціалізований")
        
        # Запускаємо моніторинг
        await monitor.start()
        logger.info("✅ Моніторинг запущений")
        
        # Запускаємо polling
        await bot.start_polling()
    
    except KeyboardInterrupt:
        logger.info("⏹️  Одержано сигнал прериватися")
        await monitor.stop()
    
    except Exception as e:
        logger.error(f"❌ Критична помилка: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("✅ Бот зупинений")
