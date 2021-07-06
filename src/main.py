from mysql.connector import connect, Error
from query import *
import logging

def init_db(connection, cursor):
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
        print('tables created successfully.')

        # create functions
        cursor.execute(trust_function_creator)
        cursor.execute(init_CurrentUser_function_query)
        print('function created successfully.')

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
        print('procedures created successfully.')

        # create trigger
        cursor.execute(init_SignUpLogger_trigger_query)
        cursor.execute(init_SendTweetLogger_trigger_query)
        cursor.execute(init_AddHashtagOfTweet_trigger_query)
        print('triggers created successfully.')

        # commit changes
        connection.commit()
        print('Database successfully initialized.')
    except Error as e:
        print('Error In Init_db:', e)

try:
    with connect(
        host="localhost",
        user="twitter_admin",
        password="admin_admin",
        database="t"
    ) as connection:
        print(connection)
        with connection.cursor() as cursor:
            init_db(connection, cursor)
except Error as e:
    print('Error:', e)