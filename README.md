# CPX-on-MAC
Citrix ADC on MAC - Advanced  use cases and easy to test environment 
# Prerequisite
Getting started first time with Docker containers on MAC you need to install Mac for Docker on your MAC machine. Get the stable download version of MAC for docker by clicking below link
  * https://download.docker.com/mac/stable/Docker.dmg
>For latest information and documentation on MAC for docker please visit
  * https://docs.docker.com/v17.12/docker-for-mac/install/#download-docker-for-mac
# System Requirements 
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
# Install Git
* To browse the code of this sample demo you need to install git on your mac machine.
 * Open Terminal of your choice
 * Type git --version on shell
 * This will automatically prompt you to git installer
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
* docker exec -it cpxdemo_cpx_1 bash
>>To access CPX CLI once you login to cpx 
* cli_script.sh "show ver"
>>For NITRO API access to CPX
* http://localhost:9080/nitro/v1/config/lbvserver
>>For NITRO API access over HTTPS 
* https://localhost:9443/nitro/v1/config/lbvserver
>>For more information on configuring Citrix ADC
* https://docs.citrix.com/en-us/citrix-adc-cpx/12-1/configure-cpx.html
# Understanding Demo use cases
>All the configuration related to Demo use cases are applied on the CPX when 'docker-compose up -d' is executed
## Usecase 1: Basic content switching: switch based on domain. Use servicegroups and HTTP monitors.


<img width="1278" alt="Screenshot 2019-03-15 at 10 31 43 PM" src="https://user-images.githubusercontent.com/43468858/54449487-3c013000-4774-11e9-8188-9283ccc32107.png">


>Relevant configs relating to below procedures are present within cpx.conf file
* Create servicegroups listening on services from hotdrink and coldrink app on port 80
* Create content switching CS vserver listening on HTTP
* Create two dummy lb vservers 
* Create appropriate CS vserver policy and attach the dummy lb vservers
* Add http monitors to servicegroup
* Send a browser request to www.hotdrink.com and www.colddrink.com

```
Relevant configuration:
##NetScaler feature to be enabled for these use cases
enable feature lb cs

#HTTP Backend Service for HotDrink app running two instance
add serviceGroup sg_hotdrink_http HTTP
bind serviceGroup sg_hotdrink_http 172.100.100.3 80
bind serviceGroup sg_hotdrink_http 172.100.100.4 80
add lb vserver lbvs_hotdrink_http HTTP 0.0.0.0 0
bind lb vserver lbvs_hotdrink_http sg_hotdrink_http

#HTTP Backend Service for ColdDrink app running two instance
add serviceGroup sg_colddrink_http HTTP
bind serviceGroup sg_colddrink_http 172.100.100.5 80
bind serviceGroup sg_colddrink_http 172.100.100.6 80
add lb vserver lbvs_colddrink_http HTTP 0.0.0.0 0
bind lb vserver lbvs_colddrink_http sg_colddrink_http
#Add HTTP monitor
add lb monitor monitorhttp HTTP -respCode 200 -httpRequest "GET /"
bind servicegroup sg_hotdrink_http -monitorName monitorhttp
bind servicegroup sg_colddrink_http -monitorName monitorhttp

#Add CS policy and action
add cs action csa_hotdrink -targetLBVserver lbvs_hotdrink_http
add cs action csa_colddrink -targetLBVserver lbvs_colddrink_http
add cs policy csp_hotdrink -rule "HTTP.REQ.HOSTNAME.SERVER.EQ(\"www.hotdrink.com\")" -action csa_hotdrink
add cs policy csp_colddrink -rule "HTTP.REQ.HOSTNAME.SERVER.EQ(\"www.colddrink.com\")" -action csa_colddrink 

#Add HTTP cs vserver for hotdrink and cold drink domain to content switch
add cs vserver csv_drinks_http HTTP 127.0.0.1 80
bind cs vserver csv_drinks_http -policyName csp_hotdrink -priority 20001
bind cs vserver csv_drinks_http -policyName csp_colddrink -priority 20002

```
## Usecase 2: SSL OFFLOAD:


<img width="1272" alt="Screenshot 2019-03-15 at 10 35 02 PM" src="https://user-images.githubusercontent.com/43468858/54448953-ff810480-4772-11e9-83af-2f28520a3715.png">


