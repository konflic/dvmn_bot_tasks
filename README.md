# dvmn_bot_tasks

Бот для нотификаций о выполнении задач на dvmn.org

Для того чтобы начать работу нужно:

1. Настроить виртуальное окружение
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Создать в коре репозитория файл .env и прописать в нём следующие переменные:

```sh
DVMN_TOKEN=...
BOT_TOKEN=...
CHAT_ID=...
```

3. Запустить выполнение скрипта
```python main.py```