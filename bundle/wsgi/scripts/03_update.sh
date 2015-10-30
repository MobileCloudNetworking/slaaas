#!/usr/bin/env bash

#get token


#url=http://dnsasrvinstacbd93655b4b0f04-mcn.apps.cloudcomplab.ch
url=http://127.0.0.1:8051


echo "Command to execute"
#echo $cmd


#
# Provision
##
curl -v -X POST "$url/orchestrator/default?action=update" \
       -H 'X-OCCI-Attribute: mcn.endpoint.maas="23.23.23.23"' \
       -H 'Content-Type: text/occi' \
       -H 'Category: provision; scheme="http://schemas.mobile-cloud-networking.eu/occi/service#"' \
       -H 'X-Auth-Token: '$OS_AUTH_TOKEN \
       -H 'X-Tenant-Name: '$OS_TENANT_NAME \
       -H 'mcn.endpoint.maas : 160.85.4.47' \
       -H 'mcn.endpoint.rcb.mq : 192.168.1.200'

#curl -v -X POST http://160.85.4.53:8888/test-dns/54ccc930ac3c30a8c6000e37 -H 'X-OCCI-Attribute: mcn.endpoint.maas="23.23.23.23"' -H 'Content-type: text/occi' -H 'X-Auth-Token: '$KID -H 'X-Tenant-Name: '$TENANT