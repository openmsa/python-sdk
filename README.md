MSA Python SDK
![Tests](https://github.com/openmsa/python-sdk/workflows/Python%20application/badge.svg)


## For developers, run outside any containers

### 1) Get source :
 git clone https://github.com/openmsa/python-sdk 

### 2) Install pyenv + pyenv plugins

 #Under Centos 7.9:
  yum install -y gcc zlib zlib-devel libffi-devel
  yum install -y openssl openssl-libs openssl-devel


	curl -L https://raw.github.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

	cat >> ~/.bashrc <<<'
	export PATH="$HOME/.pyenv/bin:$PATH"
	eval "$(pyenv init -)"
	eval "$(pyenv virtualenv-init -)"
	'

### 3) Setup a python dev environment for the project


	which pyenv || source ~/.bashrc

	pyenv install 3.7.3
	cd ..   
	python3.6 -m pip install -r python-sdk/requirements.txt
	 


### 4) Running unit tests

  cd  python-sdk

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

### Generate Documenation and Json references
`$ pdoc --html --force -o html msa_sdk`

then copy all files under `html/msa_sdk/` to `msa-docker/front/msa_sdk_doc`

Note: in order to run this a msa-api container needs to be running.

`$ python sdk_to_json.py > msa_sdk.json`

move the msa_sdk.json to msa-docker/front/msa_sdk_doc



### Trainning container
### How to create
cd  python-sdk
- `$ ./training_container build`

### How to start interactive mode
- `$ ./training_container ipython`

### Notebook container
# Create the container
$ ./training_container build

# Run the container
$ ./training_container start
Open http://127.0.0.1:8888 in your browser
Password is `ubitrain`.

# acces with bash : jolly_taussig
docker exec  -it jolly_taussig bash

# Stop the container
$ ./training_container stop

