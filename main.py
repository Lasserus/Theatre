import psycopg2
from config import config

def CreateTables(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    
        CREATE TABLE IF NOT EXISTS director(
        director_id INT,
        name VARCHAR(200),
        lastname VARCHAR(200),
        age INT,
        CONSTRAINT pk_director PRIMARY KEY(director_id)
        );
                    
        CREATE TABLE IF NOT EXISTS movie(
            movie_id INT,
            director_id INT,
            title VARCHAR(200),
            runtime_min INT,
            release_date DATE,
            description VARCHAR(2000),
            CONSTRAINT pk_movie PRIMARY KEY (movie_id),
            CONSTRAINT fk_director FOREIGN KEY(director_id) REFERENCES director(director_id)
        );

        CREATE TABLE IF NOT EXISTS cast_member(
            cast_id INT,
            name VARCHAR(200),
            lastname VARCHAR(200),
            CONSTRAINT pk_cast PRIMARY KEY (cast_id)
        ); 

        CREATE TABLE IF NOT EXISTS movie_cast(
            movie_id INT,
            cast_id INT,
            CONSTRAINT fk_mc_movie FOREIGN KEY(movie_id) REFERENCES movie(movie_id),
            CONSTRAINT fk_mc_cast FOREIGN KEY(cast_id) REFERENCES cast_member(cast_id)
        );         
        
        CREATE TABLE IF NOT EXISTS genre(
            genre_id INT,
            name VARCHAR(200),
            CONSTRAINT pk_genre PRIMARY KEY (genre_id)      
        );
        
        CREATE TABLE IF NOT EXISTS movie_genre(
            movie_id INT,
            genre_id INT,
            CONSTRAINT fk_mg_movie FOREIGN KEY(movie_id) REFERENCES movie(movie_id),
            CONSTRAINT fk_mg_genre FOREIGN KEY(genre_id) REFERENCES genre(genre_id)           
        );

        CREATE TABLE IF NOT EXISTS city(
            city_id INT,
            name VARCHAR(200),
            CONSTRAINT pk_city PRIMARY KEY (city_ID)       
            );
        
        CREATE TABLE IF NOT EXISTS cinema(
            cinema_id INT,
            name VARCHAR(200),
            city_id INT,
            CONSTRAINT pk_cimena PRIMARY KEY (cinema_id),
            CONSTRAINT fk_cinema_city FOREIGN KEY (city_id) REFERENCES city(city_id)         
                    );
        """)
        conn.commit()

def ShowMovies(conn):
    with conn.cursor() as curr:
        curr.execute("""
        SELECT m.movie_id, d.name, d.lastname, m.title, m.runtime_min, m.release_date, m.description
        FROM movie m
        INNER JOIN director d ON m.director_id = d.director_id
        """)
        rows = curr.fetchall()
        for row in rows:
            print(row)

def ShowCastandGenre(conn):
     with conn.cursor() as curr:
        curr.execute("""
        SELECT m.movie_id, m.title, c.name, c.lastname, g.name
        FROM movie m
        INNER JOIN movie_cast mc ON mc.movie_Id = m.movie_id
        INNER JOIN cast_member c ON mc.cast_id = c.cast_id
        INNER JOIN movie_genre mg ON m.movie_id = mg.movie_id
        INNER JOIN genre g ON mg.genre_id = g.genre_id
        """)
        rows = curr.fetchall()
        for row in rows:
            print(row)

def main():
    params = config()
    connection = psycopg2.connect(**params)
    
    if connection:
        CreateTables(connection)
        print("\n Movies:")
        ShowMovies(connection)
        print("\n Movie cast members and genre")
        ShowCastandGenre(connection)
       
   
    
    connection.close()


if __name__ == "__main__":
    main()
