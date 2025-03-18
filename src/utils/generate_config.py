import yaml
import os
import sys

SRC_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, SRC_DIR)

from logger import Logger


SHOW_LOG = True
logger = Logger(SHOW_LOG).get_logger(__name__)

def generate_config():
    """
    Считывает уже расшифрованный secrets.yml
    и на его основе генерирует config_secret.ini в корне репозитория.
    """
    # Определяем пути
    repo_root = os.path.dirname(SRC_DIR)
    secrets_file = os.path.join(repo_root, "secrets.yml")
    config_secret_file = os.path.join(repo_root, "config_secret.ini")

    # Получаем секреты
    try:
        with open(secrets_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Ошибка чтения {secrets_file}", exc_info=True)
        sys.exit(1)

    # Ожидаем, что data содержит ключи вида:
    #   db_host, db_port, db_user, db_password, db_name
    required_keys = ["db_host", "db_port", "db_user", "db_password", "db_name"]
    for key in required_keys:
        if key not in data:
            logger.error(f"В {secrets_file} отсутствует ключ '{key}'")
            sys.exit(1)

    # Формируем содержимое для config_secret.ini
    lines = [
        "[DATABASE]",
        f"host = {data['db_host']}",
        f"port = {data['db_port']}",
        f"user = {data['db_user']}",
        f"password = {data['db_password']}",
        f"name = {data['db_name']}",
        ""
    ]

    # Записываем config_secret.ini
    try:
        with open(config_secret_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        logger.info(f"Успешно сгенерирован {config_secret_file}")
    except Exception as e:
        logger.error(f"Ошибка при записи {config_secret_file}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    generate_config()