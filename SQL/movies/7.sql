SELECT ratings.rating, movies.title
FROM movies
JOIN ratings on movies.id = ratings.movie_id
WHERE movies.year = 2010
ORDER BY ratings.rating desc,
movies.title asc;