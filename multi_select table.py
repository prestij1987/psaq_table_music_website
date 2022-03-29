




import sqlalchemy

from sqlalchemy import create_engine

import psycopg2



db = 'postgresql+psycopg2://postgres:123@Localhost:5432/artist_base'
engine = sqlalchemy.create_engine(db)
print(engine)
connection = engine.connect()
print(connection)



def get_genres_data():
    # количество исполнителей в каждом жанре;
    request_data = connection.execute('''SELECT genrename, COUNT(artistname) FROM artist
                                    LEFT JOIN artist_genre ON artist_genre.artist_id = artist.id
                                    LEFT JOIN genre ON genre.id = artist_genre.genre.id
                                    GROUP BY genrename
                                    ORDER BY COUNT(artistname) DESC                                    
        ''').fetchall()
    result_line = 'Список жанров по количеству исполнителей:\n'
    for request in request_data:
        result_line += f'{request[0].capitalize()}: {request[1]}\n'

    return result_line


def get_tracks_between(year):
    # количество треков, вошедших в альбомы 2019-2020 годов;
    request_data = connection.execute(f'''SELECT COUNT(trackname) FROM track
                                         LEFT JOIN album ON album.id = track.album_id
                                         WHERE album.reliasedate BETWEEN {year[0]} AND {year[1]}
    ''').fetchall()[0][0]
    result_line = f'Количество треков выпущенных с {year[0]} по {year[1]}: {request_data}\n'

    return result_line


def get_mid_treck_length():
    # средняя продолжительность треков по каждому альбому;
    request_data = connection.execute(f'''SELECT albumname,AVG(track.tracklegth) FROM  track
                                         LEFT JOIN album ON album.id = track.album_id
                                         GROUP BY al.name
    ''').fetchall()
    result_line = 'Средняя продолжительность треков по каждому альбому\n'
    for data in request_data:
        result_line += f'{data[0].capitalize()}: {round(data[1])} секунд \n'

    return result_line


def get_artists_not_in(year):
    # все исполнители, которые не выпустили альбомы в 2020 году;
    request_data = connection.execute(f'''SELECT artistname FROM artist
                                             LEFT JOIN album_artist  ON album_artist.artist_id = artist.id    
                                             LEFT JOIN album ON album.id = album_artist.album_id
                                             WHERE album.reliasedate <> {year}
                                             GROUP BY artistname                                             
                                             ''').fetchall()
    result_line = f'Dсе исполнители, которые не выпустили альбомы в {year} году\n'
    for data in request_data:
        result_line += f'{data[0].capitalize()}\n'

    return result_line


def get_album_by_artist(name):
    # названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
    request_data = connection.execute(f'''SELECT albumname FROM album
                                             LEFT JOIN album_artist ON album.id = album_artist.album_id    
                                             LEFT JOIN artist ON album_artist.artist_id = artist.id 
                                             WHERE artistname = '{name.lower()}'                         
                                             ''').fetchall()
    result_line = f'Названия сборников, в которых присутствует исполнитель {name}\n'
    for data in request_data:
        result_line += f'{data[0].capitalize()}\n'

    return result_line


def get_album_of_multigenres():
    # название альбомов, в которых присутствуют исполнители более 1 жанра;
    request_data = connection.execute(f'''SELECT albumname, artistname FROM album 
                                             LEFT JOIN album_artist ON album.id = album_artist.album_id    
                                             LEFT JOIN artist ON album_artist.artist_id = artist.id 
                                             LEFT JOIN artist_genre  ON artist_genre.artist_id = artist.id
                                             LEFT JOIN genre ON genre.id = artist_genre.genre_id
                                             GROUP BY albumname,artistname
                                             HAVING COUNT(genrename) > 1                                       
                                             ''').fetchall()
    result_line = f'название альбомов, в которых присутствуют исполнители более 1 жанра:\n'

    for data in request_data:
        result_line += f'альбом {data[0].capitalize()} от исполнителя {data[1].capitalize()}\n'

    return result_line


def get_song_not_into_collection():
    # наименование треков, которые не входят в сборники
    request_data = connection.execute(f'''SELECT trackname FROM track
                                                 LEFT JOIN collection_album_track  ON collection_album_track.track_id= track.id   
                                                 LEFT JOIN collection  ON collection.id = collection_album_track.collection_id 
                                                 GROUP BY trackname
                                                 HAVING COUNT(colname) = 0                                       
                                                 ''').fetchall()
    result_line = f'ннаименование треков, которые не входят в сборники:\n'
    for data in request_data:
        result_line += f'трек: {data[0].capitalize()}\n'

    return result_line


def get_shortest_song():
    # исполнителя(-ей), написавшего самый короткий по продолжительности трек
    # (теоретически таких треков может быть несколько);
    request_data = connection.execute('''SELECT DISTINCT artistname FROM artist
                                        LEFT JOIN album_artist ON artist.id = album_artist.artist_id
                                        LEFT JOIN album ON album_artist.album_id = album.id
                                        GROUP BY artistname,album.id
                                        HAVING album.id IN (
                                            SELECT album.id FROM track 
                                            WHERE tracklength = (
                                                SELECT MIN(track.tracklength) FROM track))
                                            ''').fetchall()

    result_line = f'исполнитель(И), написавший(ие) самый короткий ' \
                  f'по продолжительности трек:\n'
    for data in request_data:
        result_line += f'исполнитель: {data[0].capitalize()}\n'

    return result_line

def get_album_with_mincount():
    # название альбомов, содержащих наименьшее количество треков.
    request_data = connection.execute('''SELECT albumname, COUNT(trackname) FROM album
                                            LEFT JOIN track ON track.album_id = album.id
                                            GROUP BY albumname
                                            HAVING COUNT(trackname) = (                                      
                                                SELECT MIN(qty) FROM (
                                                SELECT COUNT(trackname) qty FROM album
                                                LEFT JOIN track ON track.album_id = album.id
                                                GROUP BY albumname
                                                ) MinValue
                                                )                                                                                                         
                                        ''').fetchall()

    result_line = f'название альбомов, содержащих наименьшее количество треков\n'
    for data in request_data:
        result_line += f'Альбом: {data[0].capitalize()}\n'

    return result_line




if __name__ == '__main__':
   
    print(get_genres_data())
    print(get_tracks_between([2019, 2020]))
    print(get_mid_treck_length())
    print(get_artists_not_in(2020))
    print(get_album_by_artist('Artist_6'))
    print(get_album_of_multigenres())
    print(get_song_not_into_collection())
    print(get_shortest_song())
    print(get_album_with_mincount())