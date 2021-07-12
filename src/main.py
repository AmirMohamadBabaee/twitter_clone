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
                
                print("""
 /$$$$$$$$            /$$   /$$     /$$                        
|__  $$__/           |__/  | $$    | $$                        
   | $$ /$$  /$$  /$$ /$$ /$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$ 
   | $$| $$ | $$ | $$| $$|_  $$_/|_  $$_/   /$$__  $$ /$$__  $$
   | $$| $$ | $$ | $$| $$  | $$    | $$    | $$$$$$$$| $$  \__/
   | $$| $$ | $$ | $$| $$  | $$ /$$| $$ /$$| $$_____/| $$      
   | $$|  $$$$$/$$$$/| $$  |  $$$$/|  $$$$/|  $$$$$$$| $$      
   |__/ \_____/\___/ |__/   \___/   \___/   \_______/|__/      
                                                               
                """)
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
                        """
                        Tweet command
                        You can use this command to send your own tweet to show to the World that you are so creative
                        and so cool. just you need write your text after this command

                        inputs:
                            content     -> string content at most with 256 characters
                        """
                        
                        if len(args) != 1:

                            args = list()
                            args.append(input('content > '))

                        functions.SendTweet(logger, cursor, *args)

                    elif com.lower() == 'liketweet':
                        """
                        LikeTweet command
                        You can like tweets which you think are beautiful, creative and innovative.

                        inputs: 
                            tweet_id    -> id of tweet you are interested to like it which is a integer number
                        """

                        if len(args) != 1:

                            args = list()
                            args.append(input('tweet_id > '))

                        functions.LikeTweet(logger, cursor, *args)

                    elif com.lower() == 'tweetlikesnum':
                        """
                        TweetLikesNum command
                        Find out how many users like a tweet. likes number can be an indicator for users interest

                        inputs:
                            tweet_id    -> id of tweet you are interested to see its like number
                        """

                        if len(args) != 1:

                            args = list()
                            args.append(input('tweet_id > '))

                        data = functions.TweetLikesNumber(logger, cursor, *args)
                        print(f'{data} users like this post until now.')

                    elif com.lower() == 'likers':
                        """
                        Likers
                        You can see users who like a special tweet, actually users who they didn`t ban you.

                        inputs:
                            tweet_id    -> id of tweet which you like to see users who like it
                        """
                        
                        if len(args) != 1:

                            args = list()
                            args.append(input('tweet_id > '))

                        data = functions.UsersLikeTweet(logger, cursor, *args)
                        if data:
                            likers_table = PrettyTable()
                            likers_table.field_names = [f'Users who liked tweet <{args[0]}>']
                            likers_table.add_rows(data)
                            print(likers_table)
                        else:
                            print('No one liked this tweet :(')

                    elif com.lower() == 'comment':
                        """
                        Comment Command
                        You can use this comment to show your comment about a tweet and share your opinion with other people

                        inputs:
                            content     -> string at most with 256 characters
                            tweet_id    -> id of tweet which you want add a comment to it
                        """
                        
                        if len(args) != 2:

                            args = list()
                            args.append(input('content > '))
                            args.append(input('tweet_id > '))

                        functions.SendComment(logger, cursor, *args)

                    elif com.lower() == 'commentsof':
                        """
                        CommentsOf command
                        This command return comments which replied to a specific tweet

                        inputs:
                            tweet_id    -> id of tweet that you want see its comments.
                        """
                        
                        if len(args) != 1:
                            
                            args = list()
                            args.append(input('tweet_id > '))

                        data = functions.CommentOf(logger, cursor, *args)
                        if data:
                            comments_table = PrettyTable()
                            comments_table.field_names = ['Comment ID', 'Content', 'Sent Date', 'Sender', 'Replied to']
                            comments_table.add_rows(data)
                            print(comments_table)
                        else:
                            print(f'tweet <{args[0]}> does not have any comment')

                    elif com.lower() == 'tweetsof':
                        """
                        TweetsOf command
                        Find out Tweets of every user which is in twitter platform.

                        inputs:
                            username    -> string at most with 20 character
                        """
                        
                        if len(args) != 1:

                            args = list()
                            args.append(input('username > '))

                        data = functions.TweetsOf(logger, cursor, *args)
                        if data:
                            tweets_table = PrettyTable()
                            tweets_table.field_names = ['Tweet ID', 'Content', 'Sent Date', 'Sender', 'Replied to']
                            tweets_table.add_rows(data)
                            print(tweets_table)
                        else:
                            print(f'user <{args[0]}> does not have any tweet')

                    elif com.lower() == 'hashtagtweets':
                        """
                        HashtagTweets command
                        You can find every tweets with specific hashtag.

                        inputs:
                            hashtag     -> string with exactly 6 character which starts with #
                        """
                        
                        if len(args) != 1:

                            args = list()
                            args.append(input('hashtag > '))

                        data = functions.TweetsWithHashtag(logger, cursor, *args)
                        if data:
                            hashtag_table = PrettyTable()
                            hashtag_table.field_names = ['Tweet ID', 'Content', 'Sent Date', 'Sender', 'Replied to', 'Tweet ID(duplicate)', 'Hashtag']
                            hashtag_table.add_rows(data)
                            print(hashtag_table)
                        else:
                            print(f'There is no tweet with <{args[0]}> hashtag.')

                    elif com.lower() == 'populartweets':
                        """
                        PopularTweets command
                        You can find hot tweets which are so popular and reacted to them.

                        without any input
                        """

                        data = functions.PopularTweets(logger, cursor)
                        if data:
                            pop_table = PrettyTable()
                            pop_table.field_names = ['Tweet ID', 'Content', 'Sent Date', 'Sender', 'Replied to', 'Likes Number']
                            pop_table.add_rows(data)
                            print(pop_table)
                        else:
                            print(f'There is no popular tweet :(')

                    elif com.lower() == 'followingtweets':
                        """
                        FollowingTweets command
                        You can check current activities of your following easier than what you can imagine

                        without any input
                        """

                        data = functions.FollowingTweets(logger, cursor)
                        if data:
                            followings_table = PrettyTable()
                            followings_table.field_names = ['Tweet ID', 'Content', 'Sent Date', 'Sender', 'Replied to']
                            followings_table.add_rows(data)
                            print(followings_table)
                        else:
                            print(f'There is no tweet from your followings.')

                    elif com.lower() == 'mytweets':
                        """
                        MyTweets Command
                        You can find your sent tweets by this command

                        without any inputs
                        """

                        data = functions.MyTweets(logger, cursor)
                        if data:
                            my_table = PrettyTable()
                            my_table.field_names = ['Tweet ID', 'Content', 'Sent Date', 'Sender', 'Replied to']
                            my_table.add_rows(data)
                            print(my_table)
                        else:
                            print(f'there is no tweet from you :(')

                    elif com.lower() == 'message':
                        """
                        Message Command
                        Message your friends directly by using message feature of Twitter

                        inputs:
                            content     -> string at most with 256 characters
                            receiver    -> username of any user of this platform
                            tweet_id    -> id of tweet you want to forward for your friend(optional)
                        """
                        
                        if len(args) != 3:

                            args = list()
                            args.append(input('content > '))
                            args.append(input('receiver > '))
                            tweet_id = input('tweet_id > ')
                            args.append(tweet_id if tweet_id else None)

                        functions.SendMessage(logger, cursor, *args)

                    elif com.lower() == 'messageinbox':
                        """
                        MessageInbox command
                        You can find out which users have already send a message for you.

                        without any inputs
                        """

                        data = functions.MessageSenderToMe(logger, cursor)
                        if data:
                            inbox_table = PrettyTable()
                            inbox_table.field_names = ['Inbox']
                            inbox_table.add_rows(data)
                            print(inbox_table)
                        else:
                            print(f'Your inbox is empty :(')

                    elif com.lower() == 'messagesfrom':
                        """
                        MessagesFrom command
                        This command let you to see sent message from specific user to you

                        inputs:
                            username    -> string at most with 20 characters
                        """
                        
                        if len(args) != 1:

                            args = list()
                            args.append(input('username > '))

                        data = functions.MessagesToMe(logger, cursor, *args)
                        if data:
                            message_table = PrettyTable()
                            message_table.field_names = ['Message ID', 'Content', 'Sent Time', 'Sender', 'Receiver', 'Forwarded Tweet ID']
                            message_table.add_rows(data)
                            print(message_table)
                        else:
                            print(f'There is no message for you from user <{args[0]}>')

                    elif com.lower() in ('help', 'h'):
                        """
                        Help command
                        This command print this text.
                        """
                        with open('help.txt', 'r') as f:
                            text = f.read()
                            print(text)

                    connection.commit()
    except Error as e:
        logger.exception('An error occurred in database initialization')

