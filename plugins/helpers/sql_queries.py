class SqlQueries:
    songplay_table_insert = ("""
        INSERT INTO songplays (
        start_time,
        userid,
        level,
        songid,
        artistid,
        sessionid,
        location,
        user_agent,
        playid)
        SELECT DISTINCT
                TIMESTAMP 'epoch' + events.ts/1000 * interval '1 second'
                AS start_time,
                events.userid,
                events.level,
                songs.song_id,
                songs.artist_id,
                events.sessionid,
                events.location,
                events.useragent,
                md5(events.sessionid || start_time) AS playid
            FROM staging_events events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
            WHERE events.page = 'NextSong'
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
                AND events.userid IS NOT NULL
                AND events.level IS NOT NULL
                AND songs.song_id IS NOT NULL
                AND songs.artist_id IS NOT NULL
                AND events.sessionid IS NOT NULL
                AND events.location IS NOT NULL
                AND events.useragent IS NOT NULL
    """)

    user_table_insert = ("""
        INSERT INTO users (userid, first_name, last_name, gender, level)
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """)

    song_table_insert = ("""
        INSERT INTO songs (songid, title, artistid, year, duration)
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
    """)

    artist_table_insert = ("""
        INSERT INTO artists (
        artistid,
        name,
        location,
        latitude,
        longitude)
        SELECT distinct artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
        INSERT INTO time (start_time, hour, day, week, month, year, weekday)
        SELECT start_time, extract(hour from start_time),
                           extract(day from start_time),
                           extract(week from start_time),
                           extract(month from start_time),
                           extract(year from start_time),
                           extract(dayofweek from start_time)
        FROM songplays
    """)

    create_time_table = ("""
        CREATE TABLE IF NOT EXISTS public.time (
        start_time timestamp NOT NULL PRIMARY KEY,
        hour INT NOT NULL,
        day INT NOT NULL,
        week INT NOT NULL,
        month TEXT NOT NULL,
        year INT NOT NULL,
        weekday TEXT NOT NULL)
        DISTSTYLE all

    """)

    create_artist_table = ("""
        CREATE TABLE IF NOT EXISTS public.artists (
                                    artistid varchar(256) NOT NULL,
                                    name varchar(256),
                                    location varchar(256),
                                    latitude numeric(18,0),
                                    longitude numeric(18,0))
    """)

    create_songplays_table = ("""
        CREATE TABLE IF NOT EXISTS public.songplays (
                playid varchar(32) NOT NULL,
                start_time timestamp NOT NULL,
                userid int4 NOT NULL,
                "level" varchar(256),
                songid varchar(256),
                artistid varchar(256),
                sessionid int4,
                location varchar(256),
                user_agent varchar(256),
                CONSTRAINT songplays_pkey PRIMARY KEY (playid))
    """)

    create_songs_table = ("""
        CREATE TABLE IF NOT EXISTS public.songs (
                songid varchar(256) NOT NULL,
                title varchar(256),
                artistid varchar(256),
                "year" int4,
                duration numeric(18,0),
                CONSTRAINT songs_pkey PRIMARY KEY (songid))
    """)

    create_staging_events_table = ("""
        CREATE TABLE IF NOT EXISTS public.staging_events (
                    artist varchar(256),
                    auth varchar(256),
                    firstname varchar(256),
                    gender varchar(256),
                    iteminsession int4,
                    lastname varchar(256),
                    length numeric(18,0),
                    "level" varchar(256),
                    location varchar(256),
                    "method" varchar(256),
                    page varchar(256),
                    registration numeric(18,0),
                    sessionid int4,
                    song varchar(256),
                    status int4,
                    ts int8,
                    useragent varchar(256),
                    userid int4)
    """)

    create_staging_songs_table = ("""
        CREATE TABLE IF NOT EXISTS public.staging_songs (
                    num_songs int4,
                    artist_id varchar(256),
                    artist_name varchar(256),
                    artist_latitude numeric(18,0),
                    artist_longitude numeric(18,0),
                    artist_location varchar(256),
                    song_id varchar(256),
                    title varchar(256),
                    duration numeric(18,0),
                    "year" int4)

    """)

    create_users_table = ("""
        CREATE TABLE IF NOT EXISTS public.users (
                userid int4 NOT NULL,
                first_name varchar(256),
                last_name varchar(256),
                gender varchar(256),
                "level" varchar(256),
                CONSTRAINT users_pkey PRIMARY KEY (userid))

    """)
