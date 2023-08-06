# shudder

Shudder is a service for facilitating graceful shutdowns in AWS autoscaling
groups.

It works by making use of
[Lifecycle Hooks](http://docs.aws.amazon.com/cli/latest/reference/autoscaling/put-lifecycle-hook.html). You
give your autoscaling group a lifecycle hook that publishes to an SNS topic that
you configure in shudder. When shudder starts up, it will create an SQS queue
for the instance it is running on and subscribe it to the SNS topic. It polls
for new messages and waits for one that is a termination command for this
instance. It can then send a GET request to a configured endpoint telling it to
shut down gracefully, or execute commands.

It can also detect when a spot instance has been scheduled for termination,
using the [instance termination notice](https://aws.amazon.com/blogs/aws/new-ec2-spot-instance-termination-notices/)
available in instance metadata. The same configured endpoint will be hit if
a scheduled termination of a spot instance is detected.

## Usage

Install it!

```
pip install .
```

You need a toml file looking like this:

```toml
sqs_prefix = "myapp"
region = "us-east-1"
sns_topic = "arn:aws:sns:us-east-1:723456455537:myapp-shutdowns"
endpoints = ["http://127.0.0.1:5000/youaregoingtodiesoon", "http://127.0.0.1:5001/shutdown"]
commands = [["//etc/init.d/nginx", "stop"], ["/etc/init.d/filebeats", "stop"]]
```

You can specify the config file path as an environment variable:

```bash
CONFIG_FILE=/home/ubuntu/shudder.toml python -m shudder
```

Shudder expects you to have credentials *somehow*. Ideally you have an IAM role
on your server and it can pick it up that way, otherwise it'll look for a
`~/.boto` config or environment variables for `AWS_ACCESS_KEY_ID` and
`AWS_SECRET_ACCESS_KEY`.

*This project has to be run on an EC2 instance because it looks up the instance
 ID in the instance metadata. It'll break anywhere but on EC2.*

## Permissions

Your credentials need to be able to subscribe to your SNS
topic, unsubscribe from your subscription ARN,
as well as create and read from SQS queues under the prefix configured.

### Example IAM Role for Instance running Shudder

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "autoscaling:RecordLifecycleActionHeartbeat",
        "autoscaling:CompleteLifecycleAction"
      ],
      "Resource": "arn:aws:autoscaling:*:*:*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "sqs:*"
      ],
      "Resource": [
        "arn:aws:sqs:*:0123456789:*:*"
      ],
      "Effect": "Allow"
    },
    {
      "Action": [
        "sns:Unsubscribe"
      ],
      "Resource": [
        "*"
      ],
      "Effect": "Allow"
    },
    {
      "Action": [
        "sns:Subscribe"
      ],
      "Resource": [
        "arn:aws:sns:us-east-1:0123456789:*"
      ],
      "Effect": "Allow"
    }
  ]
}
```

## Enabling lifecycle hooks
Unfortunately, lifecycle hooks cannot be managed from CloudFormation or from the web console. To set up a hook, you may need to use the CLI as follows:

```bash
aws autoscaling put-lifecycle-hook
  --lifecycle-hook-name really-cool-hook-name
  --auto-scaling-group-name my-asg-name
  --lifecycle-transition autoscaling:EC2_INSTANCE_TERMINATING
  --role-arn arn:aws:iam::0123456789:role/autoscaling-lifecycle-sqs
  --notification-target-arn arn:aws:sns:us-east-1:0123456789:instance-shutdowns
  --heartbeat-timeout 300
  --default-result CONTINUE
```

The specified role must have the right to publish to the specified topic:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "arn:aws:sns:us-east-1:0123456789:instance-shutdowns"
    }
  ]
}
```

This role must be assumable by the autoscaling service, with a trust relationship policy like this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "autoscaling.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
