


import sqlalchemy

import psycopg2

from pprint import pprint


#
# engine = sqlalchemy.create_engine('postgresql://postgres:terzot13@localhost:5432/netology2021')
# pprint(engine)
#
# connection = engine.connect()
# print(connection)
# pprint(engine.table_names())
#
# Engine('postgresql://postgres:***@localhost:5432/netology2021')
# sqlalchemy.engine.base.Connection object at 0x000001562D6D33D0
# ['genre',
#  'artist_genre',
#  'artist',
#  'album_artist',
#  'album',
#  'track',
#  'collections',
#  'collections_album_track']
#
#     # Название и год выхода альбомов, вышедших в 2018 году
#
# select_1 = connection.execute('''SELECT  name, releasedate FROM album
# WHERE releasedate BETWEEN '2018-01-01' AND '2018-12-31';
# ''').fetchall()
# pprint(select_1)
#
# [('album_name_5', datetime.date(2018, 6, 14))]
#
#     # Название и продолжительность самого длительного трека
#
# select_2 = connection.execute('''SELECT   name, tracklength FROM track
# ORDER BY tracklength DESC;
# ''').fetchone()
# pprint(select_2)
#
# ('track_9', Decimal('5.50'))
#
#     # Название треков, продолжительность которых не менее 3,5 минуты
#
# select_3 = connection.execute('''SELECT  name FROM track
# WHERE tracklength >= 03.50;
# ''').fetchall()
# pprint(select_3)
#
#
# # Названия сборников, вышедших в период с 2018 по 2020 год включительно
# select_4 = connection.execute('''SELECT name FROM collections
# WHERE release_year BETWEEN '2018-01-01' AND '2020-12-31';
# ''').fetchall()
# pprint(select_4)
#
#
# # Исполнители, чье имя состоит из 1 слова
# select_5 = connection.execute('''SELECT name FROM artist
# WHERE name NOT LIKE '%% %%';
# ''').fetchall()
# pprint(select_5)
#
#
# # Название треков, которые содержат слово "мой"/"my"
# select_6 = connection.execute('''SELECT name FROM track
# WHERE name LIKE '%%my%%';
# ''').fetchall()
# pprint(select_6)

 # 1 количество исполнителей в каждом жанре;

select_2_1 = connection.execute('''SELECT DISTINCT name_artist FROM music_janre 
WHERE name in music_janre;'''
).fetchall()
pprint(select_2_1)

 # 2 количество треков, вошедших в альбомы 2019-2020 годов;

select_2_2 = connection.execute('''SELECT distinct name_track FROM album WHERE 
data_realise == 2019 and data_realise == 2020;'''
).fetchall()
pprint(select_2_2)

 # 3 средняя продолжительность треков по каждому альбому;
select_2_3 = ('''SELECT track_tracklegth FROM track
JOIN album on track.tracklength = album.name_album;''')
    select_2_3 = connection.execute('''SELECT name_track FROM album 
          WHERE AVG(tracklength);''').fetchall()
pprint(select_2_3)

# 4 все исполнители, которые не выпустили альбомы в 2020 году;

select_2_4 = connection.execute('''SELECT name FROM artist
join album on artist.name = album.name_album;'''
).fetchall()
     select_2_4 = connection.execute('''SELECT name FROM artist WHERE  
        data_realise NOT  != 2020;''').fetchall()
        pprint(select_2_4)

# 5 названия сборников, в которых присутствует конкретный исполнитель (выберите сами);

select_2_5 = ('''SELECT name FROM collection
JOIN artist ON collection.name = artist.name_artist;''').fetchall()
    select_2_5 = connection.execute('''SELECT name FROM collection 
    WHERE name_artist('artist_5');''').fetchone()
    pprint(select_2_5)

# 6 название альбомов, в которых присутствуют исполнители более 1 жанра;

select_2_6 = ('''SELECT name FROM album
JOIN artist ON album.name_album = artist.name_artist;''').fetchall()
    select_2_6 = ('''SELECT name FROM album WHERE name_artist <= 1;''').fetchall()
    pprint(select_2_6)

 # 7 наименование треков, которые не входят в сборники;

select_2_7 = ('''SELECT name_track FROM track
JOIN collection ON track.name_track = collection.name;''').fetchall()
    select_2_7 = ('''SELECT name_track FROM collection WHERE name_artist NOT IN ('collection')
''').fetchall()
    pprint(select_2_7)

# 8 исполнителя(-ей), написавшего самый короткий по продолжительности трек
# (теоретически таких треков может быть несколько);

select_2_8 = ('''SELECT name_artist FROM arist
JOIN track ON track.tracklegth = artist.name_artist;''').fetchall()
    select_2_8 = ('''SELECT name_artist FROM artist WHERE MIN('tracklegth');
''').fetchall()
    pprint(select_2_8)

# 8 название альбомов, содержащих наименьшее количество треков.

select_2_8 = ('''SELECT name_album FROM album 
JOIN track ON track.name_track = album.name_album;''').fetchall()
    select_2_8 = ('''SELECT name_album FROM album WHERE name_MIN('track');
''').fetchall()
    print(select_2_8)








