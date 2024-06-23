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
     
        """)
        conn.commit()

       

def main():
    params = config()
    connection = psycopg2.connect(**params)
    
    if connection:
        CreateTables(connection)
   
   
    
    connection.close()


if __name__ == "__main__":
    main()
