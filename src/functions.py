from mysql.connector import Error


def get_current_user(logger, cursor):
    try:

        cursor.execute('select CurrentUser()')
        current_user = cursor.fetchone()
        if current_user:
            logger.info(f'[current user] = {current_user[0]}')
            return current_user[0]

    except Error as e:
        logger.error('[get_current_user] no user has logined yet.')


def SignUp(logger, cursor, username : str, firstname : str, lastname : str, password : str, biography : str, date_of_birth : str):

    try:

        cursor.callproc('SignUp', args=(username, firstname, lastname, password, biography, date_of_birth,))
        logger.info('[SignUp] User created successfully')
        return True

    except Error as e:

        if e.errno == 1062:
            logger.error('[SignUp] There is a user with entered username. Please choose another username.')
        else:
            logger.exception('[SignUp] There is an unhandled problem in sign up procedure.')


def Login(logger, cursor, username : str, password : str):

    try:

        cursor.callproc('Login', args=(username, password,))
        logger.info(f'[Login] User <{username}> successfully logined to Twitter.')
        return True

    except Error as e:

        if e.errno == 9990:                                                                     # username not exists between registered users
            logger.error(f'[Login] {e.msg}')
        elif e.errno == 9994:                                                                   # user exists but password is not correct
            logger.error(f'[Login] {e.msg}')
        else:
            logger.exception('[Login] There is an unhandled problem in login procedure.')


def SendTweet(logger, cursor, content : str):

    try:

        current_user = get_current_user(logger, cursor)
        cursor.callproc('SendTweet', args=(content,))
        logger.info(f'[SendTweet] Tweet successfully was sent by <{current_user}>.')
        return True

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[SendTweet] {e.msg}')
        else:
            logger.exception('[SendTweet] there is an unhandled problem in sending tweet.')


def SendMessage(logger, cursor, content : str, receiver : str, tweet_id : int):

    try: 

        current_user = get_current_user(logger, cursor)
        cursor.callproc('SendMessage', args=(content, receiver, tweet_id))
        logger.warning(f'[SendMessage] {cursor.fetchwarnings()}')
        logger.info(f'[SendMessage] Message successfully was sent from <{current_user}> to <{receiver}>')
        return True

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[SendMessage] {e.msg}')
        elif e.errno == 9981:                                                                   # current user was banned by receiver of message
            logger.error(f'[SendMessage] {e.msg}')
        elif e.errno == 9991:                                                                   # there is no message with this tweet_id
            logger.error(f'[SendMessage] {e.msg}')
        elif e.errno == 9980:                                                                   # current user was banned by sender of forwarded tweet
            logger.error(f'[SendMessage] {e.msg}')
        else:
            logger.exception(f'[SendMessage] There is an unhandled problem in sending message to <{receiver}>.')


def RemoveBan(logger, cursor, username : str):

    try:

        current_user = get_current_user(logger, cursor)
        cursor.callproc('RemoveBan', args=(username,))
        logger.warning(f'[RemoveBan] {cursor.fetchwarnings()}')
        logger.info(f'[RemoveBan] User <{current_user}> successfully unbanned user <{username}>.')
        return True

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[RemoveBan] {e.msg}')
        elif e.errno == 9992:                                                                   # there is no row for this ban property
            logger.error(f'[RemoveBan] {e.msg}')
        else:
            logger.exception('[RemoveBan] There is an unhandled problem in unbanning process')


def UserLoginHistory(logger, cursor, username : str):

    try:

        cursor.callproc('UserLoginHistory', args=(username,))
        logger.warning(f'[UserLoginHistory] {cursor.fetchwarnings()}')

        if cursor.with_rows:
            for res in cursor.stored_results():
                data = res.fetchall()
                login_history = [(tup[1],) for tup in data]

                if len(login_history) > 0:
                    logger.info(f'[UserLoginHistory] <{username}> login history Retrieved successfully.')

                return login_history

    except Error as e:

        if e.errno == 9990:                                                                 # there is no user with this username in database
            logger.error(f'[UserLoginHistory] {e.msg}')
        else:
            logger.exception('[UserLoginHistory] There is an unhandled problem in this process.')


