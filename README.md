# Bike Anjo


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

```
sudo pacman -S postgresql     \
    postgis                   \
    nodejs                    \
    python2-virtualenv        \
    python-virtualenvwrapper
```

The `virtualenvwrapper` is not activated right after installing, so it needs to
be activated manually after activation.

```
source /usr/bin/virtualenvwrapper.sh 
```


### Getting the code

Clone project and change current directory to it. 

```
git clone git@github.com:bikeanjo/bikeanjo.git
```

```
cd bikeanjo
```


### Setting up the database

1. If it is first time running on Manjaro, create data folder
```
sudo -u postgres initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'
```

2. Start database service
```
sudo systemctl start postgresql
```

3. Create user and schema using a shortcut
```
ACCIDENT=no make resetdb
```

It creates:

* An user named `bikeanjo` with password `bikeanjo`
* A database schema named `bikeanjo`


### Setting up the project


1. Create Python2 Virtualenv
```
mkvirtualenv bikeanjo -p /usr/bin/python2
```

2. Activate virtualenv if not activated
```
workon bikeanjo
```

3. Install Python requirements
```
pip install -r requirements.txt
```

4. Setup local variables
```
cat > .env <<'EOF'
DJANGO_DEBUG=True
DJANGO_DATABASE_URL=postgis://bikeanjo:bikeanjo@localhost/bikeanjo
EOF
```

5. Load database initial data
```
./manage.py migrate
./manage.py sync_translation_fields --noinput                # First time only!
```

6. Install assets compiling requirements
```
npm install
./node_modules/bower/bin/bower install
./node_modules/grunt-cli/bin/grunt all
```

7. Create a superuser
```
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
```
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

```
workon bikeanjo
SITE_PACKAGES=$(python -c 'from distutils.sysconfig import get_python_lib; print(get_python_lib())')
patch -d$SITE_PACKAGES -p0 <<'DIFF'
diff --git django/contrib/gis/geos/libgeos.py django/contrib/gis/geos/libgeos.py
index 66c61f3..5040bc5 100644
--- django/contrib/gis/geos/libgeos.py
+++ django/contrib/gis/geos/libgeos.py
@@ -130,7 +130,7 @@ geos_version.restype = c_char_p
 # '3.0.0rc4-CAPI-1.3.3', '3.0.0-CAPI-1.4.1', '3.4.0dev-CAPI-1.8.0' or '3.4.0dev-CAPI-1.8.0 r0'
 version_regex = re.compile(
     r'^(?P<version>(?P<major>\d+)\.(?P<minor>\d+)\.(?P<subminor>\d+))'
-    r'((rc(?P<release_candidate>\d+))|dev)?-CAPI-(?P<capi_version>\d+\.\d+\.\d+)( r\d+)?$'
+    r'((rc(?P<release_candidate>\d+))|dev)?-CAPI-(?P<capi_version>\d+\.\d+\.\d+)( \w+)?$'
 )
DIFF
```
