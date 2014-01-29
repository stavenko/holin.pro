#!/bin/sh


QRS=/var/www/holin
RUN=$QRS/run;
HPWD=$(pwd)
[ -d $RUN ] || mkdir $RUN
[ -d $QRS ] || mkdir -p $QRS

chown www-data:www-data $RUN
chown www-data:www-data $QRS
chown www-data:www-data -R $QRS/holin/media

mysql -uroot  -e "create database if not exists holin character set =\"utf8\";"

cp holin_nginx.conf /etc/nginx/sites-enabled/
cd /etc/nginx/sites-enabled/
[ ! -f holin_nginx.conf ] || ln -s ../sites-available/holin_nginx.conf



cd $HPWD
ls -la
pwd
cp holin.sh /etc/init.d/

tar -xzf ./holin.src.tar.gz
cp -R ./src/* $QRS
cd $QRS
chmod +x ./manage.py 
./manage.py syncdb --noinput --settings="holin.settings"
./manage.py migrate --settings="holin.settings"
./manage.py collectstatic --noinput --settings="holin.settings"

chmod +x /etc/init.d/holin.sh
update-rc.d holin.sh defaults
/etc/init.d/holin.sh restart

/etc/init.d/nginx restart


cd $HPWD
rm -Rf ./src
rm ./holin.src.tar.gz