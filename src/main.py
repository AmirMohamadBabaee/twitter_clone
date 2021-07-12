from mysql.connector import connect, Error
from prettytable import PrettyTable
from query import *
import functions
import logging
import getpass

def config_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f'{__name__}.log')

    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.WARNING)

    console_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    file_fomrat = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_fomrat)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def init_db(connection, cursor, logger):
    try:
        # create tables
        cursor.execute(init_user_table_query)
        cursor.execute(init_tweet_table_query)
        cursor.execute(init_message_table_query)
        cursor.execute(init_hashtag_table_query)
        cursor.execute(init_ban_table_query)
        cursor.execute(init_last_login_table_query)
        cursor.execute(init_follow_table_query)
        cursor.execute(init_tweet_hashtag_table_query)
        cursor.execute(init_tweet_like_table)
        cursor.execute(init_SignUpLog_table_query)
        cursor.execute(init_SendTweetLog_table_query)
        logger.info('[init_db] tables created successfully.')

        # create functions
        cursor.execute(trust_function_creator)
        cursor.execute(init_CurrentUser_function_query)
        logger.info('[init_db] function created successfully.')

        # create procedures
        cursor.execute(init_SignUp_procedure_query)
        cursor.execute(init_Login_procedure_query)
        cursor.execute(init_SendTweet_procedure_query)
        cursor.execute(init_SendMessage_procedure_query)
        cursor.execute(init_RemoveBan_procedure_query)
        cursor.execute(init_AddHashtag_procedure_query)
        cursor.execute(init_UserLoginHistory_procedure_query)
        cursor.execute(init_LikeTweet_procedure_query)
        cursor.execute(init_UnfollowUser_procedure_query)
        cursor.execute(init_PopularTweets_procedure_query)
        cursor.execute(init_MyTweets_procedure_query)
        cursor.execute(init_TweetsWithHashtag_procedure_query)
        cursor.execute(init_TweetLikesNumber_procedure_query)
        cursor.execute(init_FollowingTweets_procedure_query)
        cursor.execute(init_TweetsOf_procedure_query)
        cursor.execute(init_MessageSenderToMe_procedure_query)
        cursor.execute(init_UsersLikeTweet_procedure_query)
        cursor.execute(init_MessagesToMe_procedure_query)
        cursor.execute(init_CommentOf_procedure_query)
        cursor.execute(init_FollowUser_procedure_query)
        cursor.execute(init_AddBan_procedure_query)
        cursor.execute(init_SendComment_procedure_query)
        cursor.execute(init_AddHashtagToTweet_Hashtag_procedure_query)
        logger.info('[init_db] procedures created successfully.')

        # create trigger
        cursor.execute(init_SignUpLogger_trigger_query)
        cursor.execute(init_SendTweetLogger_trigger_query)
        cursor.execute(init_AddHashtagOfTweet_trigger_query)
        logger.info('[init_db] triggers created successfully.')

        # commit changes
        connection.commit()
        logger.info('[init_db] Database successfully initialized.')
    except Error as e:
        logger.warning(f'[init_db] {cursor.fetchwarnings()}')
        logger.warning('[init_db] Database has already been initialized.')


