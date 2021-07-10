# SQL Queries of Twitter
#
# initialization of tables of Twitter
# include: user, tweet, message, hashtag, ban,
# follow, last_login, tweet_hashtag, tweet_like
#
# SendTweetLog and SignUpLog are tables which logging
# user activities and used by triggers.

# User Table
init_user_table_query = """CREATE TABLE IF NOT EXISTS user (
	username varchar(20),
    first_name varchar(20),
    last_name varchar(20),
    password varchar(128) not null,
    biography varchar(64),
    date_of_birth date,
    date_joined date,
    primary key(username)
);"""

# Tweet Table
init_tweet_table_query = """CREATE TABLE IF NOT EXISTS tweet (
	tweet_id int auto_increment primary key,
    body varchar(256),
    date_sent date,
    user_sender varchar(20),
    parent_id int,
    foreign key (user_sender) references user(username),
    foreign key (parent_id) references tweet(tweet_id)
);"""

# Message Table
init_message_table_query = """CREATE TABLE IF NOT EXISTS message (
	message_id int auto_increment primary key,
    body varchar(256),
    date_sent datetime,
    user_sender varchar(20) not null,
    user_reciever varchar(20) not null,
    tweet_id int,
    foreign key (user_sender) references user(username),
    foreign key (user_reciever) references user(username),
    foreign key (tweet_id) references tweet(tweet_id)
);"""

# Hashtag Table
init_hashtag_table_query = """CREATE TABLE IF NOT EXISTS hashtag (
	tag char(6) primary key
);"""

# Ban Table
init_ban_table_query = """CREATE TABLE IF NOT EXISTS ban (
	user_banning varchar(20),
    user_banned varchar(20),
    primary key(user_banning, user_banned),
    foreign key (user_banning) references user(username),
    foreign key (user_banned) references user(username)
);"""

# Last Login Table
init_last_login_table_query = """CREATE TABLE IF NOT EXISTS last_login (
	username varchar(20),
    last_login datetime,
    primary key(username, last_login),
    foreign key (username) references user(username)
);"""

# Follow Table
init_follow_table_query = """CREATE TABLE IF NOT EXISTS follow (
	following varchar(20),
    followed varchar(20),
    primary key(following, followed),
    foreign key (following) references user(username),
    foreign key (followed) references user(username)
);"""

# Tweet_hashtag Table
init_tweet_hashtag_table_query = """CREATE TABLE IF NOT EXISTS tweet_hashtag (
	tweet_id int,
    hashtag char(6),
    primary key (tweet_id, hashtag),
    foreign key (tweet_id) references tweet(tweet_id),
    foreign key (hashtag) references hashtag(tag)
);"""

# Tweet_like Table
init_tweet_like_table = """CREATE TABLE IF NOT EXISTS tweet_like (
	tweet_id int,
    username varchar(20),
    primary key (tweet_id, username),
    foreign key (tweet_id) references tweet(tweet_id),
    foreign key (username) references user(username)
);"""

# SendTweetLog Table
init_SendTweetLog_table_query = """CREATE TABLE IF NOT EXISTS SendTweetLog (
	user_sender varchar(20),
    tweet_id int,
    time_sent datetime,
    primary key(user_sender, tweet_id, time_sent)
);"""

# SignUpLog Table
init_SignUpLog_table_query = """CREATE TABLE IF NOT EXISTS SignUpLog (
	username varchar(20),
	time_joined datetime,
	primary key(username, time_joined)
);"""

# Functions
#
# The only function that exists in this application
# is CurrentUser function which return last user who
# login in this application

trust_function_creator = """SET GLOBAL log_bin_trust_function_creators = 1;"""

# CurrentUser Function
init_CurrentUser_function_query = """CREATE FUNCTION CurrentUser()
RETURNS varchar(20)
NOT deterministic
BEGIN
    RETURN (select username 
	from last_login
	order by last_login desc
    limit 1);
END"""

# Procedures
#
# In this application there are a lot of procedures that
# each one of them, handle one of the features of this program.
# like Login, SignUp, Send Tweet, Send Message to your friends,
# Like Tweets and a lot of cool things that you can find them in
# in this application.

