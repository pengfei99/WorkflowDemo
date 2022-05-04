The official [doc](https://argoproj.github.io/argo-workflows/cron-workflows/) 
# Introduction

**CronWorkflow are workflows that run on a preset schedule**. They are designed to be converted from Workflow easily and to mimic the same options as Kubernetes CronJob. In essence, **CronWorkflow = Workflow + some specific cron options**.


# Example

```yaml
apiVersion: argoproj.io/v1alpha1
kind: CronWorkflow
metadata:
  name: cronflow-with-params
spec:
  # cron scheduler manifest
  schedule: "* * * * *"
  concurrencyPolicy: "Allow"
  startingDeadlineSeconds: 0
  # the number of successful job which will be saved, default value is 3.
  successfulJobsHistoryLimit: 4
  # set the controller to save the number of failed jobs, default valie is 1
  failedJobsHistoryLimit: 2
  # workflow manifest
  workflowMetadata:
    labels:
      pengfei: true
  workflowSpec:
    entrypoint: main
    arguments:
      parameters:
        - name: message
          value: "hello argo"
    templates:
      - name: main
        container:
          image: busybox
          imagePullPolicy: IfNotPresent
          command: ["sh", -c]
          args: ["echo  {{workflow.parameters.message}}"]
```

To submit a cron workflow

```yaml
# submit cron workflow to argo server
argo cron create <cron-workflow-name>

# check existing cron workflow
argo cron list

# show details of the argo cron workflow
argo cron get <cron-workflow-name>
```