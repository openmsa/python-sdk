MSA Python SDK

#### Generate RPM using docker

##### Prerequisites (only if you are not in a RPM linux distro based)

_This assumes you have docker installed and running_

- Create a docker image that will serve as the builder from [here](http://ubibucket.ubiqube.com/users/efe/repos/eduardo-stuff/browse/docker/rpmbuild)

##### Generate RPM

- `$ ./build_rpm`
  (... watch letters go up)
- Your rpm is located in the rpms/

#### Generate an RPM on warm75 (it doesn't work on warm64)

1. Clone the project
2. `mkBL -a`
