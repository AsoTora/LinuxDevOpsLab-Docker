FROM centos:7
LABEL AUTHOR=ashvedau

# install httpd
RUN yum install -y httpd web-assets-httpd
COPY index.html /var/www/html/

# run httpd
EXPOSE 80
ENTRYPOINT ["httpd"]
CMD ["-DFOREGROUND"]
