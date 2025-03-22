from sqlalchemy import URL

#config = URL.create(){
#    "postgresql+psycopg2",
#    username: "postgres",
#    password: "6438"
#    host: "localhost",
#    database: "learning"
#    query: {"driver": "PostgreSQL35W"}
#}

DB_URL = "postgresql+psycopg2://postgres:6438@localhost/learning"
