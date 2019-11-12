# args 
ARG CENTOS_VERSION

# main
FROM centos:${CENTOS_VERSION}
LABEL AUTHOR=ashvedau

# install open-jdk
ARG JAVA_VERSION=11
RUN yum install -y java-${JAVA_VERSION}-openjdk
