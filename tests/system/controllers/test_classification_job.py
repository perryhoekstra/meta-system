#  **********************************************************************
#  Copyright (C) 2020 Johns Hopkins University Applied Physics Laboratory
#
#  All Rights Reserved.
#  For any other permission, please contact the Legal Office at JHU/APL.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  **********************************************************************
import unittest

import pydash
import pymongo
from pymodm import connect

from shared.config import config
from system.controllers import classification_job, user_job, user
from system.models.job_manager import JobMode, JobStatus


class TestClassificationJobController(unittest.TestCase):
    def setUp(self) -> None:
        self.mongo_uri = config.MONGO_URI
        self.my_client = pymongo.MongoClient(self.mongo_uri)
        self.db_name = "TestMETA"
        self.db = self.my_client[self.db_name]
        connect(self.mongo_uri + self.db_name)  # Connect to MongoDB

        self.user_id = user.insert("Joe Schmo", "Joe.Schmo@hotmail.com", [])
        self.user_job_id = user_job.insert(user_id=self.user_id, title="my job title", read_types=["Z"],
                                           classifiers=["A", "B"], mode=JobMode.REAL_READS)
        self.classification_job_id = classification_job.insert(user_job_id=self.user_job_id, classifier="kraken",
                                                               fastq_path="file.fastq")

    def test_insert(self):
        classification_job_id = classification_job.insert(user_job_id=self.user_job_id, classifier="kraken",
                                                          fastq_path="file.fastq")
        self.assertIsNotNone(classification_job_id)

        classification_job_id = classification_job.insert(user_job_id=self.user_job_id, classifier="kraken",
                                                          read_type="miseq", fastq_path="file.fastq")
        self.assertIsNotNone(classification_job_id)

    def test_find_by_id(self):
        data = classification_job.find_by_id(class_job_id=self.classification_job_id)
        self.assertIsNotNone(data)

    def test_find_specific_job(self):
        data = classification_job.find_specific_job(user_job_id=self.user_job_id, classifier="kraken",
                                                    read_type="miseq")
        self.assertIsNone(data)

        data = classification_job.find_specific_job(user_job_id=self.user_job_id, classifier="kraken")
        self.assertIsNotNone(data)

    def test_update_wall_clock_time(self):
        classification_job.update_wall_clock_time(obj_id=self.classification_job_id, time=0.0056)
        data = classification_job.find_by_id(class_job_id=self.classification_job_id)
        res = pydash.get(data, "wall_clock_time")
        self.assertEqual(res, 0.0056)

    def test_max_memory_MBs(self):
        classification_job.update_max_memory_MBs(obj_id=self.classification_job_id, max_mem=500.28)
        data = classification_job.find_by_id(class_job_id=self.classification_job_id)
        res = pydash.get(data, "max_memory_MBs")
        self.assertEqual(res, 500.28)

    def test_update_cpu_time(self):
        classification_job.update_cpu_time(obj_id=self.classification_job_id, time=0.12789)
        data = classification_job.find_by_id(class_job_id=self.classification_job_id)
        res = pydash.get(data, "cpu_time")
        self.assertEqual(res, 0.12789)

    def test_update_container_id(self):
        classification_job.update_container_id(obj_id=self.classification_job_id, container_id="8cd216ad9b38")
        data = classification_job.find_by_id(class_job_id=self.classification_job_id)
        res = pydash.get(data, "container_id")
        self.assertEqual(res, "8cd216ad9b38")

    def test_update_status(self):
        classification_job.update_status(obj_id=self.classification_job_id, new_status=str(JobStatus.QUEUED))
        data = classification_job.find_by_id(class_job_id=self.classification_job_id)
        res = pydash.get(data, "status")
        self.assertEqual(res, str(JobStatus.QUEUED))

    def tearDown(self) -> None:
        col_list = self.db.list_collection_names()
        for col in col_list:
            self.db.drop_collection(col)