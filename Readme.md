# Bootstrapper Server

This is the server part of the [SCION Endhost Bootstrapper](https://github.com/netsec-ethz/bootstrapper) to bootstrap SCION hosts in your AS.

## Requirements
This setup requires to have `Docker` and `Docker Compose` installed on your node, please refer to the official documentations about this. 

Furthermore, you need to have an IP address for your bootstrapping server that is reachable from all potential SCION endhosts within your AS. Let's call this IP `123.123.123.123` for the rest of this documentation.

## Setup
To run the server part, just clone this repo on a node that runs SCION in your AS. It's is required that the chosen node has all the `TRCs` of your AS under `/etc/scion/certs` and a valid `Topology` file under `/etc/scion/topology.json`. Please ensure this.

To bootstrap clients, you need to have a `bootstrapper URL`. This server setup defaults to use port `8041` on all given IP addresses of your machine. You can specify a particular IP address by changing the `ports` configuration of the `nginx` service in `docker-compose.yml`. 

To run the server, just run `docker compose up -d` in this repository. Your bootstrap server is now reachable under `http://123.123.123.123:8041/`.

## Testing routes manually
You can skip this step if you want to just play around with the bootstrapper, check `Connecting Clients` below. The following routes should return valid content that match your AS configuration and the available TRCs:
- Topology: `http://123.123.123.123:8041/topology`
- TRCs.json: `http://123.123.123.123:8041/trcs`

## Connecting Clients
The easiest way to test your server is to use the `[mock]` config entry in your `bootstrapper.toml` file. 

## Adjusting the Topology
Depending on your initial configuration, you may need to change the internal address of the `Border Router` and `Control Service` in your AS to make it available in your AS. Consider this example where both addresses are bound to localhost, which means only the node itself can connect via SCION:

```json
{
  ...
  "border_routers": {
    "br-1": {
      "interfaces": {
        ...
      },
      "internal_addr": "127.0.0.1:30001"
    }
  },
   ...
  "control_service": {
    "cs-1": {
      "addr": "127.0.0.1:30254"
    }
  },
  ...
}
```

Change it to your node's IP that is reachable within the AS. **Note: Be careful with setting this to publicly reachable IP addresses, you may need to apply firewall rules or other mechanisms to avoid hosts outside of your AS to connect to your services.**
```json
{
  ...
  "border_routers": {
    "br-1": {
      "interfaces": {
        ...
      },
      "internal_addr": "123.123.123.123:30001"
    }
  },
   ...
  "control_service": {
    "cs-1": {
      "addr": "123.123.123.123:30254"
    }
  },
  ...
}
```