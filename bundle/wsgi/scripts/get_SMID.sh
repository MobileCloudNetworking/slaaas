#!/bin/bash

#get token


#url=http://dnsasrvinstacbd93655b4b0f04-mcn.apps.cloudcomplab.ch
url=http://127.0.0.1:8080
#url=http://dnsasrvinstb8ba0a2c5865a7f2-mcn.apps.cloudcomplab.ch


echo "Command to execute"
#echo $cmd

# First Initialize

#region_name can be Ubern, bart, cs or WinterthurSDC
curl -v -X PUT "$url/orchestrator/default" \
       -H 'Content-Type: text/occi' \
       -H 'Category: orchestrator; scheme="http://schemas.mobile-cloud-networking.eu/occi/service#"' \
       -H 'X-Auth-Token: '$OS_AUTH_TOKEN \
       -H 'X-Tenant-Name: '$OS_TENANT_NAME \
       -H 'X-OCCI-Attribute: region_name="UBern"' \
       -H 'X-OCCI-Attribute: testbed="ubern"' \
       -H 'X-OCCI-Attribute: scalelimit1=50' \
       -H 'X-OCCI-Attribute: scalelimit2=100' \
       -H 'X-OCCI-Attribute: highavailability="y"'


# Deploy

curl -v -X POST "$url/orchestrator/default?action=deploy" \
       -H 'Content-Type: text/occi' \
       -H 'Category: deploy; scheme="http://schemas.mobile-cloud-networking.eu/occi/service#"' \
       -H 'X-Auth-Token: '$OS_AUTH_TOKEN \
       -H 'X-Tenant-Name: '$OS_TENANT_NAME
