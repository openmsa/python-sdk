MSA Python SDK

### Trainning container
#### How to create
- `$ ./training_container build`

#### How to start interactive mode
- `$ ./training_container ipython`

### Notebook container
```
# Create the container
$ ./training_container build

# Run the container
$ ./training_container start
Open http://127.0.0.1:8888 in your browser
```
Password is `ubitrain`.

```
# Stop the container
$ ./training_container stop
```

### Generate RPM using docker
#### Prerequisites (only if you are not in a RPM linux distro based)

_This assumes you have docker installed and running_

- Create a docker image that will serve as the builder

	./init


#### Generate RPM

- `$ ./build_rpm`
  (... watch letters go up)
- Your rpm is located in the rpms/

#### Generate an RPM on warm75 (it doesn't work on warm64)

1. Clone the project
2. `mkBL -a`

### Run unit tests

1. Make sure you have all the prod requirements `pip install -r requirements.txt`
1. Make sure you have all the dev requirements `pip install -r requirements-dev.txt`
1. Run the tests: `./run_tests [normal|html|verbose|quiet]`
  - `Cover` should be **100%** for all the files

```
Name                       Stmts   Miss  Cover
----------------------------------------------
msa_sdk/__init__.py            1      0   100%
msa_sdk/constants.py           8      0   100%
msa_sdk/device.py            115      0   100%
msa_sdk/msa_api.py            63      0   100%
msa_sdk/orchestration.py      53      0   100%
msa_sdk/order.py              15      0   100%
msa_sdk/repository.py         11      0   100%
msa_sdk/util.py               93      0   100%
----------------------------------------------
TOTAL                        359      0   100%

```
*Image above is only an example*


Install pyenv + pyenv plugins
-----------------------------

	curl -L https://raw.github.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

	cat >> ~/.bashrc <<<'
	export PATH="$HOME/.pyenv/bin:$PATH"
	eval "$(pyenv init -)"
	eval "$(pyenv virtualenv-init -)"
	'

Setup a python dev environment for the project
----------------------------------------------

	which pyenv || source ~/.bashrc

	pyenv install 3.7.3
	python -m pip install -r requirements.txt
