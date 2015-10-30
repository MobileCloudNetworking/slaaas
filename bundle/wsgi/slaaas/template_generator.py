#   Copyright (c) 2013-2015, Mobile Cloud Networking (MCN) project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

__author__ = "Claudio Marques"
__copyright__ = "Copyright (c) 2013-2015, Mobile Cloud Networking (MCN) project"
__credits__ = [""]
__license__ = "Apache"
__version__ = "1.0"
__maintainer__ = ""
__email__ = ""
__status__ = "Production"

"""
Template Generator for SLAaaS.
Version 1.0
"""

# Bart tenat mcn-dns
BART_PUBLIC_NET_ID = '77e659dd-f1b4-430c-ac6f-d92ec0137c85'
BART_PRIVATE_NET_ID = '82c56778-da2c-4e12-834d-8d09958d0563'
BART_PRIVATE_SUBNET_ID = '0e768fd0-2bbc-482c-9cbd-7469529d141f'
BART_KEY_NAME = 'mcn-key'

class SLAaaSTemplateGenerator(object):

    def __init__(self, maas_endpoint=None, rcb_mq_endpoint=None):
        self.numProvisioned = 0

        if maas_endpoint is not None:
            self.maas_endpoint = maas_endpoint
        if rcb_mq_endpoint is not None:
            self.rcb_mq_endpoint = rcb_mq_endpoint

        self.public_net_id = BART_PUBLIC_NET_ID
        self.private_subnet_id = BART_PRIVATE_SUBNET_ID
        self.private_net_id = BART_PRIVATE_NET_ID
        self.key_name = BART_KEY_NAME

    def generate(self, provisioning=False):

        template =  '---\n'
        template += 'description: "YAML MCN DNSaaS Template"\n'
        template += 'heat_template_version: 2013-05-23\n'
        template += 'outputs: \n'
        template += '  mcn.endpoint.slaaas: \n'
        template += '    description: "MCN PUBLIC endpoint for SLAaaS"\n'
        template += '    value: \n'
        template += '      get_attr: \n'
        template += '        - slaaas_server_floating_ip\n'
        template += '        - floating_ip_address\n'
        template += '  mcn.endpoint.slaaas_private_ip: \n'
        template += '    description: "MCN PRIVATE endpoint for SLAaaS"\n'
        template += '    value: \n'
        template += '      get_attr: \n'
        template += '        - slaaas_server\n'
        template += '        - first_address\n'
        template += 'parameters: \n'
        template += '  flavor: \n'
        template += '    default: m1.small\n'
        template += '    description: "Flavor to use for the server"\n'
        template += '    type: string\n'
        template += '  image: \n'
        template += '    default: slaaas_image\n'
        template += '    description: "Name of image to use for SLAaaS"\n'
        template += '    type: string\n'
        template += '  key_name: \n'
        template += '    default: mcn-key\n'
        template += '    description: "Name of an existing EC2 KeyPair to enable SSH access to the instances"\n'
        template += '    type: string\n'
        if provisioning:
            template += '  maas_ip_address: \n'
            template += '    default: "' + self.maas_endpoint + '"\n'
            template += '    description: "MaaS Instance"\n'
            template += '    type: string\n'
            template += '  rcb_mq_endpoint: \n'
            template += '    default: "' + self.rcb_mq_endpoint + '"\n'
            template += '    description: "MaaS Instance"\n'
            template += '    type: string\n'
        template += '  private_net_id: \n'
        template += '    default: 82c56778-da2c-4e12-834d-8d09958d0563\n'
        template += '    description: "ID of private network into which servers get deployed"\n'
        template += '    type: string\n'
        template += '  private_subnet_id: \n'
        template += '    default: 0e768fd0-2bbc-482c-9cbd-7469529d141f\n'
        template += '    description: "ID of private sub network into which servers get deployed"\n'
        template += '    type: string\n'
        template += '  public_net_id: \n'
        template += '    default: 77e659dd-f1b4-430c-ac6f-d92ec0137c85\n'
        template += '    description: "ID of public network for which floating IP addresses will be allocated"\n'
        template += '    type: string\n'
        template += 'resources: \n'
        template += '  slaaas_server: \n'
        template += '    properties: \n'
        template += '      flavor: \n'
        template += '        get_param: flavor\n'
        template += '      image: \n'
        template += '        get_param: image\n'
        template += '      key_name: \n'
        template += '        get_param: key_name\n'
        template += '      name: slaaas\n'
        template += '      networks: \n'
        template += '        - \n'
        template += '          port: \n'
        template += '            Ref: slaaas_server_port\n'
        template += '      user_data_format: SOFTWARE_CONFIG\n'
        template += '    type: "OS::Nova::Server"\n'
        template += '  slaaas_server_floating_ip: \n'
        template += '    properties: \n'
        template += '      floating_network_id: \n'
        template += '        get_param: public_net_id\n'
        template += '      port_id: \n'
        template += '        Ref: slaaas_server_port\n'
        template += '    type: "OS::Neutron::FloatingIP"\n'
        template += '  slaaas_server_port: \n'
        template += '    properties: \n'
        template += '      fixed_ips: \n'
        template += '        - \n'
        template += '          subnet_id: \n'
        template += '            get_param: private_subnet_id\n'
        template += '      network_id: \n'
        template += '        get_param: private_net_id\n'
        template += '      replacement_policy: AUTO\n'
        template += '    type: "OS::Neutron::Port"\n'
        if provisioning:
            template += '  Provisioning: \n'
            template += '    properties: \n'
            template += '      config: \n'
            template += '        get_resource: ConfigProvisioning\n'
            template += '      input_values: \n'
            template += '        maas_ip: \n'
            template += '          get_param: maas_ip_address\n'
            template += '        rcb_mq_ip: \n'
            template += '          get_param: rcb_mq_endpoint\n'
            template += '      server: \n'
            template += '        get_resource: slaaas_server \n'
            template += '    type: "OS::Heat::SoftwareDeployment"\n'
            template += '  ConfigProvisioning: \n'
            template += '    properties: \n'
            template += '      config: |-\n'
            template += '          #!/bin/bash\n'
            template += '          /bin/sed -i -- "s/zabbix_server=.*/zabbix_server=$maas_ip/g" /home/ubuntu/slaaas/configs/maas.cfg\n'
            template += '          /bin/sed -i -- "s/host=..*/host=.$rcb_mq_ip/g" /home/ubuntu/slaaas/configs/rabbit.cfg\n'
            template += '          /bin/nohup  sh /home/ubuntu/slaaas/restart_slaaas.sh &\n'
            template += '      group: script\n'
            template += '      inputs: \n'
            template += '        - \n'
            template += '          name: maas_ip\n'
            template += '          name: rcb_mq_ip\n'
            template += '    type: "OS::Heat::SoftwareConfig"\n'
        return template
