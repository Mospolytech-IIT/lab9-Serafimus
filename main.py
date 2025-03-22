'''Веб приложение с CRUD операциями.'''

from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URL
from models import User, Post, Base

engine = create_engine(url=DB_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(autoflush=False, bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    '''Корневой маршрут с навигацией.'''
    html = '<ul> \
          <li><a href="/users">Список пользователей</a></li> \
          <li><a href="/posts">Список постов</a></li> \
        </ul>'
    return HTMLResponse(content=html)

@app.get("/users")
def read_users():
    '''Отображает список пользователей.'''
    with Session() as db:
        users = db.query(User).all()
        users_html="<h2>Пользователи</h2><a href='/pages/create_user'>Добавить пользователя</a><ul>"
        for user in users:
            users_html += f"""<li>{user.username} - {user.email} - {user.id}
                <a href='/pages/edit_user/{user.id}'>Редактировать</a>
                <form method="post" action="/users/delete/{user.id}" style="display:inline;">
                <button type="submit">Удалить</button>
                </form></li>
                """
        users_html += """</ul><a href="/">Назад</a>"""
        return HTMLResponse(content=users_html)

@app.get("/pages/edit_user/{user_id}")
def edit_user_form(user_id: int):
    '''Возвращает страницу с формой редактирования пользователя.'''
    with Session() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return HTMLResponse(content=f"""
            <h2>Редактирование пользователя</h2>
            <form method="post" action="/users?user_id={user.id}">
                <input type="text" name="username" value="{user.username}" required>
                <input type="email" name="email" value="{user.email}" required>
                <input type="text" name="password" value="{user.password}" required>
                <button type="submit">Сохранить</button>
            </form>
            <a href="/users">Назад</a>""")

@app.post("/users")
def update_user(user_id: int, username: str = Form(...), email: str = Form(...)):
    '''Обновляет данные о пользователе.'''
    with Session() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.username = username
        user.email = email
        db.commit()
        return RedirectResponse(url="/users", status_code=303)

@app.post("/users/delete/{user_id}")
def delete_user(user_id: int):
    '''Удаляет пользователя.'''
    with Session() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        return RedirectResponse(url="/users", status_code=303)

@app.post("/users")
def create_user(username: str = Form(...), email: str = Form(...), password: str = Form()):
    '''Создает пользователя и добавляет его в базу данных.'''
    with Session() as db:
        new_user = User(username=username, email=email, password=password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return RedirectResponse(url="/users")

@app.get("/posts")
def read_posts():
    '''Возвращает сраницу со списком всех постов.'''
    with Session() as db:
        posts = db.query(Post).all()
        posts_html = "<h2>Посты</h2><a href='/pages/create_post'>Создать пост</a><ul>"
        for post in posts:
            posts_html += f"""<li>
                <b>{post.title}</b><p>{post.content}</p>
                <a href='/posts/edit/{post.id}'>Edit</a>
                <form method="post" action="/posts/delete/{post.id}" style="display:inline;">
                <button type="submit">Удалить</button>
                </form>
                </li>
                """
        posts_html += """</ul><a href="/">Назад</a>"""
        return HTMLResponse(content=posts_html)


@app.get("/pages/edit_post/{post_id}")
def edit_post_form(post_id: int):
    '''Возвращает страницу с формой редактирования поста.'''
    with Session() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return HTMLResponse(content=f"""
            <h2>Редактирование поста</h2>
            <form method="post" action="/posts/edit/{post.id}">
            <label>Заголовок</label>
            <input type="text" name="title" value="{post.title}" required>
            <label>Содержание</label>
            <textarea name="content" required>{post.content}</textarea>
            <button type="submit">Сохранить</button></form>
            <a href="/posts">Назад</a>
            """)

@app.post("/posts/edit/{post_id}")
def update_post(post_id: int, title: str = Form(...), content: str = Form(...)):
    '''Редактирует пост.'''
    with Session() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        post.title = title
        post.content = content
        db.commit()
        return RedirectResponse(url="/posts", status_code=303)

@app.post("/posts/delete/{post_id}")
def delete_post(post_id: int):
    '''Удаляет пост.'''
    with Session() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        db.delete(post)
        db.commit()
        return RedirectResponse(url="/posts", status_code=303)

@app.get("/pages/create_user")
def create_user_page():
    '''Возвращает страницу с формой создания пользователя.'''
    return HTMLResponse(content="""
        <h2>Создание пользователя</h2>
        <form method="post" action="/users">
            <input type="text" name="username" placeholder="Username" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Добавить</button>
        </form>
        <a href="/users">Назад</a>""")

@app.get("/pages/create_post")
def create_post_page():
    '''Возвращает страницу с формой создания поста.'''
    return HTMLResponse(content="""
        <h2>Создание поста</h2>
        <form method="post" action="/posts">
            <input type="text" name="title" placeholder="Title" required>
            <textarea name="content" placeholder="Content" required></textarea>
            <input type="number" name="user_id" placeholder="User ID" required>
            <button type="submit">Добавить</button>
        </form>
        <a href="/posts">Назад</a>
    """)

@app.post("/posts/")
def create_post(title: str = Form(...), content: str = Form(...), user_id: int = Form(...)):
    '''Добавляет новый пост в базу данных.'''
    with Session() as db:
        new_post = Post(title=title, content=content, user_id=user_id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return RedirectResponse(url="/posts", status_code=303)