>Relevant configs relating to below procedures are present within cpx.conf file. 
>Relevant certs are present within certs folder
* Create servicegroups listening on services from hotdrink and colddrink app on port 80
* Create content switching CS Vserver listening on port 443 (SSL)
* Create two dummy lb vservers
* Attach the relevant certs to the vservers
* Create appropriate CS vserver policy and attach the dummy lb vservers
* Send a https browser request to www.hotdrink.com and www.colddrink.com

```
Relevant Configuration:

##NetScaler feature to be enabled for these use cases
enable feature lb cs

#HTTP Backend Service for HotDrink app running two instance
add serviceGroup sg_hotdrink_http HTTP
bind serviceGroup sg_hotdrink_http 172.100.100.3 80
bind serviceGroup sg_hotdrink_http 172.100.100.4 80
add lb vserver lbvs_hotdrink_http HTTP 0.0.0.0 0
bind lb vserver lbvs_hotdrink_http sg_hotdrink_http

#HTTP Backend Service for ColdDrink app running two instance
add serviceGroup sg_colddrink_http HTTP
bind serviceGroup sg_colddrink_http 172.100.100.5 80
bind serviceGroup sg_colddrink_http 172.100.100.6 80
add lb vserver lbvs_colddrink_http HTTP 0.0.0.0 0
bind lb vserver lbvs_colddrink_http sg_colddrink_http

#Add CS policy and action
add cs action csa_hotdrink -targetLBVserver lbvs_hotdrink_http
add cs action csa_colddrink -targetLBVserver lbvs_colddrink_http
add cs policy csp_hotdrink -rule "HTTP.REQ.HOSTNAME.SERVER.EQ(\"www.hotdrink.com\")" -action csa_hotdrink
add cs policy csp_colddrink -rule "HTTP.REQ.HOSTNAME.SERVER.EQ(\"www.colddrink.com\")" -action csa_colddrink 


#Shell Commands
cp -r /etc/ssl /tmp/

#NetScaler Commands
#Add SSL certs
add ssl certKey cert_drink -cert "/tmp/ssl/wild-hotdrink.com-cert.pem" -key "/tmp/ssl/wild-hotdrink.com-key.pem"
add ssl certkey colddrink_cert  -cert "/tmp/ssl/wild-colddrink.com-cert.pem" -key "/tmp/ssl/wild-colddrink.com-key.pem"
add ssl certkey cacert -cert "/tmp/ssl/wild-rootcert.pem"

#ADD SSL cs vserver for hotdrink and cold drink domain to content switch with SSL offload
add cs vserver csv_drinks_ssl SSL 127.0.0.1 443
bind cs vserver csv_drinks_ssl -policyName csp_hotdrink -priority 20001
bind cs vserver csv_drinks_ssl -policyName csp_colddrink -priority 20002
bind ssl vserver csv_drinks_ssl -certkeyName cert_drink

```

## Usecase 3: SSL BACKEND:


<img width="1262" alt="Screenshot 2019-03-15 at 10 38 45 PM" src="https://user-images.githubusercontent.com/43468858/54449014-1f182d00-4773-11e9-9df3-eae30315b56f.png">

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
* Send a https request to www.hotdrink.com:4443 and www.colddrink.com:4443

