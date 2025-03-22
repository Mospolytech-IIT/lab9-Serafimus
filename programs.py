'''Программы из задания.'''

from sqlalchemy import text
from sqlalchemy.orm import Session
from models import User, Post

def add_users(db: Session):
    '''Добавляет в базу данных три пользователя с разными атрибутами.'''
    users_to_add = [
        User(username='Alice', email='alice@mail.ru', password='password123'),
        User(username='Bob', email='bob@gmail.com.com', password='qwerty'),
        User(username='Charlie', email='charlie2@yandex.ru', password='mysecret')
    ]
    db.add_all(users_to_add)
    db.commit()

def add_posts(db: Session):
    '''Добавляет в базу данных три разных поста.'''
    alice = db.query(User).filter_by(username='Alice').first()
    bob = db.query(User).filter_by(username='Bob').first()

    posts_to_add = [
        Post(title='Первый пост Алисы', content='Содержание первого поста Алисы.', user=alice),
        Post(title='Привет от Боба', content='Это первый пост Боба!', user=bob),
        Post(title='Еще один пост Алисы', content='Продолжение мыслей Алисы.', user=alice)
    ]
    db.add_all(posts_to_add)
    db.commit()

def print_users(db: Session):
    '''Извлекает всех пользователей из базы данных и выводит информацию в консоль.'''
    users = db.query(User).all()
    print("Извлеченные из бд пользователи:")
    for user in users:
        print(f"Имя: {user.username}, почта: {user.email}, пароль: {user.password}")
    print()

def print_posts(db: Session):
    '''Извлекает все посты из базы данных и выводит информацию в консоль.'''
    posts = db.query(Post).all()
    print("Извлеченные из бд посты:")
    for post in posts:
        print(f"Заголовок: {post.title}, контент: {post.content}, "\
            f"автор: {post.user.username}, почта автора: {post.user.email}")
    print()

def print_posts_of_user(db: Session, username: str):
    '''Извлекает все посты пользователя с заданным именем и выводит информацию в консоль.'''
    user = db.query(User).filter_by(username=username).first()
    if user is None:
        print(f"Пользователь с именем {username} не найден.")
        return
    print(f"Посты пользователя {username}:")
    for post in user.posts:
        print(f"Заголовок: {post.title} контент: {post.content}")

def update_user_email(db: Session, username: str, new_email: str):
    '''Обновляет почту пользователя с заданным именем.'''
    user = db.query(User).filter_by(username=username).first()
    if user is None:
        print(f"Пользователь с именем {username} не найден.")
        return
    user.email = new_email
    db.commit()
    print(f"Почта пользователя {username} обновлена на {new_email}.")

def update_post_content(db: Session, post_id: int, new_content: text):
    '''Обновляет контент поста с заданным id.'''
    post = db.query(Post).filter_by(id=post_id).first()
    if post is None:
        print(f"Пост с id {post_id} не найден.")
        return
    post.content = new_content
    db.commit()
    print(f"Контент поста с id {post_id} обновлен на {new_content}.")

def delete_post(db: Session, post_id: int):
    '''Удаляет пост с заданным id.'''
    post = db.query(Post).filter_by(id=post_id).first()
    if post is None:
        print(f"Пост с id {post_id} не найден.")
        return
    db.delete(post)
    db.commit()
    print(f"Пост с id {post_id} удален.")

def delete_user(db: Session, username: str):
    '''Удаляет пользователя с заданным именем вместе со всеми его постами.'''
    user = db.query(User).filter_by(username=username).first()
    if user is None:
        print(f"Пользователь с именем {username} не найден.")
        return
    db.delete(user)
    db.commit()
    print(f"Пользователь {username} удален вместе со всеми его постами.")

def print_user(db: Session, username: str):
    '''Выводит информацию о пользователе по id.'''
    user = db.query(User).filter_by(username=username).first()
    if user is None:
        print(f"Пользователь с именем {username} не найден.")
        return
    print(f"Имя: {user.username}, почта: {user.email}, пароль: {user.password}")
