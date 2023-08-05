# Copyright 2015,2016 Nir Cohen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

import boto3


# TODO: Provider a schema for each provider to validate that the relevant
# parameters are passed to its client instantiation.

class AWS(object):
    def __init__(self, conn):
        session = boto3.Session(
            aws_access_key_id=conn.get('aws_access_key_id'),
            aws_secret_access_key=conn.get('aws_secret_access_key'),
            profile_name=conn.get('profile'),
            region_name=conn.get('region'))
        self.ec2client = session.client('ec2')

    def nodes(self, tag_key, tag_value):
        response = self.ec2client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:' + tag_key,
                    'Values': [tag_value]
                }
            ]
        )
        instancelist = []
        for reservation in (response["Reservations"]):
            for instance in reservation["Instances"]:
                instancelist.append(instance["PrivateIpAddress"])
        return instancelist


PROVIDER_MAPPING = {
    'aws': AWS
}


def _assert_required_params_passed(kwargs):
    require = ['tag_key', 'tag_value']
    for k in require:
        if not kwargs.get(k):
            raise PyDiscoverError('Must pass tag_key and tag_value params')


def nodes(provider, **kwargs):
    _assert_required_params_passed(kwargs)
    discover = PROVIDER_MAPPING[provider](kwargs)
    return discover.nodes(kwargs['tag_key'], kwargs['tag_value'])


class PyDiscoverError(Exception):
    pass
