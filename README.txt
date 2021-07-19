Sort Web App Notes

///////////////////////////////////////////////////////////////////////////////////////////////////
Server Configuration Notes:

Set up was done by following this guid
    https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

To Restart webapp execute
    sudo systemctl restart sort-webapp
    
    sort-webapp is the name of the service

    there is a cron job that deletes all csv file in the downloads folder at midnight each night
        this cron job can be updated by executing "crontab -e" this is a root user crontab file

///////////////////////////////////////////////////////////////////////////////////////////////////
Flask App Setup

__init__.py
    creates flask app and start the process, this is where you designate what config to use
        Config options are in config.py file

.env 
    parameters for the environment, contains Secret Key, database location, and runs wsgi.py

wsgi.py
    launches flask app