```
Relevant Configuration:

##NetScaler feature to be enabled for these use cases
enable feature lb cs

#SSL Backend Service for HotDrink app running two instance
add serviceGroup sg_hotdrink_ssl SSL
bind serviceGroup sg_hotdrink_ssl 172.100.100.3 443
bind serviceGroup sg_hotdrink_ssl 172.100.100.4 443
add lb vserver lbvs_hotdrink_ssl HTTP 0.0.0.0 0
bind lb vserver lbvs_hotdrink_ssl sg_hotdrink_ssl

#SSL Backend Service for HotDrink app running two instance
add serviceGroup sg_colddrink_ssl SSL
bind serviceGroup sg_colddrink_ssl 172.100.100.5 443
bind serviceGroup sg_colddrink_ssl 172.100.100.6 443
add lb vserver lbvs_colddrink_ssl HTTP 0.0.0.0 0
bind lb vserver lbvs_colddrink_ssl sg_colddrink_ssl

#Shell Commands
cp -r /etc/ssl /tmp/

#NetScaler Commands
#Add SSL certs
add ssl certKey cert_drink -cert "/tmp/ssl/wild-hotdrink.com-cert.pem" -key "/tmp/ssl/wild-hotdrink.com-key.pem"
add ssl certkey colddrink_cert  -cert "/tmp/ssl/wild-colddrink.com-cert.pem" -key "/tmp/ssl/wild-colddrink.com-key.pem"
add ssl certkey cacert -cert "/tmp/ssl/wild-rootcert.pem"

#SSL Backend Service for HotDrink app running two instance with clientauth enabled
add serviceGroup sg_hotdrink_ssl_clientauth SSL
bind serviceGroup sg_hotdrink_ssl_clientauth 172.100.100.3 443
bind serviceGroup sg_hotdrink_ssl_clientauth 172.100.100.4 443
add lb vserver lbvs_hotdrink_ssl_clientauth HTTP 0.0.0.0 0
bind lb vserver lbvs_hotdrink_ssl_clientauth sg_hotdrink_ssl_clientauth
bind ssl servicegroup sg_hotdrink_ssl_clientauth -certkey cacert -CA
bind ssl servicegroup sg_hotdrink_ssl_clientauth -certkey cert_drink  
set ssl servicegroup sg_hotdrink_ssl_clientauth -serverauth enabled

#SSL Backend Service for coldDrink app running two instance with clientauth enabled
add serviceGroup sg_colddrink_ssl_clientauth SSL
bind serviceGroup sg_colddrink_ssl_clientauth 172.100.100.3 443
bind serviceGroup sg_colddrink_ssl_clientauth 172.100.100.4 443
add lb vserver lbvs_colddrink_ssl_clientauth HTTP 0.0.0.0 0
bind lb vserver lbvs_colddrink_ssl_clientauth sg_colddrink_ssl_clientauth
bind ssl servicegroup sg_colddrink_ssl_clientauth -certkey cacert -CA
bind ssl servicegroup sg_colddrink_ssl_clientauth -certkey colddrink_cert  
set ssl servicegroup sg_colddrink_ssl_clientauth -serverauth enabled

#SSL cs vserver with clientauth enabled
add cs vserver csvs_hotdrink_ssl_clientauth SSL 127.0.0.1 4443
add cs action csa_hotdrink_clientauth -targetLBVserver lbvs_hotdrink_ssl_clientauth
add cs action csa_colddrink_clientauth -targetLBVserver lbvs_colddrink_ssl_clientauth
add cs policy csp_hotdrink_clientauth -rule "HTTP.REQ.HOSTNAME.SERVER.EQ(\"www.hotdrink.com\")" -action csa_hotdrink_clientauth
add cs policy csp_colddrink_clientauth -rule "HTTP.REQ.HOSTNAME.SERVER.EQ(\"www.colddrink.com\")" -action csa_colddrink_clientauth
set ssl vserver csvs_hotdrink_ssl_clientauth -clientauth enabled
bind ssl vserver csvs_hotdrink_ssl_clientauth -certkey cacert -CA
bind ssl vserver csvs_hotdrink_ssl_clientautH -certkeyName cert_drink

```
## Debugging CPX using command line
CPX login
```
docker exec -it <cpx docker name or container ID> bash
```
Verify CS vserver
```
root@590b90a51752:/# cli_script.sh 'show cs vserver'
exec: show cs vserver
1)	csv_drinks_http (127.0.0.1:80) - HTTP	Type: CONTENT 
	State: UP
	Last state change was at Fri Mar 15 16:53:04 2019
	Time since last state change: 0 days, 00:45:38.470  ARP:DISABLED
	Client Idle Timeout: 180 sec
	Down state flush: ENABLED
	Disable Primary Vserver On Down : DISABLED
	Appflow logging: ENABLED
	Port Rewrite : DISABLED
	State Update: DISABLED
	Default: 	Content Precedence: RULE
	Vserver IP and Port insertion: OFF 
	L2Conn: OFF	Case Sensitivity: ON
	Authentication: OFF
	401 Based Authentication: OFF
	Push: DISABLED	Push VServer: 
	Push Label Rule: none
	Listen Policy: NONE
	IcmpResponse: PASSIVE
	RHIstate:  PASSIVE
	Traffic Domain: 0

```
Verify lb vserver
```
root@590b90a51752:/# cli_script.sh 'show lb vserver' | grep Type
1)	lbvs_hotdrink_http (0.0.0.0:0) - HTTP	Type: ADDRESS 
2)	lbvs_colddrink_http (0.0.0.0:0) - HTTP	Type: ADDRESS 
3)	lbvs_hotdrink_ssl (0.0.0.0:0) - HTTP	Type: ADDRESS 
4)	lbvs_colddrink_ssl (0.0.0.0:0) - HTTP	Type: ADDRESS 
5)	lbvs_hotdrink_ssl_clientauth (0.0.0.0:0) - HTTP	Type: ADDRESS 
6)	lbvs_colddrink_ssl_clientauth (0.0.0.0:0) - HTTP	Type: ADDRESS 

```

