# Workflow Templates (v2.4 and after)

## Introduction

WorkflowTemplates are definitions of Workflows that live in your cluster. This allows you to create a library of frequently-used templates and reuse them either by submitting them directly (v2.7 and after) or by referencing them from your Workflows.

## Parameters in template

### Global parameters

When working with global parameters, you can instantiate your global variables in your Workflow and then directly reference them in your WorkflowTemplate. Below is a working example:




## usefull command

```shell
# submit template to the argo server
argo template create <template-file-path>

# list existing template
argo template list
```