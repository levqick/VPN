# Adaptive Behavioral Stealth VPN

MVP-проект интеллектуальной маскировки сетевого трафика. Репозиторий объединяет Go-прокси, Python ML API и Telegram-бота в один демонстрационный стек для исследования адаптивной обфускации трафика.

## Что есть в проекте

- `vpn-core` — TCP proxy на Go.
- `ml-engine` — ML API на FastAPI и скрипты подготовки/обучения модели.
- `tg-bot` — Telegram-бот для демонстрации пользовательского сценария.
## Что делает MVP

В текущей реализации Go-прокси слушает `127.0.0.1:8080` и пересылает трафик на `google.com:80`. Во время чтения данных обфускатор запрашивает у локального ML API параметры паттерна поведения и применяет задержку `jitter`, чтобы изменить ритм сетевого обмена.

ML-модуль обучает отдельные KDE-модели для профилей `web` и `video`, а Telegram-бот показывает, как эти параметры можно получать через пользовательский интерфейс.

## Ограничения текущей версии

- Это MVP, а не production-ready VPN.
- Целевой адрес в Go-части пока задан жестко.
- Профиль `video` вызывается напрямую.
- `padding_bytes` уже возвращается API, но еще не применяется в Go-обфускаторе.
- Датасет и модель генерируются локально из скриптов проекта.
- Полноценной интеграции с WireGuard, TUN/TAP и DPI-стендами в этом репозитории пока нет.

## Стек

- Go 1.26+
- Python 3.12+
- FastAPI
- scikit-learn
- pandas
- aiogram

## Структура репозитория

```text
.
├── ml-engine/
│   ├── api.py
│   ├── dataset_gen.py
│   ├── train.py
│   └── requirements.txt
├── tg-bot/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── vpn-core/
│   ├── main.go
│   ├── go.mod
│   ├── obfuscator/
│   └── proxy/
└── README.md
```

## Быстрый запуск

### 1. ML API

```bash
cd ml-engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python dataset_gen.py
python train.py
python api.py
```

API поднимется на `http://127.0.0.1:5000`.

### 2. Go proxy

В отдельном терминале:

```bash
cd vpn-core
go run .
```

Proxy начнет слушать `127.0.0.1:8080`.

### 3. Telegram-бот

В отдельном терминале:

```bash
cd tg-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Перед запуском укажи токен бота в `tg-bot/.env`.

## Подготовка репозитория к GitHub

В `.gitignore` уже исключены:

- виртуальные окружения;
- `.env` и другие локальные секреты;
- `__pycache__`;
- сгенерированные ML-артефакты;
- локальные служебные папки Codex;
- собранный Go-бинарник.

Это значит, что в GitHub можно публиковать только кодовую часть проекта, не выкладывая токены, локальный мусор и презентационные артефакты.
