# Система обработки жалоб клиентов (FastAPI)

## Описание

Этот проект реализует REST API для приёма и анализа клиентских жалоб с использованием:

- внешнего API для анализа тональности (Sentiment Analysis by APILayer),
- классификации текста через OpenAI GPT-3.5,
- (опционально) спам-фильтрации через API Ninjas,
- хранения жалоб в базе данных SQLite,
- автоматизации обработки через n8n (Telegram-уведомления, Google Sheets и др).

## Установка и запуск

### Установка зависимостей

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourname/complaints-api.git
   cd complaints-api
   ```

2. Запустите install.bat:
   ```bash
   install.bat
   ```

3. Активируйте виртуальное окружение:
   ```bash
   .venv\Scripts\activate
   ```

4. Запустите сервер:
   ```bash
   uvicorn app.main:app --reload
   ```

## Переменные окружения

Создайте файл `.env` со следующим содержанием:

```
APILAYER_KEY=your_apilayer_key
OPENAI_API_KEY=your_openai_key
PROFANITY_API_KEY=your_profanity_key
```

## Примеры Postman

- Метод: POST
- URL: http://localhost:8000/complaints
- Заголовки: Content-Type: application/json
- Тело запроса (JSON):
  ```json
  {
    "text": "Где мой кэшбэк? Уже неделя прошла!"
  }
  ```
## Пример запроса (curl)

```bash
curl -X POST http://localhost:8000/complaints \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"как узнать статус оплаты? она до сих пор не прошла\"}"
```

## Пример ответа

```json
{
  "id": 1,
  "status": "open",
  "sentiment": "neutral",
  "category": "оплата"
}
```

## API-эндпоинты

| Метод | URL                       | Описание                                                              |
|-------|---------------------------|-----------------------------------------------------------------------|
| POST  | /complaints               | Принимает жалобу, очищает текст, определяет тональность и категорию   |
| GET   | /complaints               | Возвращает список жалоб с возможностью фильтрации по статусу и дате   |
| PUT   | /complaints/{id}          | Обновляет статус жалобы (например, closed) по ID                      |



## Внешние API

- APILayer Sentiment Analysis
- OpenAI GPT-3.5 Turbo
- Profanity Filter by API Ninjas

## Интеграция с n8n

Скрипт интегрирован с n8n-автоматизацией. Для уведомлений используется Telegram-бот, созданный вручную через [@BotFather](https://t.me/BotFather).

### Telegram

- Бот создаётся самостоятельно.
- Его токен добавляется в n8n (узел Telegram).
- При поступлении жалоб с категорией "техническая" бот отправляет уведомление и статус жалобы меняется на `closed`.

### Google Sheets

- Жалобы с категорией "оплата" записываются в таблицу Google Sheets.
- После записи статус жалобы также меняется на `closed`.
- Для интеграции используется сервисный аккаунт и авторизация по OAuth2.
  - JSON-файл ключа сервисного аккаунта загружается в ноду Google Sheets в n8n.
  - Таблица должна быть заранее создана и доступ к ней должен быть предоставлен на email сервисного аккаунта.

### Общая логика n8n

1. Раз в час выполняется запрос `/complaints?status=open&from=<текущая дата -1 час>`.
2. В зависимости от категории выполняются действия:
   - `техническая` → закрытие → Telegram-уведомление
   - `оплата` → закрытие → запись в Google Sheets.
3. В конце вызывается PUT `/complaints/{id}?status=closed`.


## Контакты

Разработчик: **Anton Marusin**  

Email: MemphisAton@gmail.com

Telegram: [@MemphisAton](https://t.me/memphisaton)