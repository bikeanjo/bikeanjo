# BikeAnjo

<img src=”https://drive.google.com/drive/u/0/folders/1GaCI_fZDvxBfJ5kMq-t70kSb-sbij1vn”>


## What is Bike Anjo?

It is a network of passionate cyclists that promotes, mobilizes and helps people getting started with cycling as a means of transportation in cities. We believe that cycling is a tool for social change and the more people ride, the better our cities will become!

In the platform you can get help to learn how to ride a bike and improve your cycling, route recommendations, commute together in traffic, tips and much more.

We analyze your request in our database and connect you to the nearest Bike Anjo volunteer to help you with your request.

bikeanjo.org


## Development environment

The *bikeanjo* platform uses PostgreSQL with PostGIS extension. Also, it uses
NPM and Bower to manage assets, so NodeJS is also needed to have a development
environment.

It is recommended to use Virtualenv and virtualenv wrapper to manage isolate and
Python2 dependencies.

The following README was written when setting up a development environment on
Manjaro Linux. But packages described here are probably available in any debian
based distribution also.

### System requirements

The command below install system requirements on Manjaro Linux. Packages may
have similar name on Debian and Ubuntu.

```sh
sudo pacman -S postgresql     \
    postgis                   \
    nodejs                    \
    python2-virtualenv        \
    python-virtualenvwrapper
```

The `virtualenvwrapper` is not activated right after installing, so it needs to
be activated manually after activation.

```sh
source /usr/bin/virtualenvwrapper.sh 
```


### Getting the code

Clone project and change current directory to it. 

```sh
git clone git@github.com:bikeanjo/bikeanjo.git
```

```
cd bikeanjo
```


### Setting up the database

1. If it is first time running on Manjaro, create data folder
```sh
sudo -u postgres initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'
```

2. Start database service
```sh
sudo systemctl start postgresql
```

3. Create user and schema using a shortcut
```sh
ACCIDENT=no make resetdb
```

It creates:

* An user named `bikeanjo` with password `bikeanjo`
* A database schema named `bikeanjo`


### Setting up the project


1. Create Python2 Virtualenv
```sh
mkvirtualenv bikeanjo -p /usr/bin/python2
```

2. Activate virtualenv if not activated
```sh
workon bikeanjo
```

3. Install Python requirements
```sh
pip install -r requirements.txt
```

4. Setup local variables
```sh
cat > .env <<'EOF'
DJANGO_DEBUG=True
DJANGO_DATABASE_URL=postgis://bikeanjo:bikeanjo@localhost/bikeanjo
EOF
```

5. Load database initial data
```sh
./manage.py migrate
./manage.py sync_translation_fields --noinput                # First time only!
```

6. Install assets compiling requirements
```sh
npm install
./node_modules/bower/bin/bower install
./node_modules/grunt-cli/bin/grunt all
```

7. Create a superuser
```sh
./manage.py shell_plus <<'EOF'
user = User.objects.create_user('admin', email='b@c.de', password='admin')
user.is_superuser=True
user.is_staff=True
user.role='bikeanjo'
user.country_id=1
user.city_id=13416
user.gender='male'
user.accepted_agreement=True
user.first_name='Bikeanjo'
user.last_name='Admin'
user.save()
EOF
```

8. Create a fake socialapp for django-allauth
```sh
./manage.py shell_plus <<'EOF'
app = SocialApp()
app.name='Facebook'
app.provider='facebook'
app.client_id='1234567890'
app.secret='1234567890'
app.save()
app.sites = Site.objects.all()
EOF
```



## Troubleshoot

### GEOSException: Could not parse version info string

Probably, libgeos was migrated to Git and Django 1.8.x used to detect libgeos
SVN revision by using a very strict regular expression. As upgrading Django just
to solve that problem may bring a lot of head aches, a little change on core
file is needed. The patch below does it.

1. Activate env
```sh
workon bikeanjo
```

2. Figure out where is site-packages
```sh
SITE_PACKAGES=$(python -c 'from distutils.sysconfig import get_python_lib; print(get_python_lib())')
```

3. Apply patch on django file
```sh
patch -d$SITE_PACKAGES -p0 <<'DIFF'
diff --git django/contrib/gis/geos/libgeos.py django/contrib/gis/geos/libgeos.py
@@ -130,7 +130,7 @@
 # '3.0.0rc4-CAPI-1.3.3', '3.0.0-CAPI-1.4.1', '3.4.0dev-CAPI-1.8.0' or '3.4.0dev-CAPI-1.8.0 r0'
 version_regex = re.compile(
     r'^(?P<version>(?P<major>\d+)\.(?P<minor>\d+)\.(?P<subminor>\d+))'
-    r'((rc(?P<release_candidate>\d+))|dev)?-CAPI-(?P<capi_version>\d+\.\d+\.\d+)( r\d+)?$'
+    r'((rc(?P<release_candidate>\d+))|dev)?-CAPI-(?P<capi_version>\d+\.\d+\.\d+)( \w+)?$'
 )
 
 
@@ -141,7 +141,7 @@
     is a release candidate (and what number release candidate), and the C API
     version.
     """
-    ver = geos_version().decode()
+    ver = geos_version().decode().strip()
     m = version_regex.match(ver)
     if not m:
         raise GEOSException('Could not parse version info string "%s"' % ver)

DIFF
```
