import sqlite3
import pandas as pd

connection = sqlite3.connect('test.db')

data_read = pd.read_csv('data.csv')
data_read.to_sql('Data', connection, if_exists='replace', index=False)
cursor = connection.cursor()

# для начала отсортируем данные по убыванию количества лайков, чтобы выявить самую популярную фотографию.

for row in cursor.execute('SELECT * FROM Data ORDER BY likes DESC'):
    print(row)
print('')
# посмотрим, в какой час фотографии набирали больше лайков (будем сначала сортировать по количеству постов, а уже потом смотреть на сумму лайков)
for row in cursor.execute('SELECT COUNT(id) AS count, SUM(likes) AS sum_likes, SUM(likes)/COUNT(id) AS average, hour_of_publication FROM Data GROUP BY hour_of_publication ORDER BY average DESC'):
    print(row)
print('')
# посмотрим, в какой день недели (дни недели указаны цифрами, где воскресенье = 0) фотографии набирали больше лайков (будем сначала сортировать по количеству постов, а уже потом смотреть на сумму лайков)
for row in cursor.execute('SELECT COUNT(id) AS count, SUM(likes) AS sum_likes, SUM(likes)/COUNT(id) AS average, strftime("%w", date_of_publication) AS day from Data GROUP BY day ORDER BY average DESC'):
    print(row)
print('')
# проверим, влияет ли как-то количество дней между постами на количество лайков
for row in cursor.execute('SELECT COUNT(id) AS count, SUM(likes) AS sum_likes, SUM(likes)/COUNT(id) AS average, JULIANDAY(date_of_next_publication) - JULIANDAY(date_of_publication) AS date_difference from Data GROUP BY date_difference ORDER BY average DESC'):
    print(row)
connection.close()