def LikeTweet(logger, cursor, tweet_id : int):

    try:

        current_user = get_current_user(logger, cursor)
        cursor.callproc('LikeTweet', args=(tweet_id,))
        logger.warning(f'[LikeTweet] {cursor.fetchwarnings()}')
        logger.info(f'[LikeTweet] user <{current_user}> liked tweet <{tweet_id}>.')
        return True

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[LikeTweet] {e.msg}')
        elif e.errno == 9991:                                                                   # there is no tweet with this tweet id
            logger.error(f'[LikeTweet] {e.msg}')
        elif e.errno == 9980:                                                                   # current user was banned by sender of tweet
            logger.error(f'[LikeTweet] {e.msg}')
        elif e.errno == 1062:                                                                   # duplicate of primary key
            logger.error('[LikeTweet] You have already liked this tweet.')
        else:
            logger.exception('[LikeTweet] There is an unhandled problem in this process.')


def UnfollowUser(logger, cursor, username : str):
    
    try:

        current_user = get_current_user(logger, cursor)
        cursor.callproc('UnfollowUser', args=(username,))
        logger.warning(f'[UnfollowUser] {cursor.fetchwarnings()}')
        logger.info(f'[UnfollowUser] user <{current_user}> unfollowed <{username}>')
        return True

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[UnfollowUser] {e.msg}')
        elif e.errno == 9995:                                                                   # there is no registered user with this username
            logger.error(f'[UnfollowUser] {e.msg}')
        elif e.errno == 9996:                                                                   # this user has not been followed by current user
            logger.error(f'[UnfollowUser] {e.msg}')
        else:
            logger.exception('[UnfollowUser] There is an unhandled problem in this process')


def PopularTweets(logger, cursor):

    try:
        
        cursor.callproc('PopularTweets')
        logger.warning(f'[PopularTweets] {cursor.fetchwarnings()}')

        for res in cursor.stored_results():
            data = res.fetchall()
            logger.info('[PopularTweets] Popular Tweets successfully retrieved.')
            return data

    except Error as e:

        if e.errno == 9993:                                                                      # there is no logined user
            logger.error(f'[PopularTweets] {e.msg}')
        else:
            logger.exception('[PopularTweets] There is an unhandled problem in this process')


def MyTweets(logger, cursor):
    try:

        current_user = get_current_user(logger, cursor)
        cursor.callproc('MyTweets')
        logger.warning(f'[MyTweets] {cursor.fetchwarnings()}')

        for res in cursor.stored_results():
            data = res.fetchall()
            logger.info('[MyTweets] My Tweets successfully retrieved.')
            return data

    except Error as e:

        if e.errno == 9993:                                                                      # there is no logined user
            logger.error(f'[MyTweets] {e.msg}')
        else:
            logger.exception('[MyTweets] There is an unhandled problem in this process')


def TweetsWithHashtag(logger, cursor, hashtag : str):

    try:

        cursor.callproc('TweetsWithHashtag', args=(hashtag,))
        logger.warning(f'[TweetsWithHashtag] {cursor.fetchwarnings()}')

        for res in cursor.stored_results():
            data = res.fetchall()
            logger.info(f'[TweetsWithHashtag] Tweets with <{hashtag}> successfully retrieved.')
            return data

    except Error as e:

        if e.errno == 9993:                                                                      # there is no logined user
            logger.error(f'[TweetsWithHashtag] {e.msg}')
        else:
            logger.exception('[TweetsWithHashtag] There is an unhandled problem in this process.')