# SignUp Procedure
init_SignUp_procedure_query = """CREATE PROCEDURE SignUp(
					username_param varchar(20), 
                    first_name_param varchar(20), 
                    last_name_param varchar(20),
                    password_param varchar(128),
                    biography_param varchar(64),
                    date_of_birth_param date
                    )
BEGIN
	INSERT INTO user(username, first_name, last_name, password, biography, date_of_birth, date_joined) VALUES (
	username_param, first_name_param, last_name_param, sha2(password_param, 512), biography_param, date_of_birth_param, curdate()
);
END"""

# Login Procedure
init_Login_procedure_query = """CREATE PROCEDURE Login(username_login varchar(20), password_login varchar(128))
BEGIN
	IF username_login NOT IN (
		SELECT username
        FROM user
    ) THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'User not found! Please sign up first.', MYSQL_ERRNO = 9990;
    END IF;
    
    IF NOT EXISTS (
		SELECT *
        FROM user
        where (username, password) = (username_login, sha2(password_login, 512))
    ) THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Your password is not correct. Please try again.', MYSQL_ERRNO = 9994;
    END IF;

	INSERT INTO last_login
		SELECT username, now() 
		FROM user
		WHERE (username, password) = (username_login, sha2(password_login, 512));    
END"""

# SendTweet Procedure
init_SendTweet_procedure_query = """CREATE PROCEDURE SendTweet(content varchar(256))
BEGIN
	DECLARE currentUser varchar(20);
    set currentUser = CurrentUser();
    
    IF currentUser IS NULL THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'There is no logined user.', MYSQL_ERRNO = 9993;
    END IF;
    
	INSERT INTO tweet(body, date_sent, user_sender) 
		SELECT content, curdate(), username
		FROM user
		WHERE username = currentUser;
END"""

# SendMessage Procedure
init_SendMessage_procedure_query = """CREATE PROCEDURE SendMessage(content varchar(256), reciever varchar(20), tweet_id_param int)
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();

	IF currentUser IS NULL THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'There is no logined user.', MYSQL_ERRNO = 9993;
    END IF;
    
    IF currentUser IN (
		SELECT user_banned
        FROM ban
        WHERE user_banning = reciever
    ) THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Sorry! You were banned by receiver of this message.', MYSQL_ERRNO = 9981;
    END IF;
    
    IF tweet_id_param IS NOT NULL THEN
		IF tweet_id_param NOT IN (
			SELECT tweet_id
            FROM tweet
        ) THEN 
			SIGNAL SQLSTATE '02000'
				SET MESSAGE_TEXT = 'Selected Tweet wasn`t found.', MYSQL_ERRNO = 9991;
        END IF;
        
        IF currentUser IN (
			SELECT user_banned
            FROM ban
            WHERE user_banning = (
				SELECT user_sender
                FROM tweet
                WHERE tweet_id = tweet_id_param
                LIMIT 1
            )
        ) THEN
			SIGNAL SQLSTATE '45000'
				SET MESSAGE_TEXT = 'Sorry! You were banned by sender of this tweet.', MYSQL_ERRNO = 9980;
        END IF;
    END IF;
    
	INSERT INTO message(body, date_sent, user_sender, user_reciever, tweet_id)
		SELECT content, now(), currentUser, reciever, tweet_id_param
		WHERE reciever NOT IN (
			SELECT user_banning
			FROM ban
			WHERE user_banned = currentUser
			)
			AND (tweet_id_param is null OR 
				tweet_id_param is not null AND (
				SELECT user_sender
				FROM tweet
				WHERE tweet.tweet_id = tweet_id_param
				) NOT IN (
					SELECT user_banning
					FROM ban
					WHERE user_banned = currentUser
				)
			);
END"""

# RemoveBan Procedure
init_RemoveBan_procedure_query = """CREATE PROCEDURE RemoveBan(user_banned_param varchar(20))
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();

	IF currentUser IS NULL THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'There is no logined user.', MYSQL_ERRNO = 9993;
    END IF;
    
    IF NOT EXISTS (
		SELECT *
        FROM ban
        WHERE (user_banning, user_banned) = (currentUser, user_banned_param)
    ) THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'This user was not banned!', MYSQL_ERRNO = 9992;
    END IF;
    
	DELETE FROM ban
	WHERE (user_banning, user_banned) = (currentUser, user_banned_param);
END"""

