
from ManagerAPI.api.managers.state_manager import StateManager
from ManagerAPI.api.models.managedJob import ManagedJobModel
from time import time
import requests
import logging as log
import os

BASE_JOB_HANDLER_URL = os.getenv('MANAGERAPI_BASE_URL', 'http://localhost:8000/')
MAX_JOB_RETRY_COUNT = os.getenv('MAX_JOB_RETRY_COUNT',5)

class JobHandler:

    stateManager = StateManager()
    baseConnectionURL = BASE_JOB_HANDLER_URL
    maxJobRetryCount = MAX_JOB_RETRY_COUNT

    def __init__(self, job_queue: str):
        self.job_queue = job_queue

    def available_job(self) -> bool:

        try:
            jobs = requests.get(self.baseConnectionURL + "jobs").json()
        except requests.exceptions.ConnectionError:
            log.error(f'[Job Handler] Failed to fetch jobs from {self.baseConnectionURL + "jobs"} for {self.job_queue}')
            return False
        except requests.exceptions.ReadTimeout:
            log.error(f'[Job Handler] Timeout fetching jobs from {self.baseConnectionURL + "jobs"} for {self.job_queue}')
            return False

        log.debug(f'Fetched {self.stateManager[self.job_queue]} available jobs - current count {len(jobs[self.stateManager[self.job_queue]])}')

        return (jobs and len(jobs[self.stateManager[self.job_queue]]) > 0)

    def fetch_job(self):

        try:
            job_query = requests.get(self.baseConnectionURL + "job/queue/" + self.job_queue)
        except requests.exceptions.ConnectionError:
            log.error(f'[Job Handler] Failed to fetch job from {self.baseConnectionURL + "job/queue/" + self.job_queue}')
            return None
        except requests.exceptions.ReadTimeout:
            log.error(f'[Job Handler] Timeout fetching job from {self.baseConnectionURL + "job/queue/" + self.job_queue}')
            return None

        if job_query.status_code != 200:
            return None

        log.debug(f'Fetched job {job_query.json()[self.job_queue]} from {self.baseConnectionURL + "job/queue/" + self.job_queue}')

        return ManagedJobModel(**job_query.json()[self.job_queue])

    def fetch_job_by_id(self, jobid):

        try:
            job_query = requests.get(self.baseConnectionURL + "job/id/" + jobid)
        except requests.exceptions.ConnectionError:
            log.error(f'[Job Handler] Failed to fetch job {self.baseConnectionURL + "job/id/" + jobid}')
            return None
        except requests.exceptions.ReadTimeout:
            log.error(f'[Job Handler] Timeout fetching job {self.baseConnectionURL + "job/id/" + jobid}')
            return None
        except requests.exceptions.HTTPError:
            log.error(f'[Job Handler] Request failed with HTTP ERROR {job_query.status_code} for {self.baseConnectionURL + "job/id/" + jobid}')

        return ManagedJobModel(**job_query.json())

    def update_job(self, job):

        log.debug(f'Attempting to update job {job.job_id} to {self.baseConnectionURL + "job"}')

        try:
            job_update = requests.post(self.baseConnectionURL + "job", json=job.model_dump())
        except requests.exceptions.ConnectionError:
            log.error(f'[Job Handler] Failed to update job {job.job_id} to {self.baseConnectionURL + "job"}')
            return False
        except requests.exceptions.ReadTimeout:
            log.error(f'[Job Handler] Timeout updating job {job.job_id} to {self.baseConnectionURL + "job"}')
            return False

        if job_update.status_code != 200:
            return False

        log.debug(f'Updated job {job.job_id} to {self.baseConnectionURL + "job"}')

        return True

    def error_job(self, job, error_message: str):

        if int(job.retries) < self.maxJobRetryCount:
            self.retry_job(job, error_message)
            return True

        job.job_error = error_message
        job.job_end_time = int(time())
        job.job_status = "error"

        self.update_job(job)

        log.debug(f'Error status set for job {job.job_id}')

        return True

    def retry_job(self,job, error_message: str ):

        job.retries = str(int(job.retries) + 1)
        job.job_error = f'Retry Error: {error_message}'

        self.update_job(job)

        log.debug(f'Job: {job.job_id} set for retry : {job.retries} ')

        return True
