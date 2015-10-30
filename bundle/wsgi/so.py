#   Copyright (c) 2013-2015, Intel Performance Learning Solutions Ltd, Intel Corporation.

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

"""
Sample SO.
"""

import random
import time
import threading
import slaaas.template_generator
import traceback

from sdk.mcn import util
from sm.so import service_orchestrator
from sm.so.service_orchestrator import LOG


class SOE(service_orchestrator.Execution):
    """
    Sample SO execution part.
    """

    def __init__(self, token, tenant, ready_event, stop_event):
        super(SOE, self).__init__(token, tenant)
        self.stack_id = None
        self.rcb_mq_endpoint = None
        self.maas_endpoint = None
        self.ready_event = ready_event
        self.stop_event = stop_event
        self.time_wait = 20
        region_name = 'RegionOne'
        self.deployer = util.get_deployer(token,
                                          url_type='public',
                                          tenant_name=tenant,
                                          region=region_name)


    def design(self):
        """
        Do initial design steps here.
        """
        LOG.info('Executing design - nothing to do here')

    def deploy(self, attributes=None):
        """
        deploy SICs.
        """
        LOG.info('Executing deployment logic ...')
        if self.stack_id is None:
            try:

                self.generator = slaaas.template_generator.SLAaaSTemplateGenerator()
                template = self.generator.generate(False)

                self.stack_id = self.deployer.deploy(template, self.token, name='SLAaaS_' + str(random.randint(1000, 9999)))
                LOG.info('Stack ID: ' + self.stack_id.__repr__())

            except Exception:
                LOG.debug('Error creating stack ')
                traceback.print_exc()
                pass

    def provision(self, attributes):
        """
        (Optional) if not done during deployment - provision.
        """
        LOG.info('Calling provision - nothing to do here yet!')

        if attributes:

            if 'mcn.endpoint.maas' in attributes:
                self.maas_endpoint = str(attributes['mcn.endpoint.maas'])
                LOG.info('MaaS endpoint is: ' + self.maas_endpoint)

            if 'mcn.endpoint.rcb.mq' in attributes:
                self.rcb_mq_endpoint = str(attributes['mcn.endpoint.rcb.mq'])
                LOG.info('RCB MQ endpoint is: ' + self.rcb_mq_endpoint)

        LOG.debug('Executing resource provisioning logic')
        # once logic executes, deploy phase is done
        self.ready_event.set()


    def dispose(self):
        """
        Dispose SICs.
        """
        LOG.info('Disposing of third party service instances...')
        if self.stack_id is not None:
            self.deployer.dispose(self.stack_id, self.token)
            self.stack_id = None
            #
            self.stop_event.set()

    def state(self):
        """
        Report on state.
        """
        if self.stack_id is not None:
            tmp = self.deployer.details(self.stack_id, self.token)
            LOG.info('Returning Stack output state...')
            output = ''
            try:
                output = tmp['output']
            except KeyError:
                pass
            return tmp['state'], self.stack_id, output
        else:
            LOG.info('Stack output: none - Unknown, N/A')
            return 'Unknown', 'N/A', None

    def update(self, provisioning=False, attributes=None):
        """
        Update SICs.
        """
        LOG.info('Executing update logic ...')
        self.maas_endpoint = "10.10.10.10"
        self.rcb_mq_endpoint = "192.168.1.200"

        if attributes:

            if 'mcn.endpoint.maas' in attributes:
                self.maas_endpoint = str(attributes['mcn.endpoint.maas'])
                LOG.info('MaaS endpoint is: ' + self.maas_endpoint)

            if 'mcn.endpoint.rcb.mq' in attributes:
                self.rcb_mq_endpoint = str(attributes['mcn.endpoint.rcb.mq'])
                LOG.info('RCB MQ endpoint is: ' + self.rcb_mq_endpoint)

        while (True):
            if self.stack_id is not None:
                tmp = self.deployer.details(self.stack_id, self.token)
                if tmp['state'] == 'CREATE_COMPLETE' or tmp['state'] == 'UPDATE_COMPLETE':
                    break
                else:
                    time.sleep(10)

        if self.stack_id is not None:
            self.generator = slaaas.template_generator.SLAaaSTemplateGenerator(self.maas_endpoint, self.rcb_mq_endpoint)
            template = self.generator.generate(True)

            self.deployer.update(self.stack_id, template, self.token)
            LOG.info('Updated stack ID: ' + self.stack_id.__repr__())

    def notify(self, entity, attributes, extras):
        super(SOE, self).notify(entity, attributes, extras)

class SOD(service_orchestrator.Decision, threading.Thread):
    """
    Sample Decision part of SO.
    """

    def __init__(self, so_e, token, tenant, ready_event, stop_event):
        super(SOD, self).__init__(so_e, token, tenant)
        threading.Thread.__init__(self)
        self.ready_event = ready_event
        self.stop_event = stop_event
        self.time_wait = self.so_e.time_wait

    def run(self):
        """
        Decision part implementation goes here.
        """

        LOG.debug('SLAaaS SOD - Waiting for deploy and provisioning to finish')
        self.ready_event.wait()
        LOG.debug('SLAaaS SOD - Starting runtime logic...')


        # RUN-TIME MANAGEMENT
        while not self.stop_event.isSet():
            event_is_set = self.stop_event.wait(self.time_wait)

            pass

        if self.stop_event.isSet():
            LOG.debug('SLAaaS SOD - STOP event set after disposal')
class ServiceOrchestrator(object):
    """
    Sample SO.
    """

    def __init__(self, token, tenant):

        self.ready_event = threading.Event()
        self.stop_event = threading.Event()
        self.so_e = SOE(token, tenant, self.ready_event, self.stop_event)
        self.so_d = SOD(self.so_e, token, tenant, self.ready_event, self.stop_event)
        LOG.debug('Starting SOD thread...')
        self.so_d.start()

