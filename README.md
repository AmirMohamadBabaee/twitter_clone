# twitter_clone
Final Project of AUT DB course in Spring 2021. All of SQL query scripts are mysql-friendly. This project was written by Python3.8 and to use it, you must first change connection configuration
of main.py to configuration of your mysql server. to do this you just need create a new user in mysql and create a database, then add its config to connect method of mysql-connector module.
To create user
```sql
mysql> CREATE USER 'username-you-like'@'localhost' IDENTIFIED BY 'a-strong-password';
```
and then grant all permission to the new user
```sql
mysql> GRANT ALL PRIVILEGES ON * . * TO 'username-you-like'@'localhost';
mysql> FLUSH PRIVILEGES;
```
and finally create database
```sql
mysql> CREATE DATABASE IF NOT EXISTS twitter
```
before start program, you have to change config of mysql connection.
```
host    ="localhost",
user    ="username-you-like",
password="a-strong-password",
database="twitter"
```

To test this program, install requirements of it by `pip`.
like this.
```
pip install -r requirements.txt
```
then you can start program by below command.
```
python3 main.py
```

# Features
  - signup, login and check login history
  - send tweet, and like them or send comment to a tweet
  - follow your friends and ban your enemies :)
  - sendmessage to your friends and share good tweets with them
  - ...
<br>also you can use `help` command to see how to use this app and explore more things in it.

# Requirements
  - Mysql
  - mysql-connector-python
  - prettytable
