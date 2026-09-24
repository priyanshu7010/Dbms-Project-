-- Converted from SQLite to SQL/MySQL-compatible format
-- Source: 57ec8191-d318-4b30-9764-ade1edde325d.sqlite3

CREATE DATABASE IF NOT EXISTS gaming_database;
USE gaming_database;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `Game`;
DROP TABLE IF EXISTS `User`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `User` (
    `user_id` INT NOT NULL,
    `user_name` VARCHAR(150) NOT NULL,
    `country` VARCHAR(100) NOT NULL,
    `u_age` INT NOT NULL,
    `pincode` VARCHAR(50) NOT NULL,
    `city` VARCHAR(100) NOT NULL,
    `passwords` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Game` (
    `game_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `game_name` VARCHAR(150) NOT NULL,
    `game_type` VARCHAR(100) NOT NULL,
    `age_rest` INT NOT NULL,
    `rate` INT NOT NULL,
    PRIMARY KEY (`game_id`),
    CONSTRAINT `fk_game_user`
        FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `User` (`user_id`, `user_name`, `country`, `u_age`, `pincode`, `city`, `passwords`) VALUES
(1, 'Ronnica', 'El Salvador', 69, '95413', 'Camiri', '9791'),
(2, 'Rik', 'Russia', 20, '90592', 'Cincinnati', '7265'),
(3, 'Mallorie', 'Croatia', 89, '70297', 'Babakansari', '6652'),
(4, 'Kimberlyn', 'Sweden', 81, '36883', 'Kani''aw', '8386'),
(5, 'Ariel', 'Portugal', 29, '68197', 'Vitrolles', '2234'),
(6, 'Gualterio', 'China', 17, '92072', 'Amieira', '8781'),
(7, 'Grantley', 'China', 61, '94123', 'Yajiang', '5112'),
(8, 'Rozamond', 'Kazakhstan', 69, '52219', 'Biljdal', '2566'),
(9, 'Nettle', 'Pakistan', 91, '88189', 'Karis', '3347'),
(10, 'Bradan', 'United States', 87, '68231', 'Zagreb', '1162'),
(11, 'Ezequiel', 'China', 87, '42448', 'Wenceslau Braz', '9223'),
(12, 'Guillaume', 'Azerbaijan', 57, '66247', 'Xlagenszi', '1486'),
(13, 'Nathalie', 'France', 34, '75008', 'Paris', '8831'),
(14, 'Matthias', 'Germany', 41, '10115', 'Berlin', '4412'),
(15, 'Chloe', 'Canada', 26, 'H2Y1C6', 'Montreal', '6723'),
(16, 'Dmitry', 'Russia', 33, '101000', 'Moscow', '5519'),
(17, 'Camila', 'Brazil', 28, '01310', 'Sao Paulo', '3321'),
(18, 'Kenji', 'Japan', 45, '100-0001', 'Tokyo', '9910'),
(19, 'Fatima', 'Morocco', 31, '20000', 'Casablanca', '7712'),
(20, 'Adelle', 'Russia', 63, '24297', 'Alakak', '3740'),
(21, 'Luca', 'Italy', 24, '00184', 'Rome', '8823'),
(22, 'Ananya', 'India', 22, '110001', 'New Delhi', '6514'),
(23, 'Lars', 'Norway', 50, '0150', 'Oslo', '4432'),
(24, 'Priya', 'India', 29, '400001', 'Mumbai', '1290'),
(25, 'Carlos', 'Spain', 38, '28001', 'Madrid', '9812'),
(26, 'Mateo', 'Argentina', 35, 'C1002', 'Buenos Aires', '5541'),
(27, 'Yuki', 'Japan', 27, '600-8001', 'Kyoto', '3129'),
(28, 'Liam', 'Ireland', 42, 'D02', 'Dublin', '8712'),
(29, 'Zoe', 'Greece', 33, '10431', 'Athens', '6643'),
(30, 'Ariel', 'Russia', 84, '81804', 'Bangkalan', '3736'),
(31, 'Chen', 'China', 39, '200000', 'Shanghai', '9921'),
(32, 'Viktor', 'Ukraine', 47, '01001', 'Kyiv', '4418'),
(33, 'Stella', 'China', 69, '92929', 'Az Zulfi', '1315'),
(34, 'Allyson', 'Poland', 45, '43032', 'Bahor', '1353'),
(35, 'Siddharth', 'India', 25, '560001', 'Bangalore', '7821'),
(36, 'Aarav', 'India', 21, '380009', 'Ahmedabad', '2910'),
(37, 'Elena', 'Greece', 29, '54621', 'Thessaloniki', '5123'),
(38, 'Felix', 'Austria', 36, '1010', 'Vienna', '6612'),
(39, 'Larry', 'Czech Republic', 54, '67487', 'Jalatrang', '7189'),
(40, 'Svend', 'China', 52, '80501', 'Karlskrona', '2893'),
(41, 'Calypso', 'Portugal', 92, '70177', 'Slobodka', '3846'),
(42, 'Irvin', 'China', 24, '39888', 'Rengat', '9355'),
(43, 'Amabel', 'Portugal', 17, '57058', 'Kamenka', '6713'),
(44, 'Friedrick', 'Mongolia', 36, '62780', 'Milovice', '4457'),
(45, 'Rozele', 'Cuba', 59, '95129', 'Beichan', '1676'),
(46, 'Myer', 'China', 70, '23649', 'Kun''aw', '1376'),
(47, 'Danna', 'Mexico', 74, '47450', 'Cazuelas', '3944'),
(48, 'Sawyere', 'Indonesia', 78, '40292', 'Ganding', '2356'),
(49, 'Hiram', 'China', 81, '49089', 'Agios Patros', '2679'),
(50, 'sayani', 'pakistan', 18, '384001', 'ahmedabad', '3445'),
(51, 'jillu', 'africa', 19, '453882', 'egypt', '9442'),
(232, 'priyanshu', 'india', 54, '358762', 'ahmedabad', '12345');

INSERT INTO `Game` (`game_id`, `user_id`, `game_name`, `game_type`, `age_rest`, `rate`) VALUES
(1, 1, 'Viva', 'Opela', 13, 8913),
(2, 1, 'Redhold', 'Stringtough', 30, 5186),
(3, 1, 'Quo Lux', 'Stronghold', 14, 7576),
(4, 1, 'Home Ing', 'Stringtough', 50, 1216),
(5, 1, 'Duobam', 'Bitwolf', 27, 9822),
(6, 1, 'Namfix', 'Rank', 34, 4924),
(7, 1, 'Aerified', 'Span', 26, 2531),
(8, 1, 'Regrant', 'Alphazap', 30, 6309),
(9, 1, 'Redhold', 'Zaam-Dox', 36, 3574),
(10, 1, 'Hatity', 'Veribet', 32, 5102),
(11, 1, 'Fintone', 'Fixflex', 35, 1999),
(12, 1, 'Hatity', 'Sonair', 38, 7365),
(13, 1, 'Veribet', 'Fixflex', 28, 1467),
(14, 1, 'Voyatouch', 'Veribet', 40, 3903),
(15, 1, 'Bigtax', 'Konklux', 33, 6303),
(16, 1, 'Namfix', 'Ventosanzap', 50, 8104),
(17, 1, 'Ventosanzap', 'Sonsing', 41, 4406),
(18, 2, 'Cyberwar', 'Action', 18, 9500),
(19, 2, 'Shadowrun', 'RPG', 16, 8800),
(20, 3, 'Battlefront', 'Multiplayer', 12, 7900);

-- End of converted database
