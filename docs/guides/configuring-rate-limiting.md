# Configuring rate limiting

To limit the number of requests made by each IP address to sensitive API endpoints within a specified time window, you
can enable `security.rate_limiting` in the configuration file. This feature is particularly useful in safeguarding
against brute-force attacks targeting authentication API endpoints.

For rootless containers, it is essential to configure both the network stack and the port forwarder to use `slirp4netns`
in order to determine the actual client IP address. Before proceeding, ensure that `slirp4netns` is installed on your
machine.

By default, Docker and Podman employ `RootlessKit` as the port forwarder. For Docker, you can find instructions on
changing the port forwarder [here](https://rootlesscontaine.rs/getting-started/docker/#changing-the-port-forwarder). For
Podman, you don't need to do anything, as `slirp4netns` can be picked up automatically.

Please note that it is crucial to correctly configure the container to use `slirp4netns` as mentioned above before
enabling `security.rate_limiting`. Failure to do so will result in rate limiting being applied to all requests,
irrespective of the IP address, as the container won't be able to determine the actual client IP address.

Moreover, when external proxies or load balancers are present in front of the container, it is necessary to specify
their IP addresses in `network.trusted_proxies` in order to obtain the actual client IP address.
