# Use an official linux distro as a parent image
FROM ubuntu

# Set the working directory to /workspace
WORKDIR /workspace

# Copy the current directory contents into the container at /workspace
ADD /workspace /workspace

RUN cd /workspace

# Install required packages
RUN apt -qq update
RUN apt -qq -y install curl
RUN apt -qq -y install git
RUN apt -qq -y install python
RUN apt -qq -y install software-properties-common python-software-properties
RUN add-apt-repository ppa:openjdk-r/ppa -y
RUN apt -qq update
RUN apt -qq -y install openjdk-8-jdk

# Clone smartweb
RUN git clone https://gitlab.com/lizarralde.ignacio/isistan-smartweb.git

#Install project dependencies
RUN ./install_dependencies.sh