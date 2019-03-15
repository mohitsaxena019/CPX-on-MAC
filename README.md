# CPX-on-MAC
Citrix ADC on MAC - Advanced  use cases and easy to test environment 
# Prerequisite
Getting started first time with Docker containers on MAC you need to install Mac for Docker on your MAC machine. Get the stable download version of MAC for docker by clicking below link
  * https://download.docker.com/mac/stable/Docker.dmg
>For latest information and documentation on MAC for docker please visit
  * https://docs.docker.com/v17.12/docker-for-mac/install/#download-docker-for-mac
# System Requirements: 
Docker for Mac launches only if all of these requirements are met.
* Mac hardware must be a 2010 or newer model,
* You can check to see if your machine has virtualization support : sysctl kern.hv_support
* macOS El Capitan 10.11 and newer macOS releases are supported.
* At least 4GB of RAM
# Install and run Docker for Mac
* Double-click Docker.dmg to open the installer, then drag Moby the whale to the Applications folder.
* Double-click Docker.app in the Applications folder to start Docker. (In the example below, the Applications folder is in “grid” view mode.)
* Login with your docker id, if you done have docker id please create one on below link
  * https://hub.docker.com/signup
# Verify your Docker installation
* Open the terminal of your choice.
* Type docker login.
* Enter your username and password created on docker hub.
* Run the below command to run your first container
  * docker run hello-world
# Domain Names for Demo
Write the following config in /etc/hosts file to run all the demo examples from local browser.
 * 127.0.0.1       www.hotdrink.com
 * 127.0.0.1       www.colddrink.com
# Demo Port Requirement
For this demo setup it will be using port
* 80 (To access the test domain on http)
* 443 (To access the test domain on SSL)
* 4443 (To access the test domain on SSL with clientauth enabled)
* 9080 (To Configure CPX via nitro api’s on http)
* 9443 (To configure CPX via nitro api’s on https)
>If any of these ports are not available then test environment will fail to start, in such cases please update docker-compose file with some other free ports.

# Deploying test environment
Chekout the code from github using below link
* git clone https://github.com/mohitsaxena019/CPX-on-MAC.git
>Once the code is downloaded, Navigate to CPX-on-MAC/cpx-demo folder. And use below command to start and stop the test environment. Before starting the test environment please make sure to update the /etc/hosts file with above mentioned domain names.

# Starting with Citrix ADC CPX