# AddHashtag Procedure
init_AddHashtag_procedure_query = """CREATE PROCEDURE AddHashtag(tweet_id_param int, hashtag_param char(6))
BEGIN
	INSERT INTO hashtag(tag)
		SELECT hashtag_param
		WHERE hashtag_param LIKE '#_____'
			AND hashtag_param NOT IN (select tag from hashtag);
		
	INSERT INTO tweet_hashtag(tweet_id, hashtag)
		SELECT tweet_id_param, tag
		FROM hashtag
		WHERE tag = hashtag_param
			AND tweet_id_param IN (select tweet_id from tweet);
END"""

# UserLoginHistory Procedure
init_UserLoginHistory_procedure_query = """CREATE PROCEDURE UserLoginHistory (username_login varchar(20))
BEGIN
	IF NOT EXISTS (
		SELECT username
        FROM user
		WHERE username = username_login
    ) THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'User not found! Please sign up first.', MYSQL_ERRNO = 9990;
    END IF;
	SELECT * 
	FROM last_login
	WHERE username = username_login
	ORDER BY last_login DESC;
END"""

# LikeTweet Procedure
init_LikeTweet_procedure_query = """CREATE PROCEDURE LikeTweet(tweet_id_param int)
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();

	IF currentUser IS NULL THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'There is no logined user.', MYSQL_ERRNO = 9993;
    END IF;

	IF NOT EXISTS (
		SELECT tweet_id
        FROM tweet
        WHERE tweet_id = tweet_id_param
    ) THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'Selected Tweet wasn`t found.', MYSQL_ERRNO = 9991;
    END IF;
    
    IF currentUser IN (
		SELECT user_banned
		FROM ban
		WHERE user_banning = (
			SELECT user_sender
            FROM tweet
            WHERE tweet_id = tweet_id_param
		)
    ) THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Sorry! You were banned by sender of this tweet.', MYSQL_ERRNO = 9980;
    END IF;
	
	INSERT INTO tweet_like(tweet_id, username)
		SELECT tweet_id, currentUser
		FROM tweet
		WHERE tweet_id = tweet_id_param
			AND user_sender NOT IN (
				SELECT user_banning
				FROM ban
				WHERE user_banned = currentUser
			);
END"""

# UnfollowUser Procedure
init_UnfollowUser_procedure_query = """CREATE PROCEDURE UnfollowUser(followed_username varchar(20))
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
    
    IF currentUser IS NULL THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'There is no logined user.', MYSQL_ERRNO = 9993;
    END IF;
    
    IF followed_username NOT IN (
		SELECT username
        FROM user
    ) THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'There is no user with this username.', MYSQL_ERRNO = 9995;
    END IF;
    
    IF NOT EXISTS (
		SELECT *
        from follow
        WHERE (following, followed) = (currentUser, followed_username)
    ) THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'This user hasn`t been followed by you.', MYSQL_ERRNO = 9996;
    END IF;
    
	DELETE FROM follow
	WHERE (following, followed) = (currentUser, followed_username);
END"""

# PopularTweets Procedure
init_PopularTweets_procedure_query = """CREATE PROCEDURE PopularTweets()
BEGIN
	DECLARE currentUser varchar(20);
	SET currentUser = CurrentUser();
    
    IF currentUser IS NULL THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'There is no logined user.', MYSQL_ERRNO = 9993;
    END IF;
    
	SELECT t.tweet_id, t.body, t.date_sent, t.user_sender, t.parent_id, tl.likes
	FROM tweet t
	LEFT JOIN (
		SELECT tweet_id, COUNT(*) AS likes
		FROM tweet_like
		GROUP BY tweet_id
	) tl ON t.tweet_id = tl.tweet_id
	WHERE t.user_sender NOT IN (
		SELECT user_banning
		FROM ban
		WHERE user_banned = currentUser
	) 
	ORDER BY likes DESC;
END"""

