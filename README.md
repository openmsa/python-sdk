MSA Python SDK

### Trainning container
#### How to create
- `$ docker build -t training-sdk .`

#### How to start
- `$ docker run --rm -it --name training-container training-sdk ipython`

### Notebook container
```
# Create the container
$ docker build -t training-notebooks -f Dockerfile.msa_sdk .

# Run the container
$ docker run --rm -u $UID -p 8888:8888 -v "$PWD/notebooks:/notebooks" training-notebooks start-notebook.sh  --NotebookApp.notebook_dir=/notebooks
[I 13:52:07.004 NotebookApp] Writing notebook server cookie secret to /home/jovyan/.local/share/jupyter/runtime/notebook_cookie_secret
[I 13:52:07.193 NotebookApp] JupyterLab extension loaded from /opt/conda/lib/python3.7/site-packages/jupyterlab
[I 13:52:07.193 NotebookApp] JupyterLab application directory is /opt/conda/share/jupyter/lab
[I 13:52:07.194 NotebookApp] Serving notebooks from local directory: /notebooks
[I 13:52:07.194 NotebookApp] The Jupyter Notebook is running at:
[I 13:52:07.194 NotebookApp] http://b7b95efd3600:8888/?token=73f5fda4b622313d251dd328734ddcebf0bb04fe5c6d66be
[I 13:52:07.195 NotebookApp]  or http://127.0.0.1:8888/?token=73f5fda4b622313d251dd328734ddcebf0bb04fe5c6d66be
[I 13:52:07.195 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 13:52:07.198 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/jovyan/.local/share/jupyter/runtime/nbserver-6-open.html
    Or copy and paste one of these URLs:
        http://b7b95efd3600:8888/?token=73f5fda4b622313d251dd328734ddcebf0bb04fe5c6d66be
     or http://127.0.0.1:8888/?token=73f5fda4b622313d251dd328734ddcebf0bb04fe5c6d66be

```
Copy the last line `http://127.0.0.1:8888/?token=73f5fda4b622313d251dd328734ddcebf0bb04fe5c6d66be` and paste in your browser (the token will be different)





### Generate RPM using docker
#### Prerequisites (only if you are not in a RPM linux distro based)

_This assumes you have docker installed and running_

- Create a docker image that will serve as the builder from [here](http://ubibucket.ubiqube.com/users/efe/repos/eduardo-stuff/browse/docker/rpmbuild)

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
