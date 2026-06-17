import bcrypt
from authx import AuthX, AuthXConfig

# Залишаємо конфігурацію AuthX без змін
config = AuthXConfig()
config.JWT_SECRET_KEY = "your-super-secret-key-change-me-in-production"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["headers"]

security = AuthX(config=config)


# Нова реалізація хешування без passlib
def get_password_hash(password: str) -> str:
    # Перетворюємо рядок у байти
    password_bytes = password.encode('utf-8')
    # Генеруємо сіль та хешуємо
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Повертаємо назад як звичайний рядок для збереження в БД
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Конвертуємо в байти чистий пароль та хеш з бази даних
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # Перевіряємо відповідність
    return bcrypt.checkpw(plain_bytes, hashed_bytes)