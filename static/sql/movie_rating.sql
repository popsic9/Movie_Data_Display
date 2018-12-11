SET NAMES utf8mb4 ;

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `rating`;
SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE IF NOT EXISTS `rating` (
  `rating_id` INT NOT NULL AUTO_INCREMENT,
  `rating` FLOAT NULL,
  PRIMARY KEY (`rating_id`))
ENGINE = InnoDB;



LOAD DATA LOCAL INFILE '/Users/Viviana/Desktop/664/project/movie/ml-latest-small/rating_range.csv'
INTO TABLE rating
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@dummy, rating);


SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `movie` ;
SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE IF NOT EXISTS `movie` (
  `movie_id` INT(11) NOT NULL AUTO_INCREMENT,
  `movie_title` VARCHAR(100) NOT NULL,
  `imdbid` INT(11) DEFAULT NULL,
  `tmdbid` INT(11) DEFAULT NULL,
  PRIMARY KEY (`movie_id`))
ENGINE = InnoDB;


LOAD DATA LOCAL INFILE '/Users/Viviana/Desktop/664/project/movie/ml-latest-small/movies.csv'
INTO TABLE movie
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(movie_title, @dummy, imdbId, tmdbId);

-- -----------------------------------------------------
-- Table `movie_rating_display`.`genre`
-- -----------------------------------------------------
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `genre` ;
SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE IF NOT EXISTS `genre` (
  `genre_id` INT NOT NULL AUTO_INCREMENT,
  `genre_name` VARCHAR(100) NULL,
  PRIMARY KEY (`genre_id`))
ENGINE = InnoDB;


LOAD DATA LOCAL INFILE '/Users/Viviana/Desktop/664/project/movie/ml-latest-small/genres.csv'
INTO TABLE genre
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@col1)
SET genre_name=@col1;

-- -----------------------------------------------------
-- Table `movie_rating_display`.`age_range`
-- -----------------------------------------------------
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `age_range` ;
SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE IF NOT EXISTS `age_range` (
  `age_range_id` INT NOT NULL AUTO_INCREMENT,
  `age_range_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`age_range_id`))
ENGINE = InnoDB;


LOAD DATA LOCAL INFILE '/Users/Viviana/Desktop/664/project/movie/ml-latest-small/age_range.csv'
INTO TABLE age_range
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(age_range_name);
-- -----------------------------------------------------
-- Table `movie_rating_display`.`work`
-- -----------------------------------------------------
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `work` ;
SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE IF NOT EXISTS `work` (
  `work_id` INT NOT NULL AUTO_INCREMENT,
  `work_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`work_id`))
ENGINE = InnoDB;

LOAD DATA LOCAL INFILE '/Users/Viviana/Desktop/664/project/movie/ml-latest-small/work.csv'
INTO TABLE work
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(work_name);












-- -----------------------------------------------------
-- Table `movie_rating_display`.`movies_genre`
-- -----------------------------------------------------
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `movie_genre` ;
SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE IF NOT EXISTS `movie_genre` (
  `movie_genre_id` INT NOT NULL AUTO_INCREMENT,
  `movie_id` INT NOT NULL,
  `genre_id` INT NOT NULL,
  PRIMARY KEY (`movie_genre_id`),
  CONSTRAINT `fk_Movies_has_Genres_Movies1`
    FOREIGN KEY (`movie_id`)
    REFERENCES `movie` (`movie_id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_Movies_has_Genres_Genres1`
    FOREIGN KEY (`genre_id`)
    REFERENCES `genre` (`genre_id`)
    ON DELETE CASCADE ON UPDATE CASCADE)
ENGINE = InnoDB;

LOAD DATA LOCAL INFILE '/Users/Viviana/Desktop/664/project/movie/ml-latest-small/movie_genre.csv'
INTO TABLE movie_genre
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(`movie_id`, `genre_id`);






-- --------------------------------------------------------
-- Table `movie_rating_display`.`user`
-- -----------------------------------------------------
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `user` ;
SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` INT NOT NULL,
  `gender` VARCHAR(45) NULL,
  `age` INT NULL,
  `zipcode` VARCHAR(45) NULL,
  `age_range_id` INT NULL,
  `work_id` INT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_Users_AgeRange`
    FOREIGN KEY (`age_range_id`)
    REFERENCES `age_range` (`age_range_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Users_Work1`
    FOREIGN KEY (`work_id`)
    REFERENCES `work` (`work_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

LOAD DATA LOCAL INFILE '/Users/Viviana/Desktop/664/project/movie/ml-latest-small/users.csv'
INTO TABLE user
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(`user_id`, `gender`, `age`, `zipcode`, `age_range_id`, `work_id`);






-- -----------------------------------------------------
-- Table `movie_rating_display`.`movie_rating`
-- -----------------------------------------------------
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `movie_rating` ;
SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE IF NOT EXISTS `movie_rating` (
  `movie_rating_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `movie_id` INT NOT NULL,
  `rating_id` INT NOT NULL,
  `timestamp` INT NULL,
  PRIMARY KEY (`movie_rating_id`),
  CONSTRAINT `fk_Movies_has_Users_Movies1`
    FOREIGN KEY (`movie_id`)
    REFERENCES `movie` (`movie_id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_Movies_has_Users_Users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`user_id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_movie_rating_rating1`
    FOREIGN KEY (`rating_id`)
    REFERENCES `rating` (`rating_id`)
    ON DELETE CASCADE ON UPDATE CASCADE)
ENGINE = InnoDB;


LOAD DATA LOCAL INFILE '/Users/Viviana/Desktop/664/project/movie/ml-latest-small/movie_ratings.csv'
INTO TABLE movie_rating
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(`user_id`, `movie_id`, `rating_id`, `timestamp`);








-- -----------------------------------------------------
-- Table `movie_rating_display`.`tag`
-- -----------------------------------------------------
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `tag`;
SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE IF NOT EXISTS `tag` (
  `tag_id` INT NOT NULL AUTO_INCREMENT,
  `movie_id` INT NOT NULL,
  `tag` VARCHAR(100) NULL,
  PRIMARY KEY (`tag_id`),
  CONSTRAINT `fk_Movies_has_Users_Movies2`
    FOREIGN KEY (`movie_id`)
    REFERENCES `movie` (`movie_id`)
    ON DELETE CASCADE ON UPDATE CASCADE)
ENGINE = InnoDB;


LOAD DATA LOCAL INFILE '/Users/Viviana/Desktop/664/project/movie/ml-latest-small/tags.csv'
INTO TABLE tag
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(`movie_id`, `tag`);