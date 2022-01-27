MSA Python SDK
![Tests](https://github.com/openmsa/python-sdk/workflows/Python%20application/badge.svg)


#################################################################################
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

### 5) Create your PR in  https://github.com/openmsa/python-sdk


### 6) Generate Documentation and Json references

#### For documentation
Go to https://github.com/ubiqube/msa-docker/pulls and merge the PR that was
created with the changes in the documentation

#### For json references
Note: in order to run this, the msa_api container needs to be running on port 8480:
 cf file docker-compose.yml, add port 8480 like :
 ```
   msa_api:
    container_name: msa_api
    image: ubiqube/msa2-api:1b2b029b43dcba54bab6c70b1ed5b45e4142b7d3
    healthcheck:
      test: ["CMD-SHELL", "curl --fail http://localhost:8480"]
    depends_on:
      - db
      - msa_es
    ports:
      - "8480:8480"
```
  and restart docker-compose

  `$ python sdk_to_json.py > msa_sdk.json`
    It will update/create file msa_sdk.json


### 7) Save Json references

Note: This should be done after the documentation PR is approved and merged

   You have to save the file `msa_sdk.json` into  https://github.com/ubiqube/msa-docker/tree/master/front/msa_sdk_doc

7.1) Clone https://github.com/ubiqube/msa-docker/tree/master/front/msa_sdk_doc
7.2) Copy `msa_sdk.json` into msa-docker/front/msa_sdk_doc/
7.3) Create the new PR
7.4) After merge it, you can check the new doc  into
	   https://</msa_IP>/msa_sdk/index.html


#################################################################################
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

 
