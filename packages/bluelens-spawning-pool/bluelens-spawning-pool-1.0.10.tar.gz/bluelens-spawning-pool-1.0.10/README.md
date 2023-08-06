# bluelens-spawning-pool
This is utility package to spawn a new Pod in the BlueLens cloud.


## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com//.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com//.git`)

Then import the package:
```python
import bluelens_spawning_pool 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import bluelens_spawning_pool
```

## Getting Started

### Write your code 
```python
from __future__ import print_function
from bluelens_spawning_pool import spawning_pool

pool = spawning_pool.SpawningPool()

project_name = 'bl-cropper'

pool.setServerUrl('35.187.244.252')
pool.setApiVersion('v1')
pool.setKind('pod')
pool.setMetadataName(project_name)
pool.setMetadataNamespace('index')
pool.addMetadataLabel('name', project_name)
container = pool.createContainer()
pool.setContainerName(container, project_name)
pool.addContainerEnv(container, 'key1', 'xxxxx')
pool.addContainerEnv(container, 'key2', 'yyyyy')
pool.setContainerImage(container, 'bluelens/bl-cropper:latest')
pool.addContainer(container)
pool.setRestartPolicy('Never')
pool.spawn()

## Author
master@bluehack.net

