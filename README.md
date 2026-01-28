# Video Voice Bot

Telegram-бот для конвертации видео в кружки (video note) и аудио в голосовые сообщения (voice).

## Функции

- Конвертация видео (mp4, mov, avi, mkv, webm) в Telegram Video Note (кружок)
- Конвертация аудио (mp3, wav, m4a, ogg, flac) в Telegram Voice Message (голосовое)
- Автоматическая обрезка видео до 60 секунд с предупреждением
- Очередь задач с ограничением параллельной обработки
- Информативные сообщения об ошибках и лимитах

## Требования

- Docker и Docker Compose
- Telegram Bot Token (получить у @BotFather)

Для локального запуска без Docker:
- Python 3.12+
- FFmpeg

## Быстрый старт с Docker Compose | Ubuntu

1. Клонировать репозиторий:

```bash
git clone https://github.com/YOUR_USERNAME/video-voice-bot.git
cd video-voice-bot
```

2. Создать файл .env:
```bash
cp .env.example .env
```

3. Отредактировать .env, вставив токен бота:
```env
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

4. Запустить:
```bash
docker compose up -d --build
```

5. Проверить логи:
```bash
docker compose logs -f
```

### Локальный запуск без DOCKER
1. Установить Python 3.12 и FFmpeg:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.12 python3.12-venv ffmpeg
# macOS
brew install python@3.12 ffmpeg
# Windows - скачать с официальных сайтов
```
2. Создать виртуальное окружение:
```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate  # Windows
```
3. Установить зависимости:
```bash
pip install -r requirements.txt
```
4. Создать .env и добавить токен:
```bash
cp .env.example .env
# отредактировать .env
```
5. Запустить:
```bash
python -m bot.main
```

### Ограничения Telegram
Максимальный размер входящего файла: 20 МБ
Максимальная длительность video note: 60 секунд
Video note должен быть квадратным (бот конвертирует автоматически)
Voice message должен быть в формате OGG Opus
### Типичные проблемы
## Бот не отвечает
Проверить токен в .env
Проверить логи: docker compose logs -f
Убедиться что бот запущен: docker compose ps
## Ошибка конвертации
Проверить что FFmpeg установлен: ffmpeg -version
Убедиться что файл не поврежден
Проверить размер файла (лимит 20 МБ)
## Кружок не отправляется
Видео длиннее 60 секунд обрезается автоматически
Размер результата может превышать лимиты Telegram
Попробовать видео меньшего разрешения или длительности
## Контейнер перезапускается
Проверить логи на ошибки
Убедиться в корректности токена
Проверить доступность сети

### Лицензия
MIT License - используйте как хотите.