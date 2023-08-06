# pd-observer

Python module that updates a Slack chat room topic with the current on-call for a pagerduty schedule.

This module is based on: https://github.com/PagerDuty/pd-oncall-chat-topic

Small changes apply to this particular code:

* We use the [/oncalls](https://v2.developer.pagerduty.com/page/api-reference#!/On-Calls/get_oncalls) endpoint of the pagerduty v2 API
* We assume that each user will update their names in pagerduty match their slack handle

# Requirements

1. Obtain a Slack API token from a Bot [Directions Here](https://my.slack.com/services/new/bot)
2. Obtain a PagerDuty API Key (v2) [Directions Here](https://support.pagerduty.com/docs/using-the-api#section-generating-an-api-key)
3. Get the unique ID of the Slack channel which you want to manage the topic
4. Get the unique ID of the Pagerduty schedule that you want to monitor

# USAGE

### Running pd_observer standalone

```shell
pd_observer -t xoxb-xxx-xxx -A XxXx -S P... -C ....
```

### Using an HTTP_PROXY

```shell
export HTTP_PROXY=proxy:2138
export HTTPS_PROXY=proxy.3128
pd_observer -t xoxb-xxx-xxx -A XxXx -S P... -C ....
```

### Docker

```shell
docker run -it docker -t xoxb-xxx-xxx -A XxXx -S P... -C ....
```
