# pyenet

pyenet is a python wrapper for the ENet library by Lee Salzman,
 http://enet.bespin.org

It was originally written by Scott Robinson <scott@tranzoa.com> and is
currently maintained by Andrew Resch <andrewresch@gmail.com>

This fork is being maintained by the piqueserver team for purposes of including
patches for bugs found while developing piqueserver, and to provide a package
on pypi.

## License

pyenet is licensed under the BSD license, see LICENSE for details.
enet is licensed under the MIT license, see http://enet.bespin.org/License.html

## Dependencies

Building pyenet requires all the same dependencies as enet plus Cython and,
obviously, Python.

## Installation

### From pypi

```
pip install pyenet
```

### Manually from git

Note: the enet sources are automatically downloaded from http://enet.bespin.org/
by `setup.py`.

This version of pyenet requires enet 1.3.

Run the setup.py build:

```
$ python setup.py build
```

Once that is complete, install the new pyenet module:

```
# python setup.py install
```

## Packaging notes

- update package version in `setup.py`

- set up the venv:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r dev-requirements.txt
  ```

- build the sdist: `python setup.py sdist`
- build the bdist wheel:
  - ```
    sudo docker run -i -t -v `pwd`:/io quay.io/pypa/manylinux1_x86_64 /bin/bash
    # from in docker container:
    cd /io
    /opt/python/cp36-cp36m/bin/pip install -r dev-requirements.txt
    ```
- upload to pypi: `twine upload dist/*`
- once successful: commit, tag, push to github

## Usage

Once you have installed pyenet, you only need to import the enet module to
start using enet in your project.

Example server:
```
>>> import enet
>>> host = enet.Host(enet.Address("localhost", 33333), 1, 0, 0)
>>> event = host.service(0)
```
Example client:
```
>>> import enet
>>> host = enet.Host(None, 1, 0, 0)
>>> peer = host.connect(enet.Address("localhost", 33333), 1)
```
More information on usage can be obtained from:
 http://enet.bespin.org/Tutorial.html


