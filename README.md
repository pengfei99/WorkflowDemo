# WorkflowDemo

In this project, we show how to use argo workflow to automate your workflows. Note that a workflow is just a sequence of processes through which a piece of work passes from initiation to completion. You can use it to do whatever you want. Below are some application examples

- ETL/Data pipeline
- CI/CD
- Stream processing
- Infra deployment


# quick start

## Install argo client

```shell
# Install argo cd client
git clone https://github.com/pengfei99/InseeDataLabToolInstallation.git
cd InseeDataLabToolInstallation/ubuntu_vm/
sudo sh argo_deb_install.sh

# check your argo cd version
argo version

# output you should see
argo: v3.1.3
  BuildDate: 2021-07-28T05:28:10Z
  GitCommit: 9337abb002d3c505ca45c5fd2e25447acd80a108
  GitTreeState: clean
  GitTag: v3.1.3
  GoVersion: go1.15.7
  Compiler: gc
  Platform: linux/amd64
```

## Run your first workflow

Create a file called hello-argo.yaml, and put below content in it.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow                  # new type of k8s spec
metadata:
  # name of the workflow spec, generate name will add a random number at the end
  # The generate name is useful when you resubmit, so it will not overwrite the old workflow
  # history, because it will always have a new name.
  # you can use name to have a static workflow name.
  generateName: hello-world-
  # name: hello-world
spec:
  entrypoint: whalesay          # invoke the whalesay template
  templates:
    - name: whalesay              # name of the template
      container:
        image: docker/whalesay
        command: [cowsay]
        args: ["hello world"]
        resources:
        # request is the minmun resource quarantee by the cluster, if no limits sets and the host server has more resource, the container can use more resource 
          requests:
            memory: "512Mi"
            cpu: "1000m"
        # limit set the maximum resource allow to the container, even the host server has more available resource, the container can not use it. 
          limits:
            memory: "1024Mi"
            cpu: "2000m"    
```