# MyTweets Procedure
init_MyTweets_procedure_query = """CREATE PROCEDURE MyTweets()
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
    
    IF currentUser IS NULL THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'There is no logined user.', MYSQL_ERRNO = 9993;
    END IF;
    
	SELECT * 
	FROM tweet
	WHERE user_sender = currentUser;
END"""

# TweetsWithHashtag Procedure
init_TweetsWithHashtag_procedure_query = """CREATE PROCEDURE TweetsWithHashtag(hashtag_param char(6))
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
    
    IF currentUser IS NULL THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'There is no logined user.', MYSQL_ERRNO = 9993;
    END IF;
    
	SELECT *
	FROM tweet t
	INNER JOIN tweet_hashtag th
	ON t.tweet_id = th.tweet_id
	WHERE th.hashtag = hashtag_param
		AND t.user_sender NOT IN (
			SELECT user_banning
			FROM ban
			WHERE user_banned = currentUser
		)
	ORDER BY t.date_sent DESC;
END"""

# TweetLikesNumber Procedure
init_TweetLikesNumber_procedure_query = """CREATE PROCEDURE TweetLikesNumber(tweet_id_param int)
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
    
    IF currentUser IS NULL THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'There is no logined user.', MYSQL_ERRNO = 9993;
    END IF;
    
    IF NOT EXISTS (
		SELECT tweet_id
        FROM tweet
        WHERE tweet_id = tweet_id_param
    ) THEN
		SIGNAL SQLSTATE '02000'
			SET MESSAGE_TEXT = 'Selected Tweet wasn`t found.', MYSQL_ERRNO = 9991;
    END IF;
    
	SELECT COUNT(*) AS "Likes number"
	FROM tweet_like tl
	WHERE tl.tweet_id = tweet_id_param
		AND (
			SELECT user_sender
			FROM tweet
			WHERE tweet_id = tl.tweet_id
		) NOT IN (
			SELECT user_banning
			FROM ban
			WHERE user_banned = currentUser
		);
END"""

# FollowingTweets Procedure
init_FollowingTweets_procedure_query = """CREATE PROCEDURE FollowingTweets()
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
	SELECT *
	FROM tweet
	WHERE user_sender IN (
		SELECT followed
		FROM follow
		WHERE following = currentUser
			and followed NOT IN (
				SELECT user_banning
				FROM ban
				WHERE user_banned = currentUser
			)
	);
END"""

# TweetsOf Procedure
init_TweetsOf_procedure_query = """CREATE PROCEDURE TweetsOf(sender_username varchar(20))
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
	SELECT *
	FROM tweet
	WHERE user_sender = sender_username
		and user_sender NOT IN (
			SELECT user_banning
			FROM ban
			WHERE user_banning = user_sender
				and user_banned = currentUser
		);
END"""

# MessageSenderToMe Procedure
init_MessageSenderToMe_procedure_query = """CREATE PROCEDURE MessageSenderToMe()
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
	SELECT DISTINCT user_sender
	FROM message
	WHERE user_reciever = currentUser
	GROUP BY user_sender
	ORDER BY MAX(date_sent) DESC;
END"""

# UsersLikeTweet Procedure
init_UsersLikeTweet_procedure_query = """CREATE PROCEDURE UsersLikeTweet(tweet_id_param int)
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
	SELECT username
	FROM tweet_like tl
	WHERE tl.tweet_id = tweet_id_param
		AND (
			SELECT user_sender
			FROM tweet
			WHERE tweet_id = tl.tweet_id
		) NOT IN (
			SELECT user_banning
			FROM ban
			WHERE user_banned = currentUser
		)
		AND username NOT IN (
			SELECT user_banning
			FROM ban
			WHERE user_banned = currentUser
		);
END"""

# MessagesToMe Procedure
init_MessagesToMe_procedure_query = """CREATE PROCEDURE MessagesToMe()
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
	SELECT * 
	FROM message
	WHERE user_reciever = currentUser
		AND (
			tweet_id is null OR
			tweet_id is not null AND(
				SELECT user_sender
				FROM tweet
				WHERE tweet.tweet_id = message.tweet_id
			) NOT IN (
				SELECT user_banning
				FROM ban
				WHERE user_banned = currentUser
			)
		)
	ORDER BY date_sent DESC;
END"""

