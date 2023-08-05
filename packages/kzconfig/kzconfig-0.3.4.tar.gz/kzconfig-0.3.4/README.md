# kzconfig

General kazoo configuration wrappers and helpers.  Wraps the following libraries:
* python-couchdb
* kazoo-sdk
* pyrkube
* dnsimple


## Customizing
Subclass `kzconfig.Context`.  In this example, I've chosen to show how a user who wants to use the default conventions except for using a different provider for DNS.

```python
from kzconfig import Context, meta

class MyContext(Context):
    _configs = ('environment',)
    _secrets = ('couchdb', 'rabbitmq', 'master-account', 'dns.coredns')

    def __init__(self, domain='example.org'):
        self.domain = domain

    @meta.lazy_property
    def dns(self):
        return MyDNS(self, self.domain)

...

import CoreDNS

class MyDNS:
    def __init__(self, context, domain):
        self.context = context
        self.domain = domain
        creds = self.context.secrets['dns.coredns']

        self.api = CoreDNS(
            username=creds['email'],
            password=creds['password']
        )

```

Quick example of subclassing without a DNS implementation.
```python
from kzconfig import Context, meta

class MyContext(Context):
    _configs = ('environment',)
    _secrets = ('couchdb', 'rabbitmq', 'master-account', 'dns.coredns')
    _domain = 'example.org'

    def __init__(self, domain='example.org'):
        self.domain = domain

    def dns(self):
        raise NotImplemented
```


## Usage
### Initializing a new context
```python
from kzconfig import Context, meta

context = Context()
```

### Kubernetes
```python
# get the pod named rabbitmq
rabbit_pod = context.kube.api.get('pod', 'rabbitmq')

# defaults to default namespace
all_pods = context.kube.api.get('pod')

# all kube-system pods
all_system_pods = context.kube.api.get('pod', namespace='kube-system')

# get first pod using label selector app=couchdb
first_couchdb_pod = context.kube.api.get_first('pod', selector=dict(app='couchdb'))
```
for more see my pyrkube library...


### CouchDB
```python

# get the system_config database
db = context.couchdb['system_config']
doc = dict(_id='hello')
# save new document to it
db.save(doc)
```

### Kazoo
```python

# get the master account object in kazoo
master_acct = context.kazoo.get_account(context.secrets['master-account'])
```

### DNS
```python
context.dns.add('A', '192.168.0.1')
```

### Sup
```python
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

Installs kubectl version == KUBECTL_VERSION || 1.7.8

If you override the version using environment variables, be sure to override KUBECTL_SHA256 also.


#### Example

```
sup kz_nodes status
```
