# kzconfig

General kazoo configuration wrappers and helpers.  Wraps the following:
* python-couchdb
* kazoo-sdk
* pyrkube
* dnsimple


## Usage
```python
from kzconfig import Context
context = Context()


rabbit_pod = context.kube.get('pod', 'rabbitmq')
db = context.couchdb['system_config']

env = context.configs['environment']
couchdb_creds = context.secrets['couchdb']

context.dns.add('A', '192.168.0.1')

master_acct = context.kazoo.get_account(context.secrets['master-account'])

context.sup.kz_nodes.status()
```


## CLI Commands
### `sup`

#### Usage
```
Usage: sup [OPTIONS] MODULE FUNCTION [ARGS]...

Options:
  --help  Show this message and exit.
```

### `install-kubectl`

#### Usage
```
Usage: install-kubectl [OPTIONS]

Options:
  --help  Show this message and exit.
```

Installs kubectl version == KUBECTL_VERSION || 1.7.8.

If you override the version using environment variables, be sure to override KUBECTL_SHA256 also.


#### Example

```
sup kz_nodes status
```


