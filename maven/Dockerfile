# first build stage
FROM maven:3.6-jdk-8-alpine as builder
WORKDIR /app
COPY pom.xml .
RUN mvn -e -B dependency:resolve
COPY src ./src
RUN mvn -e -B package
CMD ["java", "-jar", "target/jb-hello-world-maven-0.1.0.jar"]

# second stage
FROM openjdk:8-jre-alpine
COPY --from=builder /app/target/jb-hello-world-maven-0.1.0.jar /tmp
CMD ["java", "-jar", "tmp/jb-hello-world-maven-0.1.0.jar"]
