CREATE TABLE `tracks` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `spotifyid` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `valence` float NOT NULL,
  `play_date` datetime NOT NULL,
  `acousticness` float NOT NULL,
  `danceability` float NOT NULL,
  `energy` float NOT NULL,
  `speechiness` float NOT NULL,
  `tempo` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=158 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(1,'3YnwIp2b99p3e5dsFTXIIx','Dunno',0.0998,'2019-09-21 01:09:13.000',0.768,0.622,0.229,0.0445,81.87)
,(2,'66wkCYWlXzSTQAfnsPBptt','My Favorite Part',0.718,'2019-09-21 01:08:51.000',0.627,0.861,0.33,0.0526,95.016)
,(3,'5bknBRjKJZ643DAN2w8Yoy','FACE',0.678,'2019-09-20 18:30:28.000',0.591,0.945,0.702,0.12,119.887)
,(4,'5bknBRjKJZ643DAN2w8Yoy','FACE',0.678,'2019-09-20 18:05:53.000',0.591,0.945,0.702,0.12,119.887)
,(5,'7Cu2COdH93MnuireuKNiS3','Streetcar',0.142,'2019-09-20 17:51:36.000',0.721,0.41,0.298,0.0473,109.651)
,(6,'3YnwIp2b99p3e5dsFTXIIx','Dunno',0.0998,'2019-09-20 17:47:41.000',0.768,0.622,0.229,0.0445,81.87)
,(7,'66wkCYWlXzSTQAfnsPBptt','My Favorite Part',0.718,'2019-09-20 17:43:43.000',0.627,0.861,0.33,0.0526,95.016)
,(8,'0yJi7eb2SosK5CsSnnqc5o','Foreigner''s God',0.355,'2019-09-20 12:57:14.000',0.166,0.514,0.46,0.0293,89.044)
,(9,'1bk9P03MkZzlvTH4zPaOpX','It Will Come Back',0.171,'2019-09-20 12:56:44.000',0.394,0.36,0.466,0.0455,173.958)
,(10,'35PKfoynRpVFoAUE3D5Kc6','Work Song',0.223,'2019-09-20 12:50:44.000',0.762,0.421,0.39,0.125,72.204)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(11,'4C4Pduzp8LfAtQXHAGQWM5','Sedated',0.259,'2019-09-20 12:46:54.000',0.207,0.535,0.62,0.0411,171.901)
,(12,'10Wtj4WHh9APnWq5q21NDT','In A Week',0.174,'2019-09-20 12:43:26.000',0.807,0.541,0.261,0.0293,131.506)
,(13,'0bkW98npv8EsWQ2fXFzK56','From Eden',0.296,'2019-09-20 12:38:08.000',0.611,0.404,0.69,0.0505,143.211)
,(14,'0fEKxq1mghyT0b867l4Jaf','To Be Alone',0.235,'2019-09-20 12:33:25.000',0.372,0.564,0.444,0.0255,67.034)
,(15,'06gYKhvKl40JOATDLaifl3','SPSP',0.88,'2019-09-19 22:35:22.000',0.564,0.837,0.422,0.0412,90.03)
,(16,'3vywz8tUa1fphXyFRx9lG2','slow it down',0.619,'2019-09-19 22:33:34.000',0.827,0.58,0.209,0.0667,174.191)
,(17,'6Y1skSfIA0sNjfabUNtYOT','tonight',0.48,'2019-09-19 22:31:24.000',0.967,0.875,0.244,0.166,82.01)
,(18,'0Q8cTdHZE1K3x86zDZTtQ3','Exquisite Livin''',0.745,'2019-09-19 22:29:55.000',0.903,0.636,0.565,0.497,147.808)
,(19,'1cP4whyH8nbXq66JzCkzeI','Cinnamon',0.607,'2019-09-19 22:28:34.000',0.691,0.679,0.248,0.0384,87.054)
,(20,'3RUh9DrYDkDCUd1XELtuF0','This Means Goodbye',0.521,'2019-09-19 22:25:13.000',0.106,0.568,0.483,0.0755,83.06)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(21,'0Rs0yeWSSQb6cSbfmvUWrA','House Red',0.647,'2019-09-19 22:23:54.000',0.592,0.66,0.693,0.0533,140.057)
,(22,'3n2ujlr3mCscnFFpepXAIy','She''s Electric',0.457,'2019-09-19 22:20:39.000',0.173,0.532,0.913,0.0443,125.537)
,(23,'0NpvdCO506uO58D4AbKzki','Sherry',0.734,'2019-09-19 22:14:58.000',0.626,0.703,0.478,0.0441,117.562)
,(24,'2qEqMx1n0dnCBzWT9l3nGL','Real Love Baby',0.606,'2019-09-19 22:12:25.000',0.0956,0.427,0.684,0.0353,204.429)
,(25,'2qEqMx1n0dnCBzWT9l3nGL','Real Love Baby',0.606,'2019-09-19 22:12:25.000',0.0956,0.427,0.684,0.0353,204.429)
,(26,'4TBBPZks71c60whhq0PgdP','(Your Love Keeps Lifting Me) Higher & Higher',0.938,'2019-09-19 22:09:16.000',0.176,0.631,0.69,0.0531,94.574)
,(27,'5uES1C2NgkdrNHiCwf9jRr','Baby Love',0.715,'2019-09-19 22:06:15.000',0.782,0.582,0.636,0.0381,135.769)
,(28,'5uES1C2NgkdrNHiCwf9jRr','Baby Love',0.715,'2019-09-19 22:06:15.000',0.782,0.582,0.636,0.0381,135.769)
,(29,'3iSws76HjaU7k49EqJVTfF','Sugar, Sugar',0.967,'2019-09-19 22:03:36.000',0.466,0.736,0.871,0.0278,122.395)
,(30,'3iSws76HjaU7k49EqJVTfF','Sugar, Sugar',0.967,'2019-09-19 22:03:36.000',0.466,0.736,0.871,0.0278,122.395)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(31,'41ujo9qv7GdZvFNYixOxW7','Build Me Up Buttercup',0.905,'2019-09-19 22:00:49.000',0.648,0.614,0.515,0.0321,67.076)
,(32,'0yJi7eb2SosK5CsSnnqc5o','Foreigner''s God',0.355,'2019-09-19 20:26:57.000',0.166,0.514,0.46,0.0293,89.044)
,(33,'1bk9P03MkZzlvTH4zPaOpX','It Will Come Back',0.171,'2019-09-19 20:01:35.000',0.394,0.36,0.466,0.0455,173.958)
,(34,'4LGJ2pLDvTRnul3EcZoYkX','Like Real People Do',0.15,'2019-09-19 20:01:14.000',0.907,0.546,0.164,0.0319,139.327)
,(35,'35PKfoynRpVFoAUE3D5Kc6','Work Song',0.223,'2019-09-19 20:00:37.000',0.762,0.421,0.39,0.125,72.204)
,(36,'35PKfoynRpVFoAUE3D5Kc6','Work Song',0.223,'2019-09-19 13:37:35.000',0.762,0.421,0.39,0.125,72.204)
,(37,'4C4Pduzp8LfAtQXHAGQWM5','Sedated',0.259,'2019-09-19 13:26:59.000',0.207,0.535,0.62,0.0411,171.901)
,(38,'10Wtj4WHh9APnWq5q21NDT','In A Week',0.174,'2019-09-19 13:23:32.000',0.807,0.541,0.261,0.0293,131.506)
,(39,'0bkW98npv8EsWQ2fXFzK56','From Eden',0.296,'2019-09-19 13:18:13.000',0.611,0.404,0.69,0.0505,143.211)
,(40,'0fEKxq1mghyT0b867l4Jaf','To Be Alone',0.235,'2019-09-19 13:13:30.000',0.372,0.564,0.444,0.0255,67.034)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(41,'22sS7JkzeVeq4vOPCB6Fbj','Someone New',0.569,'2019-09-19 13:08:06.000',0.406,0.596,0.528,0.0351,91.924)
,(42,'5xo1Gj4WTssjQgQ0w03cf2','Jackie And Wilson',0.755,'2019-09-19 13:04:22.000',0.0638,0.564,0.725,0.0359,82.153)
,(43,'1SCXzqKZdif5b33POmzwI4','Angel Of Small Death & The Codeine Scene',0.335,'2019-09-19 13:00:40.000',0.195,0.527,0.656,0.0469,94.084)
,(44,'3dYD57lRAUcMHufyqn9GcI','Take Me To Church',0.385,'2019-09-19 12:56:50.000',0.586,0.561,0.667,0.0508,128.962)
,(45,'4Q66chx9WzqWcLItXoZ5r4','Cherry Wine - Live',0.213,'2019-09-19 12:52:48.000',0.954,0.558,0.108,0.0383,127.97)
,(46,'3lyU7Tn7aTqGRhSwAoJ0hb','Going Gets Tough',0.732,'2019-09-19 01:12:19.000',0.218,0.503,0.768,0.0324,162.051)
,(47,'3lyU7Tn7aTqGRhSwAoJ0hb','Going Gets Tough',0.732,'2019-09-19 01:12:16.000',0.218,0.503,0.768,0.0324,162.051)
,(48,'4ktAIutrCjL3oD9rR1aEWU','On My Mind (Acoustic)',0.548,'2019-09-18 21:57:55.000',0.847,0.559,0.352,0.0362,134.253)
,(49,'2BiPDpIgxZVLuP5K19vOci','Soul Jam',0.276,'2019-09-18 21:18:47.000',0.498,0.625,0.601,0.0587,75.071)
,(50,'2FhF52axPlqglBx79Ere5x','Mockingbird',0.324,'2019-09-18 21:14:20.000',0.959,0.694,0.289,0.0359,132.879)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(51,'2Rvhjn78vg0rnuBHCdtz9P','Why Georgia - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.418,'2019-09-25 19:26:37.000',0.0217,0.421,0.759,0.034,99.431)
,(52,'4OT8GH9u9Gx7ydJ49ULunN','Slow Dancing in a Burning Room - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.451,'2019-09-25 19:13:44.000',0.2,0.514,0.536,0.0288,133.848)
,(53,'6V3Sd5FVnf83LLA6VMP15F','Good Love Is On the Way - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.383,'2019-09-25 18:59:13.000',0.011,0.228,0.882,0.0749,186.658)
,(54,'1G7Gg1cH4VKBu3XaoCppzC','Come When I Call - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.658,'2019-09-25 18:54:54.000',0.38,0.788,0.49,0.0576,112.986)
,(55,'2vFYhHS8ycUITvZYownH5K','Belief - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.385,'2019-09-25 18:51:12.000',0.273,0.592,0.894,0.0626,101.245)
,(56,'79H87DHga7uOxkvFRGa4a8','I Don''t Trust Myself (With Loving You) - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.462,'2019-09-25 18:45:09.000',0.441,0.62,0.487,0.0346,83.943)
,(57,'21oJ1K99GBJrE2GVQGVjA0','Frozen',0.227,'2019-09-25 14:04:16.000',0.741,0.486,0.419,0.0563,119.065)
,(58,'66H06L8hktjhduwRDWntDT','Stand Still',0.161,'2019-09-25 13:50:36.000',0.732,0.476,0.44,0.0371,149.389)
,(59,'4qkVALwOxCIEZ7I5gkZ3m4','Butterfly',0.12,'2019-09-25 13:45:52.000',0.255,0.785,0.27,0.0892,131.894)
,(60,'6XXaouvibNRCjFSY5j5nze','Invincible',0.471,'2019-09-25 13:22:44.000',0.149,0.725,0.607,0.29,86.986)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(61,'5zsHmE2gO3RefVsPyw2e3T','What''s Up Danger (with Black Caviar)',0.116,'2019-09-25 13:12:41.000',0.00363,0.701,0.755,0.0417,95.036)
,(62,'7dbka99KTWke5o9hRp0JoB','Sunflower - Spider-Man: Into the Spider-Verse',0.912,'2019-09-25 13:08:57.000',0.552,0.761,0.479,0.0466,89.913)
,(63,'2Wzj9xKdzuaTI6jOj5VPG1','Elevate (feat. Denzel Curry, YBN Cordae, SwaVay, Trevor Rich)',0.652,'2019-09-25 13:06:20.000',0.173,0.577,0.935,0.301,129.019)
,(64,'1TNYksIQsadsgxmpeNwfGk','Home',0.31,'2019-09-25 13:02:40.000',0.00601,0.387,0.733,0.0824,118.043)
,(65,'4F07ku5lMBIoybFPStM2j4','Suede',0.723,'2019-09-25 12:59:07.000',0.459,0.669,0.735,0.329,117.284)
,(66,'1gnwGVoG7V08vMX3hyr90x','Tints (feat. Kendrick Lamar)',0.703,'2019-09-25 12:56:12.000',0.0859,0.805,0.833,0.12,109.076)
,(67,'0N3W5peJUQtI4eyR6GJT5O','King Kunta',0.489,'2019-09-25 12:51:44.000',0.00589,0.884,0.657,0.0977,107.059)
,(68,'5ri4b7YQp2PWn8tl3MRYgE','King James',0.882,'2019-09-25 12:47:48.000',0.0779,0.771,0.889,0.0777,108.015)
,(69,'6XXaouvibNRCjFSY5j5nze','Invincible',0.471,'2019-09-25 12:44:30.000',0.149,0.725,0.607,0.29,86.986)
,(70,'5zsHmE2gO3RefVsPyw2e3T','What''s Up Danger (with Black Caviar)',0.116,'2019-09-25 12:41:13.000',0.00363,0.701,0.755,0.0417,95.036)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(71,'7dbka99KTWke5o9hRp0JoB','Sunflower - Spider-Man: Into the Spider-Verse',0.912,'2019-09-25 12:37:31.000',0.552,0.761,0.479,0.0466,89.913)
,(72,'2Wzj9xKdzuaTI6jOj5VPG1','Elevate (feat. Denzel Curry, YBN Cordae, SwaVay, Trevor Rich)',0.652,'2019-09-25 12:34:52.000',0.173,0.577,0.935,0.301,129.019)
,(73,'1TNYksIQsadsgxmpeNwfGk','Home',0.31,'2019-09-25 12:31:13.000',0.00601,0.387,0.733,0.0824,118.043)
,(74,'4F07ku5lMBIoybFPStM2j4','Suede',0.723,'2019-09-25 12:27:40.000',0.459,0.669,0.735,0.329,117.284)
,(75,'1gnwGVoG7V08vMX3hyr90x','Tints (feat. Kendrick Lamar)',0.703,'2019-09-25 12:24:45.000',0.0859,0.805,0.833,0.12,109.076)
,(76,'0N3W5peJUQtI4eyR6GJT5O','King Kunta',0.489,'2019-09-25 12:20:16.000',0.00589,0.884,0.657,0.0977,107.059)
,(77,'5ri4b7YQp2PWn8tl3MRYgE','King James',0.882,'2019-09-25 12:16:21.000',0.0779,0.771,0.889,0.0777,108.015)
,(78,'1bZmbsNqOkfvGGAikytuW2','Ashamed',0.587,'2019-09-25 12:12:35.000',0.483,0.655,0.451,0.229,91.036)
,(79,'5MZQIjtghyFc4sMVUzD7MD','Kickback',0.744,'2019-09-25 12:08:21.000',0.491,0.912,0.448,0.0446,108.964)
,(80,'43IjtK3IEEyTM5Ek32a2Pr','Brakelights',0.257,'2019-09-25 12:05:30.000',0.597,0.695,0.42,0.0385,124.019)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(81,'68KdvPllp9Pug8ZG6AByFY','Gravity - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.293,'2019-09-25 11:38:45.000',0.614,0.478,0.323,0.0341,115.804)
,(82,'79H87DHga7uOxkvFRGa4a8','I Don''t Trust Myself (With Loving You) - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.462,'2019-09-25 11:25:47.000',0.441,0.62,0.487,0.0346,83.943)
,(83,'0EUSbTvyZfo9QOcxunL9Ro','In Your Atmosphere - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.285,'2019-09-25 11:17:02.000',0.713,0.368,0.44,0.0294,91.799)
,(84,'0EUSbTvyZfo9QOcxunL9Ro','In Your Atmosphere - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.285,'2019-09-24 19:35:16.000',0.713,0.368,0.44,0.0294,91.799)
,(85,'0HHdujGjOZChTrl8lJWEIq','Stop This Train - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.367,'2019-09-24 19:24:22.000',0.598,0.434,0.438,0.0326,92.001)
,(86,'7AtsEX4pJqmAaIajlMwaPU','Neon - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.498,'2019-09-24 19:19:21.000',0.48,0.435,0.548,0.0788,83.64)
,(87,'79H87DHga7uOxkvFRGa4a8','I Don''t Trust Myself (With Loving You) - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.462,'2019-09-24 19:13:24.000',0.441,0.62,0.487,0.0346,83.943)
,(88,'68KdvPllp9Pug8ZG6AByFY','Gravity - Live at the Nokia Theatre, Los Angeles, CA - December 2007',0.293,'2019-09-24 19:04:39.000',0.614,0.478,0.323,0.0341,115.804)
,(89,'1TPLsNVlofwX1txcE9gZZF','We Find Love',0.426,'2019-09-24 15:52:14.000',0.853,0.51,0.363,0.0304,78)
,(90,'6JvfBzqZmSiEG5MjM7OcSY','Diddy Bop (feat. Cam O''bi & Raury)',0.661,'2019-09-24 15:37:59.000',0.713,0.637,0.503,0.336,81.061)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(91,'6CNT5aThbP183ncXeGwTdC','Habit',0.466,'2019-09-24 15:34:30.000',0.27,0.766,0.402,0.107,125.107)
,(92,'5GUYJTQap5F3RDQiCOJhrS','Self Control',0.446,'2019-09-24 15:31:56.000',0.765,0.572,0.209,0.0313,80.069)
,(93,'3YnwIp2b99p3e5dsFTXIIx','Dunno',0.0998,'2019-09-24 15:27:45.000',0.768,0.622,0.229,0.0445,81.87)
,(94,'66wkCYWlXzSTQAfnsPBptt','My Favorite Part',0.718,'2019-09-24 15:23:48.000',0.627,0.861,0.33,0.0526,95.016)
,(95,'4ITftSVpf4XkYoDqqpWjBX','Zulu Screams (feat. Maleek Berry & Bibi Bourelly)',0.721,'2019-09-24 15:16:56.000',0.136,0.753,0.926,0.169,125.956)
,(96,'4u2GWPNC7mu01Qg5i8FwSU','Ring Ring (feat. Big Body Bes)',0.809,'2019-09-24 15:13:57.000',0.367,0.789,0.912,0.357,139.676)
,(97,'0N3W5peJUQtI4eyR6GJT5O','King Kunta',0.489,'2019-09-24 15:11:36.000',0.00589,0.884,0.657,0.0977,107.059)
,(98,'1TNYksIQsadsgxmpeNwfGk','Home',0.31,'2019-09-24 15:01:30.000',0.00601,0.387,0.733,0.0824,118.043)
,(99,'3WVmFGias0p1QPY30DER2Z','Free Room (feat. Appleby) - Capadose Remix',0.462,'2019-09-24 14:57:58.000',0.0248,0.831,0.507,0.0661,119.983)
,(100,'43IjtK3IEEyTM5Ek32a2Pr','Brakelights',0.257,'2019-09-24 14:54:18.000',0.597,0.695,0.42,0.0385,124.019)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(101,'1AWRfCMsAPQ3KqVQpsVz5M','Dun Dun Ba Ba - Interlude',0.502,'2019-09-27 16:57:21.000',0.542,0.733,0.519,0.391,85.501)
,(102,'0fu5r69xQg8OQCGsK2S5Il','Here Comes The Sun (feat. dodie)',0.461,'2019-09-27 16:55:26.000',0.838,0.641,0.398,0.054,145.043)
,(103,'63bRlSS5g67PIHsogL2xOA','It Don’t Matter (feat. JoJo)',0.608,'2019-09-27 16:51:28.000',0.538,0.712,0.373,0.175,89.891)
,(104,'6AEYJSl89zOrlcta65d5y5','I Heard You Singing (feat. Becca Stevens & Chris Thile)',0.329,'2019-09-27 16:47:06.000',0.941,0.398,0.211,0.0317,96.959)
,(105,'5YK0WaXMtRHeWEn8EIbmPw','Lua (feat. MARO)',0.327,'2019-09-27 16:42:15.000',0.86,0.445,0.179,0.0358,148.094)
,(106,'3nTzwiI3MxJ55m3n5caeco','À Noite - Interlude',0.0358,'2019-09-27 16:30:01.000',0.874,0.14,0.168,0.0451,94.566)
,(107,'7MGNHuYwmm9UjQgdVciO1v','Feel (feat. Lianne La Havas)',0.136,'2019-09-27 16:27:37.000',0.836,0.611,0.134,0.0537,115.909)
,(108,'21oJ1K99GBJrE2GVQGVjA0','Frozen',0.227,'2019-09-27 16:19:51.000',0.741,0.486,0.419,0.0563,119.065)
,(109,'66wkCYWlXzSTQAfnsPBptt','My Favorite Part',0.718,'2019-09-27 16:15:46.000',0.627,0.861,0.33,0.0526,95.016)
,(110,'6gL3AXjytTpOkzJeeYRDEi','At The Beginning - Anastasia',0.191,'2019-09-27 16:12:10.000',0.714,0.582,0.572,0.0259,94.005)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(111,'1xk2Z84gbcn4tPXiiutxzS','City Of Stars - From "La La Land" Soundtrack',0.434,'2019-09-27 16:05:37.000',0.899,0.492,0.116,0.0379,111.787)
,(112,'3x28y5GCxnrSBxeHfCLuyi','Himig Ng Pag-Ibig',0.503,'2019-09-27 16:03:06.000',0.0776,0.597,0.709,0.0375,133.946)
,(113,'66H06L8hktjhduwRDWntDT','Stand Still',0.161,'2019-09-27 15:59:20.000',0.732,0.476,0.44,0.0371,149.389)
,(114,'7ClOFUxD5aabYsyKg0j7EV','Cabin Down Below',0.772,'2019-09-27 15:54:36.000',0.00273,0.552,0.919,0.0364,122.948)
,(115,'5Vi5PBLiJAq0GVU1n9yZRB','Sleep On The Floor',0.266,'2019-09-27 15:51:42.000',0.271,0.384,0.445,0.0338,142.048)
,(116,'21oJ1K99GBJrE2GVQGVjA0','Frozen',0.227,'2019-09-27 15:48:09.000',0.741,0.486,0.419,0.0563,119.065)
,(117,'66wkCYWlXzSTQAfnsPBptt','My Favorite Part',0.718,'2019-09-27 15:44:04.000',0.627,0.861,0.33,0.0526,95.016)
,(118,'78MI7mu1LV1k4IA2HzKmHe','Dream A Little Dream Of Me - Single Version',0.394,'2019-09-27 15:40:27.000',0.913,0.443,0.104,0.101,76.497)
,(119,'58dSdjfEYNSxte1aNVxuNf','Easy',0.217,'2019-09-27 15:37:22.000',0.373,0.722,0.282,0.106,91.367)
,(120,'4hOTGmoJTQAZSaqABxPxuS','To Be Alone',0.272,'2019-09-27 15:32:07.000',0.361,0.567,0.437,0.0249,67.048)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(121,'5gbxzSqABThINGDb7vIiwe','Edge of Desire',0.455,'2019-09-27 15:06:04.000',0.326,0.606,0.441,0.0272,66.443)
,(122,'59FC22eN2Syt9bbv2d6393','Black Sun',0.608,'2019-09-27 14:54:43.000',0.17,0.608,0.642,0.0251,87.703)
,(123,'7zFXmv6vqI4qOt4yGf3jYZ','Get You (feat. Kali Uchis)',0.358,'2019-09-27 14:49:54.000',0.422,0.658,0.294,0.0321,74.038)
,(124,'5ltHoAqXvRiOQvcAqpHo3U','From Eden',0.289,'2019-09-27 14:45:15.000',0.62,0.394,0.689,0.0603,142.723)
,(125,'6trOWWOKQeql1UibRk9SBS','Ophelia',0.631,'2019-09-27 14:40:29.000',0.593,0.663,0.588,0.0286,76.044)
,(126,'1lUdXbhl6u6QMQZRTAhlWW','Naked as We Came',0.663,'2019-09-27 14:37:49.000',0.629,0.367,0.208,0.0363,172.358)
,(127,'63bRlSS5g67PIHsogL2xOA','It Don’t Matter (feat. JoJo)',0.608,'2019-09-27 14:35:16.000',0.538,0.712,0.373,0.175,89.891)
,(128,'1FWFmQZwvNctmy8kT5ESw1','Cherry Wine - Live',0.219,'2019-09-27 14:30:55.000',0.958,0.483,0.111,0.0388,74.001)
,(129,'5Vi5PBLiJAq0GVU1n9yZRB','Sleep On The Floor',0.266,'2019-09-27 14:26:53.000',0.271,0.384,0.445,0.0338,142.048)
,(130,'21oJ1K99GBJrE2GVQGVjA0','Frozen',0.227,'2019-09-27 14:23:22.000',0.741,0.486,0.419,0.0563,119.065)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(131,'66wkCYWlXzSTQAfnsPBptt','My Favorite Part',0.718,'2019-09-27 14:19:16.000',0.627,0.861,0.33,0.0526,95.016)
,(132,'78MI7mu1LV1k4IA2HzKmHe','Dream A Little Dream Of Me - Single Version',0.394,'2019-09-27 14:15:40.000',0.913,0.443,0.104,0.101,76.497)
,(133,'58dSdjfEYNSxte1aNVxuNf','Easy',0.217,'2019-09-27 14:12:34.000',0.373,0.722,0.282,0.106,91.367)
,(134,'4hOTGmoJTQAZSaqABxPxuS','To Be Alone',0.272,'2019-09-27 14:07:19.000',0.361,0.567,0.437,0.0249,67.048)
,(135,'1NLk2ytaTQSfgKvBjCRIFY','Gun Song',0.323,'2019-09-27 14:01:55.000',0.302,0.692,0.708,0.0243,96.277)
,(136,'3YnwIp2b99p3e5dsFTXIIx','Dunno',0.0998,'2019-09-27 13:58:18.000',0.768,0.622,0.229,0.0445,81.87)
,(137,'4qkVALwOxCIEZ7I5gkZ3m4','Butterfly',0.12,'2019-09-27 13:54:20.000',0.255,0.785,0.27,0.0892,131.894)
,(138,'0yJi7eb2SosK5CsSnnqc5o','Foreigner''s God',0.355,'2019-09-27 13:51:39.000',0.166,0.514,0.46,0.0293,89.044)
,(139,'0h7ENtmZ9ZyUN3EWwlQ5WA','Gale Song',0.184,'2019-09-27 13:47:54.000',0.72,0.359,0.327,0.0333,176.432)
,(140,'1TNYksIQsadsgxmpeNwfGk','Home',0.31,'2019-09-27 13:44:39.000',0.00601,0.387,0.733,0.0824,118.043)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(141,'4gT3mNJA8lnlkYFqGZ8IA2','Small Worlds',0.515,'2019-09-27 13:41:04.000',0.814,0.516,0.546,0.249,78.267)
,(142,'4Kaw0HUTA9Q3z7Elnqvb8T','Cleopatra',0.462,'2019-09-27 13:34:35.000',0.247,0.538,0.772,0.043,151.367)
,(143,'1Ge1mEPNSgh9hsFCoKzPzR','It Will Come Back',0.157,'2019-09-27 13:31:13.000',0.378,0.49,0.468,0.0354,86.979)
,(144,'5gbxzSqABThINGDb7vIiwe','Edge of Desire',0.455,'2019-09-27 13:26:35.000',0.326,0.606,0.441,0.0272,66.443)
,(145,'5ltHoAqXvRiOQvcAqpHo3U','From Eden',0.289,'2019-09-27 13:20:18.000',0.62,0.394,0.689,0.0603,142.723)
,(146,'6trOWWOKQeql1UibRk9SBS','Ophelia',0.631,'2019-09-27 13:15:35.000',0.593,0.663,0.588,0.0286,76.044)
,(147,'1lUdXbhl6u6QMQZRTAhlWW','Naked as We Came',0.663,'2019-09-27 13:12:54.000',0.629,0.367,0.208,0.0363,172.358)
,(148,'63bRlSS5g67PIHsogL2xOA','It Don’t Matter (feat. JoJo)',0.608,'2019-09-27 13:10:21.000',0.538,0.712,0.373,0.175,89.891)
,(149,'66wkCYWlXzSTQAfnsPBptt','My Favorite Part',0.718,'2019-09-27 13:03:27.000',0.627,0.861,0.33,0.0526,95.016)
,(150,'1OubIZ0ARYCUq5kceYUQiO','Congratulations (feat. Bilal)',0.207,'2019-09-27 12:33:10.000',0.948,0.465,0.225,0.0455,57.75)
;
INSERT INTO db.tracks (id,spotifyid,title,valence,play_date,acousticness,danceability,energy,speechiness,tempo) VALUES 
(151,'2kP72xV4t4LTcuGUqheQkH','Nebaluyo (feat. Oumou Sangaré)',0.483,'2019-09-27 17:01:06.000',0.391,0.585,0.702,0.338,92.959)
,(152,'3nTzwiI3MxJ55m3n5caeco','À Noite - Interlude',0.0358,'2019-09-28 12:39:19.000',0.874,0.14,0.168,0.0451,94.566)
,(153,'7MGNHuYwmm9UjQgdVciO1v','Feel (feat. Lianne La Havas)',0.136,'2019-09-28 12:36:55.000',0.836,0.611,0.134,0.0537,115.909)
,(154,'2YrY6NOa7tpNCgOUnTloj5','Next to You',0.0689,'2019-09-28 15:29:58.000',0.442,0.443,0.332,0.299,87.839)
,(155,'5YK0WaXMtRHeWEn8EIbmPw','Lua (feat. MARO)',0.327,'2019-09-28 12:49:26.000',0.86,0.445,0.179,0.0358,148.094)
,(156,'70A7N2jqbXrZnZgjQKGJUs','Sad Saturdays',0.118,'2019-09-28 15:39:00.000',0.625,0.377,0.152,0.0406,69.969)
,(157,'0jjsLGCJmUzYRu6GKQqlR4','Wait for You',0.179,'2019-09-28 15:34:32.000',0.884,0.468,0.24,0.0427,137.807)
;