if __name__ == '__main__':

    logger = config_logger()
    logger.info('Twitter Started.')
    try:
        logger.info('Try to connect to database.')
        with connect(
            host="localhost",
            user="twitter_admin",
            password="admin_admin",
            database="Twitter"
        ) as connection:
            logger.info('Program connected to database successfully.')
            with connection.cursor() as cursor:
                logger.info('initialize db.')
                init_db(connection, cursor, logger)
                
                print('Welcome To Twitter\n')
                
                interactive = True
                while interactive:

                    ps = '\n>>>'
                    current_user = functions.get_current_user(logger, cursor)
                    if current_user:
                        ps = f'\n[ {current_user} ] >>> '
                    
                    command = input(ps)

                    if command.lower() in ('q', 'quit'):
                        logger.info('shutting down program.')
                        print('Have a Good day, dude. :)\nRemember us.\nTwitter')
                        interactive = False
                        continue

                    com, *args = command.split()

                    if com.lower() == 'signup':
                        """
                        SignUp command
                        You can use this command to create your first account and enjoy a lot of cool tweets which are post everyday

                        inputs:
                            username    -> string at most with 20 characters which must be unique
                            firstname   -> string at most with 20 characters
                            lastname    -> string at most with 20 characters
                            password    -> password of your account (please set a powerful password and do not use frequent passwords like 123456)
                            biography   -> string at most with 64 characters, a text that describe you as good as possible
                            birthdate   -> date with form %Y-%m-%d like 2020-03-09
                        """

                        if len(args) != 6:

                            args = list()
                            args.append(input('username > '))
                            args.append(input('firstname > '))
                            args.append(input('lastname > '))
                            args.append(getpass.getpass(prompt='password (not shown)> '))
                            args.append(input('biography > '))
                            args.append(input('birthdate (like 2020-03-09) > '))

                        functions.SignUp(logger, cursor, *args)

                    elif com.lower() == 'login':
                        """
                        Login command
                        You can use this command to login to your account and start using this fabulous app.

                        inputs:
                            username    -> string at most with 20 characters
                            password    -> password of your account
                        """

                        if len(args) != 2:

                            args = list()
                            args.append(input('username > '))
                            args.append(getpass.getpass(prompt='password (not shown) > '))

                        functions.Login(logger, cursor, *args)

                    elif com.lower() == 'history':
                        """
                        History command
                        You can find last login of your self and other users of Twitter with this powerful command.

                        inputs:
                            username    -> string at most with 20 characters
                        """
                        
                        if len(args) != 1:

                            args = list()
                            args.append(input('username > '))

                        user_login_table = PrettyTable()
                        user_login_table.field_names = ['Last Login']
                        data = functions.UserLoginHistory(logger, cursor, *args)
                        if data:
                            user_login_table.add_rows(data)
                            print(f'\t[{args[0]}]')
                            print(user_login_table)


                    elif com.lower() == 'follow':
                        """
                        Follow command
                        You can use this command to follow users has registered in Twitter to follow their activities
                        and their tweets.

                        inputs:
                            username    -> string at most with 20 characters
                        """
                        
                        if len(args) != 1:

                            args = list()
                            args.append(input('username > '))

                        functions.FollowUser(logger, cursor, *args)

                    elif com.lower() == 'unfollow':
                        """
                        Unfollow command
                        You can unfollow users that you have already followed

                        inputs:
                            username    -> string at most with 20 characters
                        """
                        
                        if len(args) != 1:

                            args = list()
                            args.append(input('username > '))

                        functions.UnfollowUser(logger, cursor, *args)

                    elif com.lower() == 'ban':
                        """
                        Ban command
                        You can ban users who seems have ironic tweets or something worse than we can think

                        inputs:
                            username    -> string at most with 20 characters
                        """
                        
                        if len(args) != 1:

                            args = list()
                            args.append(input('username > '))

                        functions.AddBan(logger, cursor, *args)

                    elif com.lower() == 'unban':
                        """
                        Unban command
                        You can unban each user who has been banned by you

                        inputs:
                            username    -> string at most with 20 characters
                        """
                        
                        if len(args) != 1:

                            args = list()
                            args.append(input('username > '))

                        functions.RemoveBan(logger, cursor, *args)

                    elif com.lower() == 'tweet':
                        pass
                    elif com.lower() == 'liketweet':
                        pass
                    elif com.lower() == 'tweetlikesnum':
                        pass
                    elif com.lower() == 'likers':
                        pass
                    elif com.lower() == 'comment':
                        pass
                    elif com.lower() == 'commentsof':
                        pass
                    elif com.lower() == 'tweetsof':
                        pass
                    elif com.lower() == 'hashtagtweets':
                        pass
                    elif com.lower() == 'populartweets':
                        pass
                    elif com.lower() == 'followingstweets':
                        pass
                    elif com.lower() == 'mytweet':
                        pass
                    elif com.lower() == 'message':
                        pass
                    elif com.lower() == 'messageinbox':
                        pass
                    elif com.lower() == 'messagesfrom':
                        pass

                    connection.commit()
    except Error as e:
        logger.exception('An error occurred in database initialization')

