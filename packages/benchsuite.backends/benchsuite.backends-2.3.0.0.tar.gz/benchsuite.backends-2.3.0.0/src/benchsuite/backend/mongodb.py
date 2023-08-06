# Benchmarking Suite
# Copyright 2014-2017 Engineering Ingegneria Informatica S.p.A.
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
#
#
# Developed in the ARTIST EU project (www.artist-project.eu) and in the
# CloudPerfect EU project (https://cloudperfect.eu/)
import logging

import datetime
import pytz
from pymongo import MongoClient

from benchsuite.core.model.storage import StorageConnector

from benchsuite.core.model.execution import ExecutionResult

logger = logging.getLogger(__name__)


class MongoDBStorageConnector(StorageConnector):

    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.err_collection = None

    def save_execution_error(self, exec_error):
        r = self.err_collection.insert_one(exec_error.__dict__)
        logger.info('Execution error saved with with id=%s', r.inserted_id)

    def save_execution_result(self, execution_result: ExecutionResult):
        r = self.collection.insert_one({
            'start': datetime.datetime.fromtimestamp(execution_result.start, tz=pytz.utc),
            'duration': execution_result.duration,
            'properties': execution_result.properties,
            'tool': execution_result.tool,
            'workload': execution_result.workload,
            'provider': execution_result.provider,
            'exec_env': execution_result.exec_env,
            'metrics': execution_result.metrics,
            'logs': execution_result.logs,
            'user_id': execution_result.properties['user'] if 'user' in execution_result.properties else None
        })

        logger.info('New execution results stored with id=%s', r.inserted_id)

    @staticmethod
    def load_from_config(config):
        logger.debug('Loading %s', MongoDBStorageConnector.__module__ + "." + __class__.__name__)

        o = MongoDBStorageConnector()
        o.client = MongoClient(config['Storage']['connection_string'])
        o.db = o.client[config['Storage']['db_name']]
        o.collection = o.db[config['Storage']['collection_name']]
        if 'error_collection_name' not in config['Storage']:
            config['Storage']['error_collection_name'] = 'exec_errors'
        o.err_collection = o.db[config['Storage']['error_collection_name']]

        logger.info('MongoDBStorageConnector created for %s, db=%s, coll=%s', config['Storage']['connection_string'], config['Storage']['db_name'], config['Storage']['collection_name'])

        return o


