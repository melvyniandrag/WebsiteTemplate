# Deploy a Website with Professional Tools

This tutorial shows you how to make a simple website with a handful of libraries and software used by professionals. Here's a list of what we're using:

* Django
* Bootstrap 4 CSS
* sqlite3
* Docker
* Apache2
* Nginx

## setup
1. create a droplet
2. apt install git
3. fork the website tutorial repo https://github.com/melvyniandrag/WebsiteTemplate/tree/master#
4. clone your fork to your droplet. 
5. cd WebsiteTemplate
6. apt install -y python3-dev python3-pip  python3-django

## Run with the built in debug webserver

1. Test out the site :
```
 $cd WebsiteTemplate/main
 $ls
 # there should be a manage.py there.
 $python3 manage.py runserver 0.0.0.0:80
```
1. This will give an error in the browser, we need to set an environment variable
1. run this: $export website_secret_key="put whatever random text you want"
1. Run the server again on 0.0.0.0:80
1. Check again in your browser
1. Ta da!
1. kill the website (CTRL+C)


## Now let's run with a proper webserver: apache2

1. Now lets use a proper webserver: apache2
1. apt install -y apache2 libapache2-mod-wsgi-py3
1. Go to your ipaddress in your browser. You see the default apache page!
1. Now lets replace that default page with our real website...
1. cp -r main /var/www/main
1. cp my_website.conf /etc/apache2/sites-available
1. have a look at my_website.conf. There is some interesting stuff in there, but we won't discuss it.
1. chown -R www-data:www-data /var/www/main
1. cd /var/www/main
1. python3 manage.py collectstatic --noinput
1. a2enmod wsgi
1. a2dissite 000-default.conf
1. a2ensite my_website.conf
1. reload apache2 as instructed systemctl reload apache2 // note that didnt work...  do systemctl restart apache2
1. check your browser! Go to the ip address of your droplet. You may need to reload with CTRL+F5 in your browser, or however you clear the cache in the browser you use.
1. ERROR! we previously exported the environment variable with export website_secret_key="some stuff"...
and you can see the env var is set if you echo $website_secret_key....
So what happened? Have a look at /var/log/apache2/error.log and see if you can spot the error message...  it says SECRET_KEY is missing!
1. Open up /var/www/main/main/settings.py and you will see that SECRET_KEY comes from an environment var. We need to make this environment var visible to apache 2.
1. add the line export website_secret_key="something something" to the bottom of /etc/apache2/envvars and then restart apache2. You should see that the website now works! 

You may have noticed that the steps we just did are a tremendous pain in the butt. You have to copy files all over, change ownership, install stuff, and run a handful of commands. What a pain, really boring to do this over and over, and it's easy for you to screw it up. And for a real website, you would do much much much more that what we did above. Very time consuming and error prone.

If only there was a way to automate all this and just deploy your website with a couple of commands....

## Now lets run inside a docker container
*discuss docker with students*

### Install Docker
Go here:
https://docs.docker.com/engine/install/debian/#install-using-the-repository
and follow instructions in the install using the apt repository section. DO NOT follow the install from a package section.

After the install, be sure to do the Linux Post Install steps too.

*note the install takes a little while. Would be a great time to talk about Docker more while it completes*

The install instructions run a hello-world container. 

You can see the image and container created by running

docker image ls
and
docker container ls 


although contrainer wont show output you would need to run
docker container ls -a

because the container stops and exits right away.

This is a big deal, what you just did!! Nice work!! This is probably a total mystery, but it's super important. And you have taken your first step in understanding docker, congrats.

### After installing docker
First turn off apache2. We don't want to use that. If we leave apache2 on, it will handle the requests. We want to forward the requests on port 80 to the Docker container. The container should handle the website, not the system Apache2 that we've been using.


```
systemctl stop apache2
```

Go in your browser and verify that the website is not working.

Now lets build and run the docker container. Go back to where you cloned the repository. Probably /root.


```
cd /root/WebsiteTemplate
ls
# you should see a Dockerfile. We'll build it and run the image.
# do a docker image ls
# you won't see my_website
docker build -t my_website -f Dockerfile .
```
You will get a warning not to use ENV for sensitive data. This is a complex topic and we wont discuss it today - today we are here mainly to expose you to a bunch of interesting tools and the workflow for deploying websites.

The warning is saying not to put sensitive data there. And indeed, this is dangerous.   we put the website secret key there, and put it on github. If our github got hacked, the secret would be out and our site would get hacked. 

