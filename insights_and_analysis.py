from connection import connect_to_postgres

def print_result(result):                         #Prints the result
    for row in result:
        print('  '.join([str(_) for _ in row]))

def get_top_movie_titles(*, criteria):                #Taking top movie titles
    if criteria == 'duration':
        query = "SELECT title, minutes FROM movies ORDER BY minutes DESC LIMIT 5;"
    elif criteria == "year":
        query = "SELECT title, year FROM movies ORDER BY year DESC LIMIT 5;"
    elif criteria == "average_rating":
        query = '''
            SELECT m.title, AVG(r.rating) AS avg_rating
            FROM movies m
            LEFT JOIN ratings r ON m.id = r.movie_id
            GROUP BY m.id, m.title
            HAVING COUNT(r.id) >= 5
            ORDER BY avg_rating DESC
            LIMIT 5;
        '''
    elif criteria == "number_of_ratings":
        query = '''
                SELECT m.title, COUNT(r.id) AS num_ratings
                FROM movies m
                LEFT JOIN ratings r ON m.id = r.movie_id
                GROUP BY m.id, m.title
                HAVING COUNT(r.id) >= 5
                ORDER BY num_ratings DESC
                LIMIT 5;
        '''
    connection = connect_to_postgres()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# -----------------------------------------
print("------------Top 5 Movies------------------")
print("Based on duration: ")
print_result(get_top_movie_titles(criteria="duration"))
print()
print("Based on year: ")
print_result(get_top_movie_titles(criteria="year"))
print()
print("Based on average rating: ")
print_result(get_top_movie_titles(criteria="average_rating"))
print()
print("Based on number of ratings: ")
print_result(get_top_movie_titles(criteria="number_of_ratings"))
print()

def get_unique_raters():
    query = "SELECT distinct rater_id from ratings ORDER BY rater_id;"
    connection = connect_to_postgres()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# --------------------------------------------
print("----------------unique raters--------------")
print_result(get_unique_raters())


def get_top_rater_ids(*, criteria):
    if criteria == 'most_movies_rated':
        query = '''
                SELECT rater_id, COUNT(movie_id) AS num_movies_rated
                FROM ratings
                GROUP BY rater_id
                ORDER BY num_movies_rated DESC
                LIMIT 5;
        '''
    elif criteria == 'highest_average_rating_given':
        query = '''
                SELECT rater_id, AVG(rating) AS avg_rating
                FROM ratings
                GROUP BY rater_id
                HAVING COUNT(id) >= 5
                ORDER BY avg_rating DESC
                LIMIT 5;
        '''
    connection = connect_to_postgres()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# ------------------------------------------
print("--------------top raters id-----------------")
print("based on most_movies_rated")
print_result(get_top_rater_ids(criteria="most_movies_rated"))
print()
print("based on highest_average_rating_given")
print_result(get_top_rater_ids(criteria="highest_average_rating_given"))
print()


def get_top_rated_movies(*, criteria):
    if criteria == 'Michael Bay':                  #Taking one criteria at a time when director= "Michael Bay"
        query = '''
            SELECT m.title, AVG(r.rating) AS avg_rating
            FROM public.movies m
            JOIN public.ratings r ON m.id = r.movie_id
            WHERE m.director = 'Michael Bay'
            GROUP BY m.id, m.title
            HAVING COUNT(r.id) >= 5
            ORDER BY avg_rating DESC
            LIMIT 5;
        '''
    elif criteria == "Comedy":                   #Taking one criteria at a time when genre= "Comedy"
        query = '''
        SELECT m.title, AVG(r.rating) AS avg_rating
        FROM public.movies m
        JOIN public.ratings r ON m.id = r.movie_id
        WHERE m.genre LIKE '%Comedy%'
        GROUP BY m.id, m.title
        HAVING COUNT(r.id) >= 5
        ORDER BY avg_rating DESC
        LIMIT 5;
    '''
    elif criteria=="2013":                         #Taking one criteria at a time when year= "2013"
        query = '''
        SELECT m.title, AVG(r.rating) AS avg_rating
        FROM public.movies m
        JOIN public.ratings r ON m.id = r.movie_id
        WHERE m.year = '2013'
        GROUP BY m.id, m.title
        HAVING COUNT(r.id) >= 5
        ORDER BY avg_rating DESC
        LIMIT 5;
    '''
    elif criteria == "India":                       #Taking one criteria at a time when Country= "India"
        query = '''
            SELECT m.title, AVG(r.rating) AS avg_rating
            FROM public.movies m
            JOIN public.ratings r ON m.id = r.movie_id
            WHERE m.country LIKE '%India%'
            GROUP BY m.id, m.title
            HAVING COUNT(r.id) >= 5
            ORDER BY avg_rating DESC
            LIMIT 5;
        '''
    else:                                           #Taking all criteria 
        query = '''
            SELECT m.title, AVG(r.rating) AS avg_rating
            FROM public.movies m
            JOIN public.ratings r ON m.id = r.movie_id
            WHERE m.director = 'Michael Bay'
                AND m.genre = 'Comedy'
                AND m.year = 2013
                AND m.country = 'India'
            GROUP BY m.id, m.title
            HAVING COUNT(r.id) >= 5
            ORDER BY avg_rating DESC
            LIMIT 5;
        '''
    connection = connect_to_postgres()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

