SELECT AVG(rating) FROM ratings
join movies on movies.id = ratings.movie_id
WHERE movies.year = 2012;