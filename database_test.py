import psycopg2

connection = psycopg2.connect(database="mydatabase",
                              host="localhost",
                              user="arch",
                              password="",
                              port=5432)

print(connection.status)
db = connection.cursor()
print(db)
db.execute("DROP TABLE website")
# db.execute("DROP TABLE job")
db.execute(
    "CREATE TABLE website \
          ( id SERIAL PRIMARY KEY, \
          name VARCHAR(255), \
          url VARCHAR(255) \
          );"
)
db.execute(
    "CREATE TABLE job \
    ( id SERIAL PRIMARY KEY, \
    website_id INT NOT NULL, \
    title TEXT NOT NULL, \
    content TEXT NOT NULL, \
    CONSTRAINT fk_website FOREIGN KEY(website_id) REFERENCES website(id) \
    );"
)
db = connection.cursor()
db.execute(
    "INSERT INTO website (name, url) \
    VALUES ('archwiki', 'https://www.archwiki.com');"
)
db = connection.commit()

# CREATE TABLE article (
#   id SERIAL PRIMARY KEY,
#   author_id INT NOT NULL,
#   title TEXT NOT NULL,
#   content TEXT NOT NULL,
#   CONSTRAINT fk_author FOREIGN KEY(author_id) REFERENCES author(id)
# )

