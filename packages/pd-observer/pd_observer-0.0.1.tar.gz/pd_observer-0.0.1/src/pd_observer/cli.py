#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2017 Rhommel Lamas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from optparse import OptionParser
import os
import sys
import logging
import requests

log = logging.getLogger('pdobserver')

def log_to_stream(name=None,
                  stream=None,
                  format=None,
                  level=None,
                  debug=False):

    if level is None:
        level = logging.DEBUG if debug else logging.INFO

    if format is None:
        format = '%(message)s'

    if stream is None:
        stream = sys.stderr

    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(format))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

def arg_parse():
    """
    Get all options from user input or default to ENV_VARS
    """
    usage = '%prog [options]'
    description = ('Utility to update the topic of a slack channel with the oncall of a defined schedule')
    parser = OptionParser(usage=usage,
                          description=description)
    parser.add_option(
        '-t',
        '--slack-api-token',
        dest='slack_api_token',
        metavar='SLACK_API_TOKEN',
        help='Slack API token. Default: SLACK_API_TOKEN'
    )
    parser.add_option(
        '-A',
        '--pagerduty-api-key',
        dest='pd_api_key',
        metavar='PD_API_KEY',
        help='Pagerduty API key. Default: PD_API_KEY'
    )
    parser.add_option(
        '-S',
        '--schedule',
        dest='schedule_id',
        metavar='SCHEDULE_ID',
        help='ScheduleID to monitor (PXXXXX). Default: SCHEDULE_ID'
    )
    parser.add_option(
        '-C',
        '--slack-channel',
        dest='slack_channel',
        metavar='SLACK_CHANNEL',
        help='Slack channel to update topic. Default: SLACK_CHANNEL'
    )
    parser.add_option(
        '-P',
        '--topic-prefix',
        dest='topic_prefix',
        metavar='TOPIC_PREFIX',
        help='Slack topic prefix. Default: \'On-Call: @\''
    )
    parser.add_option(
        '--dry-run',
        dest='dry_run',
        default=False,
        action="store_true",
        help='dry-run and not publish to graphite'
    )
    parser.add_option(
        '-q',
        '--quiet',
        dest='quiet',
        default=False,
        action='store_true',
        help='Don\'t print to stderr. (Default: False)'
    )
    parser.add_option(
        '-v',
        '--verbose',
        dest='verbose',
        default=False,
        action='store_true',
        help='Print more messages. (Default: False)'
    )
    (options, args) = parser.parse_args()

    if not options.quiet:
        log_to_stream(name='pdobserver',
                      debug=options.verbose)

    if not options.slack_api_token:
        options.slack_api_token = os.environ['SLACK_API_TOKEN']

    if not options.pd_api_key:
        options.pd_api_key = os.environ['PD_API_KEY']

    if not options.schedule_id:
        options.schedule_id = os.environ['SCHEDULE_ID']

    if not options.slack_channel:
        options.schedule_id = os.environ['SLACK_CHANNEL']

    if not options.topic_prefix:
        options.topic_prefix = 'On-Call: @'

    return options

def get_oncall(pd_api_token,
               schedule_id):
    """
    Get who is on-call on a given schedule
    """
    headers = {}
    headers['Accept'] = 'application/vnd.pagerduty+json;version=2'
    headers['Authorization'] = 'Token token={token}'.format(token=pd_api_token)

    url = 'https://api.pagerduty.com/oncalls'

    payload = {}
    payload['time_zone'] = 'UTC'
    payload['schedule_ids[]'] = schedule_id

    r = requests.get(url, headers=headers, params=payload)
    try:
        sid = r.json()['oncalls'][0]['user']['summary']
    except IndexError:
        log.debug("Schedule Not Found for: {}".format(schedule_id))
        sid = None
    return sid

def get_current_topic(slack_api_token,
                      slack_channel):
    """
    Get the current topic for a slack channel
    """
    payload = {}
    payload['token'] = slack_api_token
    payload['channel'] = slack_channel

    r = requests.post('https://slack.com/api/channels.info', data=payload)
    try:
        current = r.json()['channel']['topic']['value']
        log.debug("Current Topic: '{}'".format(current))
    except KeyError:  # the channel is private
        r = requests.post('https://slack.com/api/groups.info', data=payload)
        current = r.json()
        log.debug("Current Topic: '{}'".format(current))

    return current

def update_slack_topic(slack_api_token,
                       slack_channel,
                       proposed_update,
                       topic_prefix):
    """
    Update the slack topic of a desired slack channel with the information from the on-call
    """
    log.debug("Entered update_slack_topic() with: {} {} {}".format(slack_channel,
                                                                proposed_update,
                                                                topic_prefix))
    payload = {}
    payload['token'] = slack_api_token
    payload['channel'] = slack_channel

    current_topic = get_current_topic(slack_api_token,
                                      slack_channel)
    c_delim_count = current_topic.count('|')

    if c_delim_count < 1:
        if not current_topic:
            new_topic = ("{}{}".format(topic_prefix,
                                       proposed_update))
        else:
            if "On-Call" not in current_topic:
                new_topic = ("{}{} | {}".format(topic_prefix,
                                                proposed_update,
                                                current_topic))
            else:
                new_topic = ("{}{}".format(topic_prefix,
                                           proposed_update))
    else:
        first_part = current_topic.rsplit('|', c_delim_count)[0].strip()
        second_part = current_topic.rsplit('|', c_delim_count)[1].strip()

        new_topic = ("{}{} | {}".format(topic_prefix,
                                        proposed_update,
                                        second_part))

    if current_topic != new_topic:
        if len(new_topic) > 250:
            topic = topic[0:247] + "..."
        payload['topic'] = new_topic

        r = requests.post('https://slack.com/api/channels.setTopic', data=payload)

        if r.json().get('error') == 'channel_not_found':  # private channel
            r = requests.post('https://slack.com/api/groups.setTopic', data=payload)
        log.debug(r.json())
    else:
        log.info('Not updating slack, topic is the same')

        return None

def main():
    """
    Entrypoint
    """

    options = arg_parse()

    who_oncall = get_oncall(options.pd_api_key,
                            options.schedule_id)

    update_oncall = update_slack_topic(options.slack_api_token,
                                       options.slack_channel,
                                       who_oncall,
                                       options.topic_prefix)
