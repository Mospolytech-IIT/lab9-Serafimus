'''Модуль 1 и 2 частей лабораторной работы.'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URL
from models import Base
from programs import add_users, add_posts, print_users, print_posts, print_posts_of_user,\
    update_user_email, update_post_content, delete_post, delete_user, print_user

# Подключение к базе данных и создание таблиц
engine = create_engine(url=DB_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(autoflush=False, bind=engine)

db = Session()

# Добавление данных:

# Добавление пользователей в базу
add_users(db)
# Добавление постов в базу
add_posts(db)

# Извлечение данных:

# Извлечение пользователей из базы
print_users(db)
# Извлечение постов со связанными с ними пользователями
print_posts(db)
# Извлечение записей Posts, созданных конкретным пользователем
print_posts_of_user(db, "Alice")


# Обновление данных:

# Обновление почты пользователя
update_user_email(db, "Alice", "greetAccel2942@gmail.com")
print_user(db, "Alice")
print("\nИнфо о пользователе после обновления:")
print_user(db, "Alice")
# Обновление контента поста
update_post_content(db, 1,
"Мне захотелось изменить содержание этого поста. Теперь оно будет такое.")
print("\nПосты после обновления:")
print_posts(db)

# Удаление данных

# Удаление поста
print("\n\nПосты до удаления: ")
print_posts(db)
delete_post(db, 2)
print("\nПосты после удаления")
# Удаление пользователя вместе со всеми его постами
print("\n\nПользователи до удаления:\n")
print_users(db)
print("Посты до удаления:\n")
print_posts(db)
delete_user(db, "Bob")
print("\n\nПользователи после удаления.")
print_users(db)
print("\n\nПосты после удаления.")
print_posts(db)
