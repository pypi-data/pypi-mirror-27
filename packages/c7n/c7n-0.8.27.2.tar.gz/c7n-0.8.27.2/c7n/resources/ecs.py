# Copyright 2015-2017 Capital One Services, LLC
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
from __future__ import absolute_import, division, print_function, unicode_literals

from c7n.filters import MetricsFilter
from c7n.query import QueryResourceManager
from c7n.manager import resources


@resources.register('ecs')
class ECSCluster(QueryResourceManager):

    class resource_type(object):
        service = 'ecs'
        enum_spec = ('list_clusters', 'clusterArns', None)
        batch_detail_spec = (
            'describe_clusters', 'clusters', None, 'clusters')
        name = "clusterName"
        id = "clusterArn"
        dimension = None
        filter_name = None


@ECSCluster.filter_registry.register('metrics')
class ECSMetrics(MetricsFilter):

    def get_dimensions(self, resource):
        return [{'Name': 'ClusterName', 'Value': resource['clusterName']}]
