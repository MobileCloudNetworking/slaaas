# SLA service

This service provides tenant instances of the SLA service

## Service Dependencies

 * Monitoring service to retrieve metrics
   * parameter: `mcn.endpoint.maas`
 * RCB service and access to its RabbitMQ endpoint to report violations
   * parameter: `mcn.endpoint.rcb.mq`

It does not use the resolver component to get these dependencies and expects
the required parameters supplied by the higher level E2E orchestrator.

This service returns the endpoint on which the SLA service is available at.

 * parameter: `mcn.endpoint.slaaas`
