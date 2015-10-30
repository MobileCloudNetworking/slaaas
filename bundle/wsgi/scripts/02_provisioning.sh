#!/usr/bin/env bash

#get token


#url=http://dnsasrvinstacbd93655b4b0f04-mcn.apps.cloudcomplab.ch
url=http://127.0.0.1:8080


echo "Command to execute"
#echo $cmd


#
# Provision
#
curl -v -X POST "$url/orchestrator/default?action=provision" \
       -H 'Content-Type: text/occi' \
       -H 'Category: provision; scheme="http://schemas.mobile-cloud-networking.eu/occi/service#"' \
       -H 'X-Auth-Token: '$OS_AUTH_TOKEN \
       -H 'X-Tenant-Name: '$OS_TENANT_NAME