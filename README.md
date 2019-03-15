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
This demo uses following ports
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
>>Deploy the demo
* docker-compose up -d
>>Destroy the demo
* docker-compose down
>>To Access the CPX once deployment is up 
* docker exec -it cpx-demo_cpx_1 bash
>>To access CPX CLI once you login to cpx 
* cli_script.sh "show ver"
>>For NITRO API access to CPX
* http://localhost:9080/nitro/v1/config/lbvserver
>>For NITRO API access over HTTPS 
* https://localhost:9443/nitro/v1/config/lbvserver
>>For more information on configuring Citrix ADC
* https://docs.citrix.com/en-us/citrix-adc-cpx/12-1/configure-cpx.html
# Understanding Demo use cases
# Usecase 1: Basic content switching: switch based on domain. Use servicegroups and HTTP monitors.
>Topology file: citrix-walmart topology.pptx
>Relevant configs relating to below procedures are present within cpx.conf file
* Create servicegroups listening on services from hotdrink and coldrink app on port 80
* Create content switching CS vserver listening on HTTP
* Create two dummy lb vservers 
* Create appropriate CS vserver policy and attach the dummy lb vservers
* Add http monitors to lb vserver
* Send a browser request to www.hotdrink.com and www.colddrink.com
# Usecase 2: SSL OFFLOAD:
>Topology file:citrix-walmart topology.pptx
>Relevant configs relating to below procedures are present within cpx.conf file
>Relevant certs are present within certs folder
* Create servicegroups listening on services from hotdrink and colddrink app on port 80
* Create content switching CS Vserver listening on port 443 (SSL)
* Create two dummy lb vservers
* Attach the relevant certs to the vservers
* Create appropriate CS vserver policy and attach the dummy lb vservers
* Send a https browser request to www.hotdrink.com and www.colddrink.com
#Usecase 3: SSL BACKEND:
>Topology file:citrix-walmart topology.pptx
>Relevant configs relating to below procedures are present within cpx.conf file
>Relevant certs are present within certs folder
* Create servicegroups listening on services from hotdrink and colddrink app on port 443
* Create content switching CS Vserver listening on port 443 (SSL)
* Create two dummy lb vservers
* Attach the relevant certs to the vserver
* Create appropriate CS VServer policy and attach the dummy lb vservers
* Send a https browser request to www.hotdrink.com and www.colddrink.com
* Add new CS and LB vserver for enabling clientauth and serverauth
* Attach the relevant LB vservers with CS vserver for enabling clientauth and serverauth
* Send a https request to www.hotdrink.com and www.colddrink.com

