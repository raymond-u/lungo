# Architecture

```mermaid
graph LR
    Host(Host) --> Portal(Portal<br /><br />Openresty)
    Portal -->|Perform real IP forwarding<br />and rate limiting| Proxy(Reverse Proxy<br /><br />Openresty)
    Proxy <--->|Authorize requests| Auth(Access Control<br /><br />Oathkeeper) ---> Control
    Proxy ---> UI(Web UI<br /><br />Node.js)
    UI --->|Find accessible apps| Control
    UI ---> Backends

    subgraph Control [&nbsp]
        subgraph P1 [Access Control Backends]
            subgraph P2 [&nbsp]
                direction TB
                Authenticator(Authenticator<br /><br />Kratos) ~~~ Authorizer(Authorizer<br /><br />Keto)
            end
        end
    end

    subgraph Backends [&nbsp]
        subgraph P3 [App Backends]
            subgraph P4 [&nbsp]
                direction TB
                App1(App 1) ~~~ App2(App 2) ~~~ App0(...)
            end
        end
    end

    classDef Dotted stroke-dasharray: 5 5
    class Control,Backends Dotted
    classDef Padding fill: none, stroke: none
    class P1,P2,P3,P4 Padding
```

Lungo consists of three primary components:

- **Reverse proxy** - Openresty, responsible for authorizing incoming requests using Oathkeeper and forwarding them to
  the relevant backend.
- **Access control backends** - Kratos and Keto, which manage user authentication and authorization, respectively.
- **Application backends** - a set of applications accessible through the proxy.
