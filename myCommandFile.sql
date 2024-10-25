DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS developers;

CREATE TABLE games (
        title text,
        rating text,
        avgLength int,
        developer text,
        releaseDate text,
        PRIMARY KEY (title, releaseDate)
        FOREIGN KEY (developer) REFERENCES developers(name)
);

CREATE TABLE developers (
        name text,
        foundingYear text,
        headquartersCity text,
        PRIMARY KEY(name)
);

INSERT INTO developers (name, foundingYear, headquartersCity) VALUES
        ('Atlus', '1986', 'Tokyo'),
        ('Naughty Dog', '1984', 'Santa Monica'),
        ('Square Enix', '2003', 'Tokyo'),
        ('Fromsoft', '1986', 'Tokyo'),
        ('BlueTwelve', '2016', 'Montpellier'),
        ('Capcom', '1979', 'Osaka'),
        ('Rockstar Games', '1998', 'New York'),
        ('Sucker Punch', '1997', 'Bellevue'),
        ('3D Realms', '1987', 'Garland'),
        ('The Creative Assembly', '1987', 'Horsham'),
        ('Id Software', '1991', 'Richardson'),
        ('HAL Laboratory', '1980', 'Tokyo'),
        ('Game Freak', '1989', 'Tokyo'),
        ('Santa Monica Studio', '1999', 'Santa Monica');

INSERT INTO games (title, rating, avgLength, developer, releaseDate) VALUES
        ('Persona 5', 'M', 100, 'Atlus', '2016-09-16'),
        ('Persona 3', 'M', '100', 'Atlus', '2006-07-13'),
        ('The Last of Us', 'M', '17', 'Naughty Dog', '2013-05-07'),
        ('Final Fantasy VII', 'T', '50', 'Square Enix', '1997-09-07'),
        ('Final Fantasy XVI', 'M', '58', 'Square Enix', '2023-06-22'),
        ('Nier Automata', 'M', '38', 'Square Enix', '2017-03-07'),
        ('Nier Replicant', 'M', 40, 'Square Enix', '2021-04-23'),
        ('Elden Ring', 'M', 120, 'Fromsoft', '2022-02-25'),
        ('Bloodborne', 'M', 44, 'Fromsoft', '2015-03-24'),
        ('Stray', 'E', 7, 'BlueTwelve', '2022-07-19'),
        ('Resident Evil 2', 'M', 15, 'Capcom', '2019-01-25'),
        ('Red Dead Redemption 2', 'M', 50, 'Rockstar Games', '2018-10-26'),
        ('Ghost of Tsushima', 'M', 50, 'Sucker Punch', '2020-07-17'),
        ('Ghostrunner', 'M', 10, '3D Realms', '2020-10-27'),
        ('Alien Isolation', 'M', 22, 'The Creative Assembly', '2014-10-07'),
        ('Doom', 'M', 16, 'Id Software', '2016-05-13'),
        ('Doom Eternal', 'M', 20, 'Id Software', '2020-03-20'),
        ('Sekiro', 'M', 42, 'Fromsoft', '2019-03-22'),
        ('Grand Theft Auto V', 'M', 50, 'Rockstar Games', '2013-09-17'),
        ('Super Smash Bros Melee', 'E', 10, 'HAL Laboratory', '2001-12-03'),
        ('Pokemon Platinum', 'E', 70, 'Game Freak', '2009-03-22'),
        ('God of War', 'M', 33, 'Santa Monica Studio', '2018-04-20');


