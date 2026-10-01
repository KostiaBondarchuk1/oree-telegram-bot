"""
Telegram Bot
"""
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import settings

logger = logging.getLogger(__name__)


class TelegramBot:
    """Telegram Bot"""
    
    def __init__(self):
        self.bot = Bot(token=settings.telegram_bot_token)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Налаштовує обробники команд"""
        
        @self.dp.message(Command("start"))
        async def cmd_start(message: types.Message):
            """Обробник команди /start"""
            await message.answer(
                "👋 Привіт! Я бот моніторингу цін ОРЕЕ.\n\n"
                "Команди:\n"
                "/prices - Останні ціни\n"
                "/calculate - Виконати розрахунки\n"
                "/status - Статус моніторингу\n"
                "/help - Допомога"
            )
        
        @self.dp.message(Command("help"))
        async def cmd_help(message: types.Message):
            """Обробник команди /help"""
            await message.answer(
                "📖 <b>Довідка</b>\n\n"
                "<b>/start</b> - Запуск бота\n"
                "<b>/prices</b> - Показати останні ціни\n"
                "<b>/calculate</b> - Виконати розрахунки\n"
                "<b>/status</b> - Статус моніторингу\n"
                "\n💡 Бот автоматично моніторить сайт ОРЕЕ кожні 5 хвилин",
                parse_mode="HTML"
            )
        
        @self.dp.message(Command("prices"))
        async def cmd_prices(message: types.Message):
            """Обробник команди /prices"""
            from app.database.firebase import db
            
            prices = db.get_all_prices(limit=5)
            
            if not prices:
                await message.answer("❌ Дані про ціни відсутні")
                return
            
            response = "📊 <b>Останні ціни:</b>\n\n"
            for price_doc in prices:
                response += f"📅 {price_doc.get('date', 'N/A')}\n"
            
            await message.answer(response, parse_mode="HTML")
        
        @self.dp.message(Command("status"))
        async def cmd_status(message: types.Message):
            """Обробник команди /status"""
            from app.scraper.monitor import monitor
            
            status = "✅ Моніторинг активний" if monitor.is_running else "❌ Моніторинг зупинений"
            
            await message.answer(
                f"<b>Статус боту:</b>\n\n"
                f"{status}\n"
                f"⏱️ Інтервал: {settings.monitor_interval} сек\n"
                f"🌐 Сайт: {settings.oree_url}",
                parse_mode="HTML"
            )
        
        @self.dp.message(Command("calculate"))
        async def cmd_calculate(message: types.Message):
            """Обробник команди /calculate"""
            await message.answer(
                "🧮 Функція розрахунків в розробці.\n"
                "Чекаємо формулу від адміністратора."
            )
    
    async def start_polling(self):
        """Запускає бота в режимі polling"""
        logger.info("🚀 Запускаю Telegram бота...")
        try:
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"❌ Помилка при запуску бота: {e}")
            raise
    
    async def stop(self):
        """Зупиняє бота"""
        logger.info("🛑 Зупиняю Telegram бота...")
        await self.bot.session.close()