def TweetLikesNumber(logger, cursor, tweet_id : int):

    try:

        cursor.callproc('TweetLikesNumber', args=(tweet_id,))
        logger.warning(f'[TweetLikesNumber] {cursor.fetchwarnings()}')

        for res in cursor.stored_results():
            data = res.fetchall()
            logger.info(f'[TweetLikesNumber] Likes number of tweet <{tweet_id}> successfully retrieved.')
            return data[0][0]

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[TweetLikesNumber] {e.msg}')
        elif e.errno == 9991:                                                                   # there is no tweet with this tweet id
            logger.error(f'[TweetLikesNumber] {e.msg}')
        else:
            logger.exception('[TweetLikesNumber] There is an unhandled problem in this process.')


def FollowingTweets(logger, cursor):

    try:

        current_user = get_current_user(logger, cursor)
        cursor.callproc('FollowingTweets')
        logger.warning(f'[FollowingTweets] {cursor.fetchwarnings()}')

        for res in cursor.stored_results():
            data = res.fetchall()
            logger.info(f'[FollowingTweets] Tweets of followed user by user <{current_user}>')
            return data

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[FollowingTweets] {e.msg}')
        else:
            logger.exception('[FollowingTweets] There is an unhandled problem in this process.')


def TweetsOf(logger, cursor, username : str):

    try:

        cursor.callproc('TweetsOf', args=(username,))
        logger.warning(f'[TweetsOf] {cursor.fetchwarnings()}')

        for res in cursor.stored_results():
            data = res.fetchall()
            logger.info(f'[TweetsOf] Tweets of user <{username}> successfully retrieved.')
            return data

    except Error as e:

        if e.errno == 9993:                                                                      # there is no logined user
            logger.error(f'[TweetsOf] {e.msg}')
        elif e.errno == 9995:                                                                    # there is no registered user with this username
            logger.error(f'[TweetsOf] {e.msg}')
        elif e.errno == 9982:                                                                    # current user was banned by user with this username
            logger.error(f'[TweetsOf] {e.msg}')
        else:
            logger.exception('[TweetsOf] There is an unhandled problem in this process.')


def MessageSenderToMe(logger, cursor):

    try:

        current_user = get_current_user(logger, cursor)
        cursor.callproc('MessageSenderToMe')
        logger.warning(f'[MessageSenderToMe] {cursor.fetchwarnings()}')

        for res in cursor.stored_results():
            data = res.fetchall()
            logger.info(f'[MessageSenderToMe] Message Senders to user <{current_user}> successfully retrieved.')
            data = list(map(lambda x : x[0], data))
            return data

    except Error as e:

        if e.errno == 9993:
            logger.error(f'[MessageSenderToMe] {e.msg}')
        else:
            logger.exception('[MessageSenderToMe] There is an unhandled problem in this process')


def UsersLikeTweet(logger, cursor, tweet_id : int):

    try:

        cursor.callproc('UsersLikeTweet', args=(tweet_id,))
        logger.warning(f'[UsersLikeTweet] {cursor.fetchwarnings()}')

        for res in cursor.stored_results():
            data = res.fetchall()
            logger.info(f'[UsersLikeTweet] Users who liked tweet <{tweet_id}> successfully retrieved.')
            data = list(map(lambda x : x[0], data))
            return data

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[UsersLikeTweet] {e.msg}')
        elif e.errno == 9991:                                                                   # there is no tweet with this tweet id
            logger.error(f'[UsersLikeTweet] {e.msg}')
        elif e.errno == 9980:                                                                   # current user was banned by sender of tweet
            logger.error(f'[UsersLikeTweet] {e.msg}')
        else:
            logger.exception('[UsersLikeTweet] There is an unhandled problem in this process.')


