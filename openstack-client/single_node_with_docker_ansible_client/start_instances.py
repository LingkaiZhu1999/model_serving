# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random, re
import inspect
from os import environ as env

from novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


flavor = "ssc.medium"
private_net = "UPPMAX 2022/1-1 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 20.04 - 2021.03.23"

identifier = 1

loader = loading.get_plugin_loader('password')

key_name = 'LingkaiZhu'
auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)


if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/prod-cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_prod = open(cfg_file_path)
else:
    sys.exit("prod-cloud-cfg.txt is not in current working directory")

cfg_file_path =  os.getcwd()+'/dev-cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_dev = open(cfg_file_path)
else:
    sys.exit("dev-cloud-cfg.txt is not in current working directory")    

secgroups = ['Lingkai']

print ("Creating instances ... ")
instance_prod = nova.servers.create(name="prod_server_with_docker_"+str(identifier), image=image, flavor=flavor, key_name=key_name,userdata=userdata_prod, nics=nics,security_groups=secgroups)
instance_dev_1 = nova.servers.create(name="dev_server_lingkai"+str(identifier), image=image, flavor=flavor, key_name=key_name,userdata=userdata_dev, nics=nics,security_groups=secgroups)
instance_dev_2 = nova.servers.create(name="dev_server_lingkai"+str(identifier+1), image=image, flavor=flavor, key_name=key_name,userdata=userdata_dev, nics=nics,security_groups=secgroups)
instance_dev_3 = nova.servers.create(name="dev_server_lingkai"+str(identifier+2), image=image, flavor=flavor, key_name=key_name,userdata=userdata_dev, nics=nics,security_groups=secgroups)
inst_status_prod = instance_prod.status
inst_status_dev_1 = instance_dev_1.status
inst_status_dev_2 = instance_dev_2.status
inst_status_dev_3 = instance_dev_3.status


print ("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status_prod == 'BUILD' or inst_status_dev_1 == 'BUILD' or inst_status_dev_2 == 'BUILD' or inst_status_dev_3 == 'BUILD':
    print ("Instance: "+instance_prod.name+" is in "+inst_status_prod+" state, sleeping for 5 seconds more...")
    print ("Instance: "+instance_dev_1.name+" is in "+inst_status_dev_1+" state, sleeping for 5 seconds more...")
    print("Instance: " + instance_dev_2.name + " is in " + inst_status_dev_2 + " state, sleeping for 5 seconds more...")
    print("Instance: " + instance_dev_3.name + " is in " + inst_status_dev_3 + " state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance_prod = nova.servers.get(instance_prod.id)
    inst_status_prod = instance_prod.status
    instance_dev_1 = nova.servers.get(instance_dev_1.id)
    inst_status_dev_1 = instance_dev_1.status
    instance_dev_2 = nova.servers.get(instance_dev_2.id)
    inst_status_dev_2 = instance_dev_2.status
    instance_dev_3 = nova.servers.get(instance_dev_3.id)
    inst_status_dev_3 = instance_dev_3.status

ip_address_prod = None
for network in instance_prod.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_prod = network
        break
if ip_address_prod is None:
    raise RuntimeError('No IP address assigned!')

ip_address_dev_1 = None
for network in instance_dev_1.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_dev_1 = network
        break
if ip_address_dev_1 is None:
    raise RuntimeError('No IP address assigned!')

ip_address_dev_2 = None
for network in instance_dev_2.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_dev_2 = network
        break
if ip_address_dev_2 is None:
    raise RuntimeError('No IP address assigned!')

ip_address_dev_3 = None
for network in instance_dev_3.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_dev_3 = network
        break
if ip_address_dev_3 is None:
    raise RuntimeError('No IP address assigned!')

print ("Instance: "+ instance_prod.name +" is in " + inst_status_prod + " state" + " ip address: "+ ip_address_prod)
print ("Instance: "+ instance_dev_1.name +" is in " + inst_status_dev_1 + " state" + " ip address: "+ ip_address_dev_1)
print ("Instance: "+ instance_dev_2.name +" is in " + inst_status_dev_2 + " state" + " ip address: "+ ip_address_dev_2)
print ("Instance: "+ instance_dev_3.name +" is in " + inst_status_dev_3 + " state" + " ip address: "+ ip_address_dev_3)
