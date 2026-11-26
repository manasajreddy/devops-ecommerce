

# Get the official Docker CLI
FROM docker:27-cli AS docker-cli

# Jenkins base image
FROM jenkins/jenkins:lts-jdk21

# Install Docker CLI into Jenkins
USER root

COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker

# Verify Docker CLI installation
RUN docker --version

# Return to Jenkins user
USER jenkins