def MessagesToMe(logger, cursor, username : str):

    try:

        current_user = get_current_user(logger, cursor)
        cursor.callproc('MessagesToMe', args=(username,))
        logger.warning(f'[MessagesToMe] {cursor.fetchwarnings()}')

        for res in cursor.stored_results():
            data = res.fetchall()
            logger.info(f'[MessagesToMe] Messages from user <{username}> to user <{current_user}> successfully retrieved.')
            return data

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[MessagesToMe] {e.msg}')
        elif e.errno == 9995:                                                                   # there is no registered user with this username
            logger.error(f'[MessagesToMe] {e.msg}')
        else:
            logger.exception('[MessagesToMe] There is an unhandled problem in this process')


def CommentOf(logger, cursor, tweet_id):

    try:

        cursor.callproc('CommentOf', args=(tweet_id,))
        logger.warning(f'[CommentOf] {cursor.fetchwarnings()}')

        for res in cursor.stored_results():
            data = res.fetchall()
            logger.info(f'[CommentOf] Comments of tweet <{tweet_id}> successfully retrieved.')
            return data

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[CommentOf] {e.msg}')
        elif e.errno == 9991:                                                                   # there is no tweet with this tweet id
            logger.error(f'[CommentOf] {e.msg}')
        elif e.errno == 9980:                                                                   # current user was banned by sender of tweet
            logger.error(f'[CommentOf] {e.msg}')
        else:
            logger.exception('[CommentOf] There is an unhandled problem in this process')


def FollowUser(logger, cursor, username : str):

    try:

        current_user = get_current_user(logger, cursor)
        cursor.callproc('FollowUser', args=(username,))
        logger.warning(f'[FollowUser] {cursor.fetchwarnings()}')
        logger.info(f'user <{current_user}> successfully followed user <{username}>.')
        return True

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[FollowUser] {e.msg}')
        elif e.errno == 9995:                                                                   # there is no registered user with this username
            logger.error(f'[FollowUser] {e.msg}')
        elif e.errno == 9983:                                                                   # current user cannot follow himself/herself
            logger.error(f'[FollowUser] {e.msg}')
        elif e.errno == 1062:                                                                   # duplicate of primary key
            logger.error('[FollowUser] You have already followed this user.')
        else:
            logger.exception('[FollowUser] There is an unhandled problem in this process')


def AddBan(logger, cursor, username : str):

    try:

        current_user = get_current_user(logger, cursor)
        cursor.callproc('AddBan', args=(username,))
        logger.warning(f'[AddBan] {cursor.fetchwarnings()}')
        logger.info(f'[AddBan] user <{current_user}> successfully banned user <{username}>.')
        return True

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[AddBan] {e.msg}')
        elif e.errno == 9995:                                                                   # there is no registered user with this username
            logger.error(f'[AddBan] {e.msg}')
        elif e.errno == 9984:                                                                   # current user cannot ban himself/herself
            logger.error(f'[AddBan] {e.msg}')
        elif e.errno == 1062:                                                                   # duplicate of primary key
            logger.error(f'[AddBan] You have already benned this user.')
        else:
            logger.exception('[AddBan] There is an unhandled problem in this process')


def SendComment(logger, cursor, content : str, tweet_id : int):

    try:

        current_user = get_current_user(logger, cursor)
        cursor.callproc('SendComment', args=(content, tweet_id,))
        logger.warning(f'[SendComment] {cursor.fetchwarnings()}')
        logger.info(f'[SendComment] user <{current_user}> successfully commented on tweet <{tweet_id}>.')
        return True

    except Error as e:

        if e.errno == 9993:                                                                     # there is no logined user
            logger.error(f'[SendComment] {e.msg}')
        elif e.errno == 9991:                                                                   # there is no tweet with this tweet id
            logger.error(f'[SendComment] {e.msg}')
        elif e.errno == 9980:                                                                   # current user was banned by sender of tweet
            logger.error(f'[SendComment] {e.msg}')
        elif e.errno == 1062:                                                                   # duplicate of primary key
            logger.error(f'[SendComment] This comment is duplicated.')
        else:
            logger.exception('[SendComment] There is an unhandled problem in this process')