
DIST=./dist
[ -d $DIST ] || (rm -Rf $DIST && mkdir -p $DIST)


tar -cvzf holin.src.tar.gz src/
tar -cvzf holin.pack holin.src.tar.gz holin_init.sh holin_nginx.conf holin.sh
mv holin.pack $DIST
sudo scp -i /Users/azl/Downloads/instrumera.pem $DIST/holin.pack ubuntu@instrumera.ru:/home/ubuntu/holin/
