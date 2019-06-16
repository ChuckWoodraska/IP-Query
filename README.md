# IP Query

# Set Up

Get necessary libs:

`pipenv install`

or 

`pip install -r requirements.txt`

Copy config.ini.example to config.ini and fill out the IP Stack Access Key.
Copy testconfig.ini.example to testconfig.ini and fill out the IP Stack Access Key.
You can get a free key here: https://ipstack.com/product

# Running the Program

Create database with all the data:

`flask create_db`

There is a sample database already filled out as this process can take about 5 mins.

Run webserver to interact with the data:

`flask run`

Once server is up and running go to a browser and open up 127.0.0.1:5000 to query and filter IP data.

Run tests by first changing into the tests directory and then running:

`pytest`

# See it in action!

This video can show you more: https://youtu.be/HrEI8OCw_gU

Live version: 

