
from ManagerAPI.api.managers.state_manager import StateManager
from ManagerAPI.api.models.managedJob import ManagedJobModel
from time import time
import requests


class JobHandler:

    stateManager = StateManager()
    baseConnectionURL = "http://localhost:8000/"

    def __init__(self, job_queue: str):
        self.job_queue = job_queue

    def available_job(self) -> bool:

        try:
            jobs = requests.get(self.baseConnectionURL + "jobs").json()
        except requests.exceptions.ConnectionError:
            return False

        return (jobs and len(jobs[self.stateManager[self.job_queue]]) > 0)

    def fetch_job(self):

        try:
            job_query = requests.get(self.baseConnectionURL + "job/queue/" + self.job_queue)
        except requests.exceptions.ConnectionError:
            return None

        if job_query.status_code != 200:
            return None

        return ManagedJobModel(**job_query.json()[self.job_queue])

    def update_job(self, job):

        try:
            job_update = requests.post(self.baseConnectionURL + "job", json=job.model_dump())
        except requests.exceptions.ConnectionError:
            return False

        if job_update.status_code != 200:
            return False

        return True

    def error_job(self, job, error_message: str):

        job.job_error = error_message
        job.job_end_time = int(time())
        job.job_status = "error"

        self.update_job(job)

        return True
