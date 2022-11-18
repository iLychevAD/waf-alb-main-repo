### Parts of the solution

1. The Terraform files to create ALB, WAF and a pretending-to-be-a-web-server AWS Lambda (I decided to use a Lambda instead of a EC2 for a web-server imitation) are in the https://github.com/iLychevAD/waf-alb-template repo.

2 . And this repo contains a pytest script to verify whitelisting works (in the `tests` directory), and a CloudFormation (or `CFN` for brevity) template `demo_install.cfn.yaml` to deploy other components of the solution (more detailed description see below).

#### 1. Terraform files

The ALB, WAF, Lambda configuration fully meets the task requirement. The whitelisting rules can be checked by the PyTest script.

Before deploying the resources, some manual modification of the Terraform files is required (had no time to fix that) - namelly, you should change a VPC id and Subnets (in the `variables.tf` ot `terrafrom.tfvars` file. In a finished solution that information would be detected automatically either in the pipeline or by Terraform scripts by using `local exec` functionality) as proper for your AWS account (it's implied that a default VPC is used).

#### 2. The rest of the solution

*Notice* even though I tried to provide a CFN template, it's not working (had no time to troubleshoot and debug it). You can try to deploy it at your own risk - at least it should not hurt your AWS account. Use the following command to deploy:

```
aws cloudformation create-stack --stack-name <SOME NAME> --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND --template-body file://demo_install.cfn.yaml --parameters ParameterKey=NamePrefix,ParameterValue="rb-test-task"
```
*Disclaimer*: the template content is partially taken from https://aws.amazon.com/blogs/devops/multi-branch-codepipeline-strategy-with-event-driven-architecture/

So, further goes mostly a theoretical description of what I was planning to have eventually (you can have more idea about implementation details by looking into the CFN template).

The aforementioned repo (https://github.com/iLychevAD/waf-alb-template) is used to store parametrized Terraform-based "building blocks" which can be used while provided certain values for the parameters to deploy actual instances of itself. So, in this case we have only one such building block that includes ALB+WAF+Lambda combination.

The CFN template creates a CodeCommti repo which serves as a GitOps source of thruth for environments (desired) state. There is a direct correspondence `a git branch` == `an environment` (an env name would be taken from a Git branch name).

That repo workflow supposes that when a new env is to be created, a user (or repo's admin ?) creates a new branch in that repo which effectively means establishing a new env. Then user should put a Terraform file into it, referring a required version of the template, e.g:

```
module "wa-alb-instance" {
  source = "git::https://github.com/iLychevAD/waf-alb-template?ref=v1.0.0"
}
```

(notice, we dont specify variables for the used module here to simplify this parent module configuration. Instead the values for variables to customize a template for a particular environment are fetched from environment variables, see https://github.com/iLychevAD/waf-alb-template/blob/main/locals.tf. The actual values for those env variables are set inside CodeBuild project).
 

### TO DOs:

- CodeBuild project that performs `terraform apply` is granted too much privileges (`policy/AdministratorAccess`), should be narrowed down only to permissions over the AWS resources present in the Terrafrom files

- Pull Requests workflow is not implemented (i.e. when for PRs a CodeBuild executes and displays result of `terraform plan` to give an idead what will happen if the PR is merged)