#------------------------------
print('------------top rated movies-----------')
print('-------------Director= "Michael Bay"------------')
print_result(get_top_rated_movies(criteria="Michael Bay"))
print()
print('-------------Genre= "Comedy"------------')
print_result(get_top_rated_movies(criteria="Comedy"))
print()
print('-------------Released Year= "2013"------------')
print_result(get_top_rated_movies(criteria="2013"))
print()
print('-------------Country= "India"------------')
print_result(get_top_rated_movies(criteria="India"))
print()


def get_favorite_movie_genre(*, rater_id):
    query = f'''
        SELECT rater_id, m.genre, COUNT(r.id) AS num_ratings
        FROM public.ratings r
        JOIN public.movies m ON r.movie_id = m.id
        WHERE r.rater_id = {str(rater_id)}
        GROUP BY rater_id, m.genre
        ORDER BY num_ratings DESC
        LIMIT 1;
    '''
    connection = connect_to_postgres()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

#----------------------------
print('--------------favorite movie genre -------------')
print_result(get_favorite_movie_genre(rater_id=1040))
print()

def get_highest_average_rated_movie_genre(*, rater_id):
    query = f'''
        SELECT m.genre, AVG(r.rating) AS avg_rating
        FROM public.ratings r
        JOIN public.movies m ON r.movie_id = m.id
        WHERE r.rater_id = {str(rater_id)}
        GROUP BY m.genre
        HAVING COUNT(r.id) >= 5
        ORDER BY avg_rating DESC
        LIMIT 1;

    '''
    connection = connect_to_postgres()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

#----------------------------
print('-------------- highest_average_rated_movie_genre -------------')
print_result(get_highest_average_rated_movie_genre(rater_id=1040))
print()


def get_year_with_second_highest_number_of_action_movies():
    query = '''
        WITH ActionMovies AS (
        SELECT m.year, COUNT(*) AS num_action_movies
        FROM movies m
        JOIN ratings r ON m.id = r.movie_id
        WHERE m.genre LIKE '%Action%'
        AND m.country = 'USA'
        AND m.minutes < 120
        AND r.rating >= 6.5
        GROUP BY m.year
    )
    SELECT year
    FROM ActionMovies
    ORDER BY num_action_movies DESC
    OFFSET 1 
    LIMIT 1;

    '''
    connection = connect_to_postgres()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


#----------------------------
print('-------------- year_with_second_highest_number_of_action_movies -------------')
print_result(get_year_with_second_highest_number_of_action_movies())
print()



def get_count_of_movies_with_5_reviews_and_7_ratings():
    query = '''
            SELECT SUM(num_high_rated_movies) AS total_high_rated_movies
            FROM (
                SELECT COUNT(DISTINCT movie_id) AS num_high_rated_movies
                FROM ratings
                GROUP BY movie_id
                HAVING COUNT(DISTINCT rater_id) >= 5 AND AVG(rating) >= 7
            ) subquery;

    '''
    connection = connect_to_postgres()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


#----------------------------
print('-------------- count_of_movies_with_5_reviews_and_7_ratings -------------')
print_result(get_count_of_movies_with_5_reviews_and_7_ratings())
print()