# CommentOf Procedure
init_CommentOf_procedure_query = """CREATE PROCEDURE CommentOf(tweet_id_param int)
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
	SELECT *
	FROM tweet t
	WHERE parent_id = tweet_id_param
		AND (
			SELECT user_sender
			FROM tweet
			WHERE tweet_id = t.parent_id
		) NOT IN (
			SELECT user_banning
			FROM ban
			WHERE user_banned = currentUser
		)
		AND user_sender NOT IN (
			SELECT user_banning
			FROM ban
			WHERE user_banned = currentUser
		);
END"""

# FollowUser Procedure
init_FollowUser_procedure_query = """CREATE PROCEDURE FollowUser(followed_username varchar(20))
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
	INSERT INTO follow(following, followed)
		SELECT currentUser, followed_username
		WHERE currentUser in (SELECT username FROM user) 
			and followed_username in (SELECT username FROM user)
            and currentUser <> followed_username;
END"""

# AddBan Procedure
init_AddBan_procedure_query = """CREATE PROCEDURE AddBan(user_banned_param varchar(20))
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
	INSERT INTO ban(user_banning, user_banned)
		SELECT currentUser, user_banned_param
		WHERE currentUser IN (SELECT username FROM user)
			and user_banned_param IN (SELECT username FROM user);
END"""

# SendComment Procedure
init_SendComment_procedure_query = """CREATE PROCEDURE SendComment(content varchar(256), tweet_id_param int)
BEGIN
	DECLARE currentUser varchar(20);
    SET currentUser = CurrentUser();
	INSERT INTO tweet(body, date_sent, user_sender, parent_id) 
		SELECT content, curdate(), currentUser, tweet_id
		FROM tweet
		WHERE tweet_id = tweet_id_param
			and user_sender NOT IN (
			SELECT user_banning
			FROM ban
			WHERE user_banned = currentUser
		);
END"""

# AddHashtagToTweet_Hashtag Procedure
init_AddHashtagToTweet_Hashtag_procedure_query = """CREATE PROCEDURE AddHashtagToTweet_Hashtag(text_in varchar(256), tweet_id_param int)
BEGIN 
	DECLARE x int;
	DECLARE subs varchar(6);
    
    SET x = 1;
    
	loop_label : LOOP
		SET subs = REGEXP_SUBSTR(text_in, '#.....', 1, x);
        IF subs is NULL THEN
			LEAVE loop_label;
        END IF;
        
        SET x = x + 1;
        IF TRIM(subs) LIKE '#_____' THEN 
			call AddHashtag(tweet_id_param, subs);
		END IF;
        
	END LOOP loop_label;
END"""

# Trigger
#
# This application has three Trigger that automate
# some operation of Twitter. 
# SignUpLogger, log new User information in SignUpLog table 
# when registration of user completed. 
# SendTweetLogger, log new Tweet information in SendTweetLog 
# Table after sending
# tweet. 
# AddHashtagOfTweet extract all of Hashtags in body of tweet and 
# create new row in hashtag table for each of then and add them 
# to tweet_hashtag table.

# SignUpLogger Trigger
init_SignUpLogger_trigger_query = """CREATE TRIGGER SignUpLogger
	AFTER INSERT
    ON user FOR EACH ROW
BEGIN
    INSERT INTO SignUpLog(username, time_joined) VALUES (NEW.username, now());
END"""

# SendTweetLogger Trigger
init_SendTweetLogger_trigger_query = """CREATE TRIGGER SendTweetLogger
	AFTER INSERT
    ON tweet FOR EACH ROW
BEGIN
	INSERT INTO SendTweetLog VALUES (NEW.user_sender, NEW.tweet_id, now());
END"""

# AddHashtagOfTweet Trigger
init_AddHashtagOfTweet_trigger_query = """CREATE TRIGGER AddHashtagOfTweet
	AFTER INSERT
    ON tweet FOR EACH ROW
BEGIN
	call AddHashtagToTweet_Hashtag(NEW.body, NEW.tweet_id);
END"""