# Cactus Api Login

This API provides a user authentication system. It allows you to create, verify and authenticate users, and perform profile update and delete operations.

## API URL

https://cactus-api-login-4453c01c9d7e.herokuapp.com/

## Instalación

pip install -r requirements.txt

## API usage

### Create a User

POST /user/create

Create a new user in the database.

Request Parameters
username (string): Username.
password (string): User password.
email (string): User's email address.

### Login session

POST /login

Log in and return a valid JWT token.

Request Parameters
email (string): User's email address.
password (string): User password.

### Verify Credentials

POST /verify

Check if the credentials provided are valid.

Request Parameters
email (string): User's email address.
password (string): User password.

### Update User Information

PUT /user/update/< id >

Updates information for an existing user.

Request Parameters
username (string, optional): New username.
email (string, optional): New email address.

### Change Password

PUT /user/editpw/< id >

Change the password of an existing user.

Request Parameters
password (string): New password for the user.

### Get All Users

GET /getusers

Gets a list of all users.

### Delete User

DELETE /user/delete/< id >

Delete a user from the database.
