# Система учёта электроинструмента на предприятии

Учебное Flask-приложение для темы 7: учёт электроинструмента на предприятии.

## Возможности

- добавление электроинструмента с инвентарным номером;
- просмотр и фильтрация инструментов;
- выдача инструмента сотруднику;
- возврат инструмента на склад;
- отправка инструмента в ремонт;
- JSON-эндпоинт для получения списка инструментов.

## Технологии

- Python 3;
- Flask;
- SQLite;
- HTML;
- CSS.

## Структура

```text
electrotool-accounting-app/
├── app.py
├── database.py
├── GITHUB_UPLOAD.md
├── requirements.txt
├── schema.sql
├── electrotools.db
├── docs/
│   ├── README.md
│   ├── otchet_zadaniya_2-4.md
│   ├── otchet_zadaniya_2-4.docx
│   └── screenshots/
│       └── main.png
├── templates/
│   └── index.html
└── static/
    └── styles.css
```

## Запуск

```bash
pip install -r requirements.txt
python app.py
```

После запуска сайт доступен по адресу `http://127.0.0.1:5000/`.

## Документация для сдачи

Отчёт по заданиям 2-4 находится в папке `docs/`.

## API-пример

Получить список инструментов в JSON:

```http
GET /api/tools
```

Получить только инструменты на складе:

```http
GET /api/tools?status=in_stock
```
