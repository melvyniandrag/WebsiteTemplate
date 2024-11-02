FROM debian:bookworm

ENV website_secret_key=thisisasecretkeymakesuretochangeitbeforeproduction0987809qlkjn5

RUN apt -y update

RUN apt -y upgrade

RUN apt -y install python3-dev python3-pip apache2 libapache2-mod-wsgi-py3

RUN apt -y install python3-django

COPY my_website.conf /etc/apache2/sites-available

COPY main /var/www/main

WORKDIR /var/www

RUN chown -R www-data:www-data main

WORKDIR /var/www/main

RUN python3 manage.py collectstatic --noinput

RUN a2enmod wsgi

RUN a2dissite 000-default.conf

RUN a2ensite my_website.conf

EXPOSE 80

CMD ["apachectl", "-D", "FOREGROUND"]
