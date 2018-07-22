
# Linux Server Configuration for Udacity Full Stack Nanodegree Project 6

For the last project in the nanodegree I created and instance of a Linux server (Ubuntu 16.04) on AWS with Lightsail. I made a series of configurations to secure the server with the UFW firewall, created a new user that I added to 'sudoers'. I enabled remote login with SSH and disabled login as the root user. I installed Apache, Python and mod_wsgi. I installed PostgreSQL, created a new postgres database, user, and gave the new user permissions on the database. I then cloned my Item Catalog Flask app from project 4 [https://github.com/yshiawallace/formific-item-catalog](https://github.com/yshiawallace/formific-item-catalog), installed a virtual environment, configured the virtual host and mod_wgsi, and made updates to my app files to make them compatible with the server environment.


## Web URL of app
http://35.182.146.216/

## Summary of configurations made to server

### Upgraded all packages on server (while logged in as non-root user)
	`sudo apt-get update`
	`sudo apt-get upgrade`

### Change SSH port from 22 to 2200
`sudo nano /etc/ssh/sshd_config`
* locate the line with 'Port 22' and change to 'Port 2200'
* Save and close file (on a Mac - Ctrl + O, return, Ctrl + X)
* restart the sshd servce with `sudo service sshd restart`

### Configure UFW firewall to deny all incoming connections except on port 2200 and http
	`sudo ufw default deny incoming`
	`sudo ufw default allow outgoing`
	`sudo ufw allow ssh`
	`sudo ufw allow 2200/tcp`
	`sudo ufw allow www`
* Check rules with: 
	`sudo ufw show added`
* NB: Make sure that ssh is allowed before you enable firewall or you will be blocked from your server!
	`sudo ufw enable`

### Open a new custom port (2200) on Amazon Lightsail Firewall

### Re-start server and login from port 2200
* Downloaded a key from Lightsail to use until I create my own ssh key pair. Login using this key and continue configurations.

### Created a new user: 'grader'
	`sudo adduser grader`
* follow the prompts and specify password

### Add new user to sudoers
	`sudo usermod -aG sudo grader`

### Switch to new user with:
	`su grader`
* (enter the password as prompted)

### Generate key pair and copy public key to server
* In a new terminal window (not logged into server) enter:
	`ssh-keygen`
* in the terminal window that is logged into server as user 'grader', in the root directory, enter:
	`mkdir .ssh`
	`touch .ssh/authorized_keys`
* read the key from my local computer with:
	`cat /Users/yshiawallace/.ssh/id_rsa.pub`
* Copy the contents of this file
* Edit the .ssh file on the server (logged in as grader):
	`sudo nano .ssh/authorized_keys`
* Paste the contents of the local key into this file.
* Save and close the `.ssh/authorized_keys` file on the server.
* Give grader access to the .ssh folder:
	`chmod 700 .ssh`
	`chmod 644 .ssh/authorized_keys`
* Now the grader can ssh into the server remotely with `ssh grader@35.182.146.216 -p 2200 -i ~/.ssh/id_rsa`	

### Disable remote login as root. Edit this file:
	`sudo nano /etc/ssh/sshd_config`
* change this line: `#PermitRootLogin yes` to `PermitRootLogin no`
* Save and close file
* Restart ssh 
	`sudo /etc/init.d/sshd restart`

### Sync timezone of server
* Find timezone
	`timedatectl list-timezones`
* use space bar to look for the timezone of the server. Mine is: America/New York
* set the timezone:
	`sudo timedatectl set-timezone America/New_York`
* verify changes with
	`date`

### Install NTP
	`sudo apt-get install ntp`

### Open firewall (UFW) to NTP on port 123
* Open a new custom port (123) on Amazon Lightsail Firewall. Select 'Custom	UDP	123'.
* Allow UFW to accept connections from port 123:
	`sudo ufw allow 123/udp`
* Verify your changes:
	`sudo ufw show added`

### Install and configure Apache
	`sudo apt-get update`
	`sudo apt-get install apache2`
* check status of the server:
	`sudo systemctl status apache2`


### Install Python 2 and mod-wsgi
* Ubuntu 16.0.4 comes with python installed. My catalog app runs on Python 2.7, so check which version is installed:
	`which python2`
* Install pip for python:
	`sudo apt-get install python-pip`
* Install mod_wsgi:
	`sudo apt-get install libapache2-mod-wsgi python-dev`
* Enable mod_wgsi:
	`a2enmod wsgi`

### Install PostgreSQL
	`sudo apt-get install postgresql postgresql-contrib`

### Create a new postgresql database `catalog` and grant permissions to `grader`
* Switch over to postgres user:
	`sudo -i -u postgres`
* Enter the psql command line:
	`psql`
* Create new user:
	`CREATE USER formific WITH PASSWORD 'formific';`
* Create a new database:
	`CREATE DATABASE formific WITH OWNER formific;`
* List all database:
	`\l`
* enter the database you just created:
	`\connect formific`
* View all tables in this database, there should be none yet:
	`\dt`
* Quit psql:
	`\q`
* Switch back to `grader` user:
	`exit`

### Clone catalog app to server
* `cd` into `/var/www` and create a new directory called 'formificApp':
	`sudo mkdir formificApp`
* `cd` into `formificApp` and 
* Grant `grader` ownership of the directory:
	`sudo chown -R grader:grader formificApp`
* Install git:
	`sudo apt-get install git`
* Git clone catalog app repo to the `/var/www/formificApp/formificApp` directory
	`sudo git clone https://github.com/yshiawallace/formific-item-catalog`
* Move app files to `/var/www/formificApp/formificApp` directory:
	`sudo mv -v /var/www/formificApp/formificApp/formific-item-catalog/vagrant/catalog/* /var/www/formificApp/formificApp`
* Delete old `formific-item-catalog` file from `/var/www/formificApp/formificApp/` recursively:
	`sudo rm -R formific-item-catalog`
* Re-name original catalog app controller file to `__init__.py`:
	`sudo mv formific.py __init__.py`
* Edit `__init__.py`:
	`sudo nano __init__.py`
* Change `app.run(host='0.0.0.0', port=8000)` to `app.run()`
* Save and close file.
* Edit `database.py` file:
	`sudo nano database.py`
* Change `engine = create_engine('sqlite:///formific.db', convert_unicode=True)` to `engine = create_engine('postgresql://formific:formific@localhost/formific)`
* make same edit to `starter_items.py`

### Install and set up a virtual environment with
	`pip install virtualenv`
	`virtualenv venv`
* Activate virtual environment:
	`source venv/bin/activate`

### Install Flask with:
	`pip install Flask`

### Install all app dependencies:
	`pip install sqlalchemy psycopg2 psycopg2-binary httplib2 requests oauth2client`	

### Test the app by running:
	`python __init__.py`
* You should see a message telling you the app is running ('Running on http://127.0.0.1:5000').
* Hit `^C` to exit the app.

### Configure and enable site:
	`sudo nano /etc/apache2/sites-available/formificApp.conf`
* add the following to this file:
```
<VirtualHost *:80>
    ServerName 35.182.146.216
    ServerAdmin admin@35.182.146.216
    WSGIDaemonProcess formificApp python-path=/var/www/formificApp/formificApp
    WSGIScriptAlias / /var/www/formificApp/flaskapp.wsgi process-group=formificApp application$
    <Directory /var/www/formificApp>
    <Files flaskapp.wsgi>
        Order allow,deny
        Allow from all
    </Files>
    </Directory>
    Alias /static /var/www/formificApp/formificApp/static
    <Directory /var/www/formificApp/formificApp/static/>
        Order allow,deny
        Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>
```
* Save and close the file.
* Enable the virtual host with the following command:
	`sudo a2ensite formificApp.conf`

### Create the .wsgi file:
	`cd /var/www/formificApp`
	`nano flaskapp.wsgi`
* Copy and paste the following into this file:
```
#!/usr/bin/python
activate_this = '/var/www/formificApp/formificApp/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/formificApp/")

from formificApp import app as application
application.secret_key = 'super_secret_key'
```
* Save and close the file.
* Restart apache:
	`sudo service apache2 reload`

### Go to URL and see if the app is running
[http://35.182.146.216/](http://35.182.146.216/)

If there is an error in the terminal window, start looking for what triggered the error. If not start by checking the apache error log:
	`sudo cat /var/log/apache2/error.log`

To see a feed of the most recent errors as they occur
	`sudo tail -f /var/log/apache2/error.log`

At this point in the configuration I ran into a series of errors and road blocks that took me days to solve. After much intense error log reading, googling, researching, sweating, I FINALLY manage to get the app running.

### Additional modifications needed to make to get my app running
1. I re-installed mod_wgsi because I thought it may have been compiled for the wrong version of Python.
* I uninstalled the existing mod_wgsi first
	`sudo apt-get purge --auto-remove libapache2-mod-wsgi`
* Then I used this resource [https://www.digitalocean.com/community/tutorials/installing-mod_wsgi-on-ubuntu-12-04](https://www.digitalocean.com/community/tutorials/installing-mod_wsgi-on-ubuntu-12-04)
```
mkdir ~/sources
cd ~/sources
wget https://codeload.github.com/GrahamDumpleton/mod_wsgi/tar.gz/4.6.4
tar xvfz 4.6.4
cd mod_wsgi-4.6.4
sudo apt-get install apache2-dev
./configure --with-python=/usr/bin/python2.7
make
sudo make install
```

2. I kept just seeing the Ubuntu default page when I went to my URL, so I found out that I had to disable the default site configuration:
```
sudo a2dissite 000-default.conf
sudo service apache2 reload
```

3. I thought there might be a permissions error, so I granted ownership of all files to the user `grader`
	`sudo chown -R grader:grader formificApp`

4. I had to update quite a few of my app files.
	* I had to update my template paths to use absolute paths instead of relative paths.
	* I had to fix cicular imports by moving all my models into one file in the main directory (the one that has my __ini__.py file in it), and removing my original module called `models`.
	* I had to add relationships to my `ArtItem`, `User` and `Medium` model classes that used the the `back_populates` specification.
	* I had to run `python starter_items.py` to populate my database before trying to run my site, or there were conflicts. When this happened, I had to drop all my tables, restart postgresql with `sudo service postgresql reload` and then restart apache `sudo service apache2 reload`.


## Resources consulted

https://stackoverflow.com/questions/46028907/how-do-i-connect-to-a-new-amazon-lightsail-instance-from-my-mac
https://discussions.udacity.com/t/cannot-connect-to-amazon-lightsail-ubuntu-after-reboot/344606
https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart
https://askubuntu.com/questions/7477/how-can-i-add-a-new-user-as-sudoer-using-the-command-line
https://askubuntu.com/questions/27559/how-do-i-disable-remote-ssh-login-as-root-from-a-server
https://www.digitalocean.com/community/tutorials/how-to-set-up-timezone-and-ntp-synchronization-on-ubuntu-14-04-quickstart
https://www.digitalocean.com/community/tutorials/additional-recommended-steps-for-new-ubuntu-14-04-servers#configure-timezones-and-network-time-protocol-synchronization
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04
https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-14-04
http://www.bogotobogo.com/python/Flask/Python_Flask_HelloWorld_App_with_Apache_WSGI_Ubuntu14.php
https://www.digitalocean.com/community/tutorials/how-to-create-remove-manage-tables-in-postgresql-on-a-cloud-server
http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/?highlight=wsgi
http://www.islandtechph.com/2017/10/21/how-to-deploy-a-flask-python-2-7-application-on-a-live-ubuntu-16-04-linux-server-running-apache2/
http://www.bogotobogo.com/python/Flask/Python_Flask_HelloWorld_App_with_Apache_WSGI_Ubuntu14.php
http://chrisstrelioff.ws/sandbox/2016/09/21/python_setup_on_ubuntu_16_04.html
https://discussions.udacity.com/t/how-do-i-insert-data-via-sqlalchemy-in-one-to-one-and-many-to-many-relationships/21294/2
http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-relationship

