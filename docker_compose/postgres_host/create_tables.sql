CREATE SCHEMA IF NOT EXISTS movie;

DROP TABLE IF EXISTS movie.links, postgres.movie.ratings, postgres.movie.events;

CREATE TABLE movie.links (
    movieId bigint,
    imdbId varchar(400),
    tmdbId varchar(400)
);

CREATE TABLE movie.ratings (
    userId bigint,
    movieId bigint,
    rating float(25),
    timestamp bigint
);

CREATE TABLE movie.events (
  user_id_for_mai bigint,
  session_id varchar(400),
  session_page_index bigint,
  session_main_index bigint,
  rocket_datetime bigint,
  country varchar(400),
  subsite_title varchar(400),
  name varchar(400),
  ui_type varchar(400),
  ui_id varchar(400),
  ui_title varchar(400),
  content_id bigint,
  compilation_id bigint,
  purchase_id bigint,
  trial bigint,
  currency varchar(400),
  object_id bigint,
  object_type varchar(400),
  price float(25),
  ownership varchar(400),
  renewable bigint,
  renewal_price float(25)
);

CREATE TABLE movie.test (
    test_id bigint
);