Verify running configuration

```
root@590b90a51752:/# cli_script.sh 'show run'                   
exec: show run
#NS12.1 Build 51.16
# Last modified Fri Mar 15 16:53:02 2019
set ns config -IPAddress 172.100.100.254 -netmask 255.255.255.0
set ns config -tagged NO
enable ns feature LB CS SSL AAA
enable ns mode L3 USNIP PMTUD

OUTPUT TRIMMED
.......
```


# Example of applying a responder policy through command line on CPX
## Denying access to www.hotdrink.com using responder policy

Enable responder rewrite feature
```
root@590b90a51752:/# cli_script.sh 'enable feature responder rewrite'
exec: enable feature responder rewrite
Done
```
Add a responder action to respond with a certain http header when a http request arrives to CPX
```
root@590b90a51752:/# cli_script.sh 'add responder action respond_custom_content respondwith "\"HTTP/1.1 200 OK\r\nAccept-Encoding: text\r\nServer: Test-Server\r\n\r\n\""'
exec: add responder action respond_custom_content respondwith "\"HTTP/1.1 200 OK\r\nAccept-Encoding: text\r\nServer: Test-Server\r\n\r\n\""
```
Add a responder policy with the above action if url contains /
```
root@590b90a51752:/# cli_script.sh 'add responder policy respond_custom_content_policy "http.req.url.contains(\"/\")" respond_custom_content'
exec: add responder policy respond_custom_content_policy "http.req.url.contains(\"/\")" respond_custom_content
Done
```

Check the applied responder config
```
root@590b90a51752:/# cli_script.sh 'show run' | grep responder
add responder action respond_custom_content respondwith "\"HTTP/1.1 200 OK\r\nAccept-Encoding: text\r\nServer: Test-Server\r\n\r\n\""
add responder policy respond_custom_content_policy "http.req.url.contains(\"/\")" respond_custom_content
```
Apply the policy to hotdrink lb vserver

```
root@590b90a51752:/# cli_script.sh 'bind lb vserver lbvs_hotdrink_http -policyname respond_custom_content_policy -priority 1000' 
exec: bind lb vserver lbvs_hotdrink_http -policyname respond_custom_content_policy -priority 1000
Done
```

Check the browser by accessing www.hotdrink.com

A browser query would show a blank page

```
root@slave40:~/MohitCPX/CPX-on-MAC/cpx-demo# curl -vvv  http://www.hotdrink.com
* Rebuilt URL to: http://www.hotdrink.com
*   Trying 127.0.0.1...
* Connected to www.hotdrink.com (127.0.0.1) port 1080 (#0)
> GET / HTTP/1.1
> Host: www.hotdrink.com:1080
> User-Agent: curl/7.47.0
> Accept: */*
> 
< HTTP/1.1 200 OK =========> Response from responder policy
< Accept-Encoding: text =========> Response from responder policy
< Server: Test-Server=========> Response from responder policy
* no chunk, no close, no size. Assume close to signal end
< 
* Closing connection 0
```

Unbind the responder policy to allow access to www.hotdrink.com
```
root@590b90a51752:/# cli_script.sh 'unbind lb vserver lbvs_hotdrink_http -policyname respond_custom_content_policy'
exec: unbind lb vserver lbvs_hotdrink_http -policyname respond_custom_content_policy
Done
```

Access www.hotdrink.com to view the webpage

## Similarly try adding rewrite policies to CPX. Please check the documentation within the following links for adding rewrite and responder policies

[CPX Rewrite Policy](https://developer-docs.citrix.com/projects/netscaler-command-reference/en/12.0/rewrite/rewrite-policy/rewrite-policy/)

[CPX Rewrite Action](https://developer-docs.citrix.com/projects/netscaler-command-reference/en/12.0/rewrite/rewrite-action/rewrite-action/)

[CPX Responder Policy](https://developer-docs.citrix.com/projects/netscaler-command-reference/en/12.0/responder/responder-policy/responder-policy/)

[CX Responder Action](https://developer-docs.citrix.com/projects/netscaler-command-reference/en/12.0/responder/responder-action/responder-action/)

