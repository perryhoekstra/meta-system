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

import json

from pymodm import MongoModel, fields

from system.models.job_manager import JobStatus
from system.models.job_manager import JobType
from system.utils.encoder import json_encoder


class User(MongoModel):
    # Dynamic
    name = fields.CharField()
    email = fields.CharField()
    user_jobs = fields.ListField(blank=True)  # List of UserJobs generated by User

    def __repr__(self):
        return self.as_dict().__repr__()

    def __str__(self):
        return self.as_dict().__str__()

    def as_dict(self):
        return self.to_son().to_dict()

    def as_json(self):
        return json.dumps(self.as_dict(), separators=(",", ":"), default=json_encoder)  # , cls=SchemaJSONEncoder)

    class Meta:
        collection_name = "User"
        ignore_unknown_fields = True
        final = True
        indexes = []  # TODO


class UserJob(MongoModel):
    user_id = fields.ObjectIdField()  # ObjectId for User who ordered UserJob
    title = fields.CharField()  # Title provided by the user
    read_types = fields.ListField()  # Which read types to use for this UserJob
    abundance_tsv = fields.CharField()  # The path for the abundance profile (.tsv)
    fastq = fields.CharField()  # The path for the sequence profile (.fastq)
    classifiers = fields.ListField()  # Which classifiers to use for this UserJob
    started_datetime = fields.DateTimeField(blank=True)  # The time this UserJob was started
    created_datetime = fields.DateTimeField() #The time this UserJob was created
    mode = fields.CharField(blank=True)  # A field to describe whether this is a real job or a simulation job

    # Dynamic
    child_jobs_completed = fields.IntegerField()  # Number of children jobs that have finished
    total_child_jobs = fields.IntegerField()  # Total number of children jobs for UserJob
    updated_datetime = fields.DateTimeField()  # The time this UserJob was last updated
    queue = fields.ListField(blank=True)  # A list of the Mongo IDs of jobs left to complete
    status = fields.CharField(
        choices=[str(JobStatus.QUEUED), str(JobStatus.PROCESSING), str(JobStatus.COMPLETED), str(JobStatus.FAILED),
                 str(JobStatus.CANCELLED)]
    )  # Status to describe what proportion of jobs in queue are finished
    hide = fields.BooleanField(blank=True)  # Hide Status provided by the user
    completed_datetime = fields.DateTimeField(blank=True)  # The time this UserJob was completed

    def __repr__(self):
        return self.as_dict().__repr__()

    def __str__(self):
        return self.as_dict().__str__()

    def as_dict(self):
        return self.to_son().to_dict()

    def as_json(self):
        return json.dumps(self.as_dict(), separators=(",", ":"), default=json_encoder)  # , cls=SchemaJSONEncoder)

    class Meta:
        collection_name = "UserJob"
        ignore_unknown_fields = True
        final = True  # prevent the _cls field will not be stored in the document
        indexes = []  # TODO


class SimulationJob(MongoModel):
    # Static
    user_job_id = fields.ObjectIdField()  # ObjectId for UserJob who ordered SimulationJob
    read_type = fields.CharField()  # Which read type to use for this SimulationJob
    abundance_tsv = fields.CharField()  # The contents of abundance profile (.tsv)
    number_of_reads = fields.IntegerField()  # The number of reads to do for this SimulationJob
    started_datetime = fields.DateTimeField(blank=True)  # The time this SimulationJob was created
    created_datetime = fields.DateTimeField() #The time this UserJob was created

    # Dynamic
    cpu_time = fields.FloatField(blank=True)  # The cpu time it took to complete this SimulationJob
    wall_clock_time = fields.FloatField(blank=True)  # The wall clock time it took to complete this SimulationJob
    updated_datetime = fields.DateTimeField()  # The time this SimulationJob was last updated
    container_id = fields.CharField()  # The current running container's ID
    queue_position = fields.IntegerField()  # SimulationJob's position in the UserJob queue
    status = fields.CharField(
        choices=[str(JobStatus.QUEUED), str(JobStatus.PROCESSING), str(JobStatus.COMPLETED), str(JobStatus.FAILED),
                 str(JobStatus.CANCELLED)]
    )  # Status to describe what proportion of jobs in queue are finished

    def __repr__(self):
        return self.as_dict().__repr__()

    def __str__(self):
        return self.as_dict().__str__()

    def as_dict(self):
        return self.to_son().to_dict()

    def as_json(self):
        return json.dumps(self.as_dict(), separators=(",", ":"), default=json_encoder)  # , cls=SchemaJSONEncoder)

    class Meta:
        collection_name = "SimulationJob"
        ignore_unknown_fields = True
        final = True  # prevent the _cls field will not be stored in the document
        indexes = []  # TODO


