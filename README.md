# Template for a website

This template uses
* Django
* Bootstrap 4 CSS
* sqlite3
* Docker
* Apache2
* Nginx

## Deploy instructions
* Get a server and install Docker Engine ( formerly Docker CE )
```
sudo apt install nginx
```
* build the docker container
* run the docker container




### Docker instructions

```
docker build -t my_website -f Dockerfile .
docker run --name my_website -p 80:80 my_website
```

### Important Note
Be sure to do this
```
chmod -R www-data:www-data /var/www/main
```

