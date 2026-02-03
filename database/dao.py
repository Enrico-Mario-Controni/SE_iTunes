from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_nodes(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select a.id as id, a.title as titolo
                    from album a
                    where a.id in (select t.album_id
                                    from track t 
                                    group by t.album_id 
                                    having sum(t.milliseconds)> %s) """

        cursor.execute(query,(durata,))

        for row in cursor:
            result.append((row["id"], row["titolo"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_edges(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t1.album_id as u , t2.album_id as v
                    from track t1, track t2, playlist_track pt1, playlist_track pt2  
                    where t1.album_id <> t2.album_id 
                    and t1.id = pt1.track_id 
                    and t2.id = pt2.track_id 
                    and pt1.playlist_id = pt2.playlist_id 
                    and t1.album_id in (select t.album_id
                                        from track t 
                                        group by t.album_id 
                                        having sum(t.milliseconds)> %s)
                    and t2.album_id in (select t.album_id
                                        from track t 
                                        group by t.album_id 
                                        having sum(t.milliseconds)>%s )
                    group by t1.album_id, t2.album_id  """

        cursor.execute(query,(durata,durata,))

        for row in cursor:
            result.append((row["u"], row["v"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connected_time(album_connesso):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select sum(t.milliseconds )/60000 as peso
                    from track t 
                    where t.album_id = %s"""

        cursor.execute(query,(album_connesso,))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result

