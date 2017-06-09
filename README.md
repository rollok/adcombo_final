
```
http://code.activestate.com/recipes/576557-dump-postgresql-db-schema-to-text/
pgcli postgres://postgres:mysecretpassword@172.17.0.2:5432/postgres
pg_restore -U postgres -d postgres --host=172.17.0.2 --port=5432 -W dvdrental.tar
```


```
$ docker build -t pgcli .
To create a container from the image:

$ docker run --rm -ti pgcli pgcli <ARGS>
To access postgresql databases listening on localhost, make sure to run the docker in "host net mode". E.g. to access a database called "foo" on the postgresql server running on localhost:5432 (the standard port):

$ docker run --rm -ti --net host pgcli pgcli -h localhost foo
To connect to a locally running instance over a unix socket, bind the socket to the docker container:

$ docker run --rm -ti -v /var/run/postgres:/var/run/postgres pgcli pgcli foo
```
# adcombo_final
