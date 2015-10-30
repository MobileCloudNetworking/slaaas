#!/usr/bin/env bash

#get token


#url=http://dnsasrvinstacbd93655b4b0f04-mcn.apps.cloudcomplab.ch
url=http://127.0.0.1:8080


echo "Command to execute"
#echo $cmd


#
# DELETE
#
curl -v -X DELETE "$url/orchestrator/default" \
       -H 'Content-Type: text/occi' \
       -H 'X-Auth-Token: '$OS_AUTH_TOKEN \
       -H 'X-Tenant-Name: '$OS_TENANT_NAME