from redis import StrictRedis, exceptions
from ManagerAPI.api.models.managedJob import ManagedJobModel
import logging
import shutil
import os

log = logging.getLogger('uvicorn')


class JobManager:

    def __init__(self, redisConnectionManagerConfig, stateManager):
        self.redis = StrictRedis(host=redisConnectionManagerConfig.host, port=redisConnectionManagerConfig.port, db=redisConnectionManagerConfig.db,
                                 decode_responses=redisConnectionManagerConfig.decode_responses)
        self.stateManager = stateManager

    def update_job(self, job: ManagedJobModel):

        try:
            self.redis.hmset(job.job_id, job.model_dump())
        except exceptions.ConnectionError as e:
            log.error(f'Redis connection issue while updating {job.job_id} : {e}')
            return False

        log.info(f'Adding job {job.job_id} to Redis')

        return self.post_job_to_queue(queue=job.job_status, job_id=job.job_id)

    def get_job(self, job_id: str):

        try:
            job = self.redis.hgetall(job_id)
        except exceptions.ConnectionError as e:
            log.error(f'Redis connection issue while fetching {job_id} : {e}')
            return None

        if not job:
            log.error(f'Job {job_id} not found')
            return None

        log.debug(f'Fetched Job {job_id} : {job}')

        return ManagedJobModel(**job)

    '''
      Gets a list of job ids from a given queue.
    '''
    def get_jobs_from_state(self, queue: str):
        jobs = []

        '''
        Check if queue is valid
        '''
        if not self.stateManager.valid_state(queue):
            return None

        try:
            jobs = self.redis.lrange(self.stateManager[queue], 0, -1)
        except exceptions.ConnectionError as e:
            log.error(f'Redis connection issue while fetching {queue} : {e}')

        return jobs

    def post_job_to_queue(self, queue: str, job_id: str):

        '''
        Check if queue is valid
        '''
        if not self.stateManager.valid_state(queue):
            log.error(f'Invalid queue {queue}')
            return False

        '''
        Check if job is already in queue
        '''
        if job_id in self.get_jobs_from_state(queue=queue):
            log.info(f'Job {job_id} already in queue {queue}')
            return True

        try:
            self.redis.rpush(self.stateManager[queue], job_id)
        except exceptions.ConnectionError:
            return False

        log.info(f'Added job {job_id} to queue {self.stateManager[queue]}')

        return True

    def get_job_from_queue(self, queue: str):

        if not self.stateManager.valid_state(queue):
            return None

        try:
            job_id = self.redis.lpop(self.stateManager[queue])
        except exceptions.ConnectionError:
            return None

        if not job_id:
            return None

        return self.get_job(job_id)

    def delete_job(self, job_id: str, force: bool = False):

        JOB_IMG_VID_DIR = os.getenv('IMAGE_VIDEO_DIR', '/tmp')

        file_path = f'{JOB_IMG_VID_DIR}/{job_id}'
        log.debug(f'Attempting to delete job {job_id} from {file_path}')

        if not force:
            if os.path.exists(file_path):
                shutil.rmtree(file_path)
            else:
                log.error(f'Job {job_id} data not found on disk')
                return False

        '''
        Add block to delete associated job files from disk
        '''
        try:
            self.redis.delete(job_id)
        except exceptions.ConnectionError:
            log.error(f'Failed to delete job {job_id}')
            return False

        log.info(f'Deleted job {job_id}')

        return True