class ClassificationJob(MongoModel):
    # Static
    user_job_id = fields.ObjectIdField()  # ObjectId for UserJob who ordered ClassificationJob
    classifier = fields.CharField()  # Which classifier to use for this ClassificationJob
    read_type = fields.CharField(blank=True)  # Which read type was used to simulate the fastq file
    fastq_path = fields.CharField()  # The filename for the fastq input file
    started_datetime = fields.DateTimeField(blank=True)  # The time this ClassificationJob was created
    created_datetime = fields.DateTimeField() #The time this UserJob was created

    # Dynamic
    cpu_time = fields.FloatField(blank=True)  # The cpu time it took to complete this ClassificationJob
    max_memory_MBs = fields.FloatField(blank=True)  # The maximum amount of memory needed for this classifier
    wall_clock_time = fields.FloatField(blank=True)  # The wall clock time it took to complete this ClassificationJob
    updated_datetime = fields.DateTimeField()  # The time this ClassificationJob was last updated
    container_id = fields.CharField()  # The current running container's ID
    queue_position = fields.IntegerField()  # ClassificationJob's position in the UserJob queue
    status = fields.CharField(
        choices=[str(JobStatus.QUEUED), str(JobStatus.PROCESSING), str(JobStatus.COMPLETED), str(JobStatus.FAILED),
                 str(JobStatus.CANCELLED)]
    )  # Status to describe what proportion of jobs in queue are finished

    def __repr__(self):
        return self.as_dict().__repr__()

    def __str__(self):
        return self.as_dict().__str__()

    def as_dict(self):
        return self.to_son().to_dict()

    def as_json(self):
        return json.dumps(self.as_dict(), separators=(",", ":"), default=json_encoder)  # , cls=SchemaJSONEncoder)

    class Meta:
        collection_name = "ClassificationJob"
        ignore_unknown_fields = True
        final = True  # prevent the _cls field will not be stored in the document
        indexes = []  # TODO


class EvaluationJob(MongoModel):
    # Static
    user_job_id = fields.ObjectIdField()  # ObjectId for UserJob who ordered
    read_type = fields.CharField(blank=True)
    started_datetime = fields.DateTimeField(blank=True)  # The time this EvaluationJob was created
    created_datetime = fields.DateTimeField() #The time this UserJob was created

    # Dynamic
    cpu_time = fields.FloatField(blank=True)  # The cpu time it took to complete this EvaluationJob
    wall_clock_time = fields.FloatField(blank=True)  # The wall clock time it took to complete this EvaluationJob
    updated_datetime = fields.DateTimeField()  # The time this EvaluationJob was last updated
    queue_position = fields.IntegerField()  # EvaluationJob's position in the UserJob queue
    status = fields.CharField(
        choices=[str(JobStatus.QUEUED), str(JobStatus.PROCESSING), str(JobStatus.COMPLETED), str(JobStatus.FAILED),
                 str(JobStatus.CANCELLED)]
    )  # Status to describe what proportion of jobs in queue are finished

    def __repr__(self):
        return self.as_dict().__repr__()

    def __str__(self):
        return self.as_dict().__str__()

    def as_dict(self):
        return self.to_son().to_dict()

    def as_json(self):
        return json.dumps(self.as_dict(), separators=(",", ":"), default=json_encoder)  # , cls=SchemaJSONEncoder)

    class Meta:
        collection_name = "EvaluationJob"
        ignore_unknown_fields = True
        final = True  # prevent the _cls field will not be stored in the document
        indexes = []  # TODO


class Classifier(MongoModel):
    # Static
    image = fields.CharField()  # docker image name (used in docker pull)
    file_formats = fields.ListField(fields.CharField())  # accepted sequence formats
    download = fields.ListField(fields.CharField())  # CLI for downloading database references
    build = fields.ListField(fields.CharField())  # CLI for building databases
    classify = fields.ListField(fields.CharField())  # CLI for running classification
    report = fields.ListField(fields.CharField())  # CLI for generating reports

    # Dynamic
    database_name = fields.CharField()  # parent directory name of database

    def __repr__(self):
        return self.as_dict().__repr__()

    def __str__(self):
        return self.as_dict().__str__()

    def as_dict(self):
        return self.to_son().to_dict()

    def as_json(self):
        return json.dumps(self.as_dict(), separators=(",", ":"), default=json_encoder)  # , cls=SchemaJSONEncoder)

    class Meta:
        collection_name = "Classifier"
        ignore_unknown_fields = True
        final = True  # prevent the _cls field will not be stored in the document
        indexes = []  # TODO


class JobQueue(MongoModel):
    # Static
    job_type = fields.CharField(
        choices=[str(JobType.SIMULATION), str(JobType.CLASSIFICATION), str(JobType.EVALUATION)]
    )
    job_id = fields.ObjectIdField()
    started_datetime = fields.DateTimeField(blank=True)
    created_datetime = fields.DateTimeField() #The time this UserJob was created

    # Dynamic
    queue_position = fields.IntegerField()
    updated_datetime = fields.DateTimeField()

    def __repr__(self):
        return self.as_dict().__repr__()

    def __str__(self):
        return self.as_dict().__str__()

    def as_dict(self):
        return self.to_son().to_dict()

    def as_json(self):
        return json.dumps(self.as_dict(), separators=(",", ":"), default=json_encoder)  # , cls=SchemaJSONEncoder)

    class Meta:
        collection_name = "JobQueue"
        ignore_unknown_fields = True
        final = True  # prevent the _cls field will not be stored in the document
        indexes = []  # TODO
