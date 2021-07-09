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
    except Error as e:
        logger.error('[SignUp] There is a user with entered username.')

def Login(logger, cursor, username : str, password : str):
    try:
        cursor.callproc('Login', args=(username, password,))
        logger.info(f'[Login] User <{username}> successfully logined to Twitter.')
    except Error as e:
        logger.exception('[Login] There is an unhandled problem in login procedure.')

def SendTweet(logger, cursor, content : str):
    try:
        current_user = get_current_user()
        cursor.callproc('SendTweet', args=(content,))
        logger.info(f'[SendTweet] Tweet successfully was sent by <{current_user}>.')
    except Error as e:
        logger.error('[SendTweet] there is an unhandled problem in sending tweet.')

def SendMessage(logger, cursor, content : str, receiver : str, tweet_id : int):
    try: 
        current_user = get_current_user(logger, cursor)
        cursor.callproc('SendMessage', args=(content, receiver, tweet_id))
        logger.warning(f'[SendMessage] {cursor.fetchwarnings()}')
        logger.info(f'[SendMessage] Message successfully was sent from <{current_user}> to <{receiver}>')
    except Error as e:
        if e.errno == 9981:                                                                     # current user was banned by receiver of message
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
    except Error as e:
        if e.errno == 9992:                                                                     # there is no row for this ban property
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
                login_history = [tup[1] for tup in data]
                if len(login_history) > 0:
                    logger.info(f'[UserLoginHistory] <{username}> login history Retrieved successfully.')
                return login_history
    except Error as e:
        if e.errno == 9990:                                                                 # there is no user with this user name in database
            logger.error(f'[UserLoginHistory] {e.msg}')
        else:
            logger.exception('[UserLoginHistory] There is an unhandled problem in this process.')

def LikeTweet(logger, cursor, tweet_id : int):
    try:
        current_user = get_current_user(logger, cursor)
        cursor.callproc('LikeTweet', args=(tweet_id,))
        logger.warning(f'[LikeTweet] {cursor.fetchwarnings()}')
        logger.info(f'[LikeTweet] user <{current_user}> liked tweet <{tweet_id}>.')
    except Error as e:
        if e.errno == 9991:                                                                     # there is no tweet with this tweet id
            logger.error(f'[LikeTweet] {e.msg}')
        elif e.errno == 9980:                                                                   # current user was banned by sender of tweet
            logger.error(f'[LikeTweet] {e.msg}')
        elif e.errno == 1062:                                                                   # duplicate of primary key
            logger.error('[LikeTweet] You have already liked this tweet.')
        else:
            logger.exception('[LikeTweet] There is an unhandled problem in this process.')