1 thing you could do is just be sure to change that secret key before deploying it, dont use the key you put on github. But there are many solutions, this is a complex software design question and will depend on how YOU like to program, or how your company likes to manage secrets.

```
# when this is done, do docker image ls. 
# you'll see your image is built!
# now lets start a container with this image!
docker container  ls 
# your container is NOT running. Let's turn it on.
docker run -d --name my_website -p 80:80 my_website
docker container ls
#you'll see your container is running!
```

Now checkout your website! Be sure to use http!!! Don't use https, we didn't set that up!!!

## Cleanup
Before moving on, let's clean up. Turn off and delete your docker containers
```
docker container ls -a
# for each name under NAMES run ( probably you only have my_website)
docker container kill my_website
docker container rm my_website
```


## NGINX reverse proxy
NGINX can be used as a webserver instead of apache2. Me personally, I usually use apache2 as my server and nginx as my reverse proxy. This is out of ignorance, because I learned the apache2 webserver, and I don't really write websites, so I never took time to learn another one. And then when I needed a reverse proxy, I learned nginx. And I never needed another reverse proxy, so I just use this one. If you think this is fun, then you are newer to this game than me, and I just taught you apache2 and nginx, and you can now go learn MORE and be better than.

What is a reverse proxy? Let's discuss it. *discuss* *draw on board*

We will run the website on port 6000 instead of 80. Website requests will reach your computer on port 80.Then nginx will forward the request on to port 6000.

Make sure the server name in my.nginx.conf says "server_name \_;"


Then we need to install nginx
```
sudo apt install nginx
```

And put the config file in sites-available. With apache2 , there is a command we used to symlink the apache conf file into sites-enabled... so far as I know there is no equivalent `a2ensite` command for nginx, so you need to manually symlink it with `ln -s`
```
cp my.nginx.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/my.nginx.conf /etc/nginx/sites-enabled/my.nginx.conf
```

Then delete the default nginx config
```
rm /etc/nginx/sites-enabled/default
```

and restart nginx
```
systemctl restart nginx
```

Then run the docker container on port 6000. We don't need to rebuild the container, because it's already built. You would only run `docker build` again if you changed your website of Dockerfile. 

Note that we run it now with -p6000:80. This forwards requests on port 6000 to port 80 of the container.

Server receives request on port 80.
Nginx forwards that to your container on port 6000
Docker forwards the data on port 6000 to port 80 inside the container.
Apache is running inside the container on port 80.
That's the gist of it.


```
docker run -d --name my_website -p 6000:80 my_website
```

You should be able to access the site now!!

## Why are we wasting time with the reverse proxy?
Is there time in class?
Have students
```
cd /root
cp -a WebsiteTemplate WebsiteTemplate2
```
Now, make changes in the html templates for websitetemplate2
Then build the docker image, but give it a different name like my_website_2

Then run that image with a different container name, but set the port to 7000:80

Then update the nginx config to point /site1 to port 6000
and /site2 to port 7000

restart nginx

Then if you go to http://ipaddress/site1/ you'll get site 1
and if you go to http://ipaddress/site2 you'll get site 2

That's how you run 2 websites on one server!!!!
COOL

## Docker compose TODO

## HTTPS TODO. Method # 1 NGINX Proxy Manager
Review these vids and make sure instructions still good
https://www.youtube.com/watch?v=P3imFC7GSr0
https://www.youtube.com/watch?v=jx6T6lqX-QM
docs
https://nginxproxymanager.com/

## HTTPS 2 Method #2 do it yourself
https://letsencrypt.org/getting-started/

## TODO Postgres
By this point, our website is using sqlite3
Show how we can set up docker compose with a postgres database and link the website to a postgres db. 
Lots of fun to be had, we can run the db on a separate server. Then we look deeper into mounting volumes. 
Fun demo where we see that if the container crashes, we lose all the data if we didnt mount a volume. 
In fact, it would be better to demo that with sqlite first, since it's easier. 

## PS we could have done all of this using a venv
but we wont do this to keep things dead simple. We are using the system python3 and installing dependencies
in the debian way like apt install python3-django. How you manage your python environment is a complex issue
as I've hinted at in this class. If you use a venv, you need to change the config files used in this demo.
I'll leave that as an exercise for you to figure out some time.

1. apt install -y python3.13-venv
6. python3 -m venv django-website-venv
7. ls
