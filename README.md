# CST 8919 Lab 1: Implementing User Login with Flask and Auth0

This lab shows how to have a starter version of using Flask and Auth0 modules when developing a program for secure authentication.

# Running the App

To run the program, first you need to have `python3` and `pip` installed in order to install the modules needed for this program.

Then you need to go into the directory of you program and write:

```bash
.\.venv\Scripts\activate
pip install -r .\requirements.txt
```

in the command line in order to install all the modules in the requirement.txt file which are flask to have different endpoint and Auth0 to have secure authitcation.

After that, run 

```bash
openssl rand -hex 32
```
and copy the string from the command terminal and pase it in the `APP_SECRET_KEY` enviroment variable in the .env file.

In order to run the program bt writing this in the command line:

```bash
python server.py
```

Then you will se this in the command terminal 

```bash
 * Serving Flask app 'server'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:3000
 * Running on http://192.168.0.248:3000
```

Open: `http://localhost:3000` to open the webpage of the program you are running.

# Link to to the video on how the program works and documenation on the code

[Video link](https://www.youtube.com/watch?v=3reTzkSjqlU)