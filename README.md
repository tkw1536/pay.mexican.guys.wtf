# pay.mexican.guys.wtf
## What?

A dockerizable site for keeping track of who has to pay the mexicans.

## Why?

Too lazy to commit and push by hand every time.

## How?

```bash
docker build . -t pay_mexican_guys
docker run --name=mexicans -e 'DJANGO_ALLOWED_HOSTS=*' -e 'DJANGO_SECRET_KEY=supersecret' -v data:/data/ -p 8080:8080 pay_mexican_guys
docker exec -ti mexicans python manage.py createsuperuser
```

If you encounter a permissions error, ensure that the `www-data:www-data` user (with `uid/gid 82/82`) has permissions to write the volume.

Afterwards visit `http://localhost:8080/admin` to login.
Everything should be self-explanatory.
