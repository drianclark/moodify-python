CREATE TABLE db.tracks (
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	spotifyid varchar(100) NOT NULL,
	title varchar(100) NOT NULL,
	valence FLOAT NOT NULL,
	play_date DATETIME NOT NULL,
	acousticness FLOAT NOT NULL,
	danceability FLOAT NOT NULL,
	energy FLOAT NOT NULL,
	speechiness FLOAT NOT NULL,
	tempo FLOAT NOT NULL,
	CONSTRAINT tracks_PK PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

