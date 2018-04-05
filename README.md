# flask-webcrawler
Simple webcrawler with web interface in Flask for [yell.ru](http://yell.ru)

## Step by step instruction

Update your local package index and then install the packages by typing:
```
sudo apt-get update
sudo apt-get install python-pip python-dev nginx redis-server
```

Create a Python Virtual Environment:

[virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html)- full manual

Install virtual environment with python3 support:
```
MacOS: mkvirtualenv --python=/usr/local/bin/python3 viz_parser
Linux: mkvirtualenv --python=/usr/bin/python3 viz_parser 
```
Activate your virtualenv:
```
workon viz_parser
```
Install all requirements into your virtualenv:
```
pip install -r requirements.txt
pip install uwsgi
```
cd to directory app/settings/:
```
    mv config_local.py_sample config_local.py
```
And then modify this config file for your custom settings, for example, you must set mail settings.

Create config files for project.
Change config section of fabfile.py for your local settings: 
```
CONFIG['host'] - set ip address of your server.
CONFIG['port'] - set server's port for ssh access.
CONFIG['username'] - set username login with required access for server.
CONFIG['project_dir'] - will be auto-generate, but you can set it manual.
CONFIG['virtualenv_dir'] - path of your virtualenv project, 
if your project's virtualenv located not in ~/.virtualenvs/viz_parser, you must set it by manual.
CONFIG['pid'], CONFIG['socket'] - path of your socket and pid files, 
if you want to locate this files in another place, you can do it in this sections.

```
Create all required configs from console:
```
    fab generate_configs    
```
This command included four other commands:
```
    generate_config_nginx - generate config for nginx
    generate_config_uwsgi - generate config for uwsgi
    generate_config_systemd_uwsgi - generate config for uwsgi as systemd service
    generate_config_systemd_rq - generate config for rq as systemd service
```
If it need, you can run this commands separately.

Also you need configure nginx:
```
sudo cp conf/viz_parser.conf /etc/nginx/sites-available/viz_parser.conf
sudo ln -s /etc/nginx/sites-available/viz_parser.conf /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

```

You must type only category of site, not subcategory in url form's field.
For example, [http://www.yell.ru/spb/top/restorany-i-kafe/](http://www.yell.ru/spb/top/restorany-i-kafe/)

Run all tests:
```
python -m unittest discover tests/
``` 

Run tests separately:
```
python -m unittest tests/test_scrapy.py
python -m unittest tests/test_yell.py
``` 
The work of the program is focused on a specific structure of the source site. If there are significant changes in the layout of the source site, the program will need to be adapted. You can check the site for changing the html structure by using the appropriate test(tests/test_yell.py).