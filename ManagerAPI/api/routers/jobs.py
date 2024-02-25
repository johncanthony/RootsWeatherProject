from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ManagerAPI.api.managers.job_manager import JobManager
from ManagerAPI.api.models.managedJob import ManagedJobModel
from ManagerAPI.api.managers.state_manager import StateManager
from ManagerAPI.api.managers.connection_manager import RedisConnectionConfig
import logging

log = logging.getLogger('uvicorn')

jobRouter = APIRouter()
jobManager = JobManager(RedisConnectionConfig(), StateManager())


@jobRouter.get('/jobs', tags=['jobs'])
async def get_jobs():
    queued_jobs = {}

    for queue in jobManager.stateManager.states():
        log.debug(f'Getting jobs from queue {queue} - {jobManager.stateManager[queue]}')
        queued_jobs[jobManager.stateManager[queue]] = jobManager.get_jobs_from_state(queue=queue)

    return queued_jobs


@jobRouter.get('/job/id/{job_id}', tags=['jobs'])
async def get_job(job_id):

    job = jobManager.get_job(job_id=job_id)
    if job is None:
        log.error(f'Job {job_id} not found')
        raise HTTPException(status_code=404, detail='Job not found')

    return job.model_dump()


@jobRouter.post('/job', tags=['jobs'])
async def update_job(job: ManagedJobModel):

    log.info(f'Updating job: {job.model_dump()}')

    if not jobManager.update_job(job=job):
        log.error(f'Failed to update job {job.job_id}')
        raise HTTPException(status_code=500, detail='Failed to update job')

    return job.model_dump()


@jobRouter.delete('/job/id/{job_id}', tags=['jobs'])
async def delete_job(job_id, force: bool = False):

    if not jobManager.get_job(job_id=job_id):
        log.error(f'Job {job_id} not found')
        raise HTTPException(status_code=404, detail='Job not found')

    if not jobManager.delete_job(job_id=job_id, force=force):
        log.error(f'Failed to delete job {job_id}')
        raise HTTPException(status_code=500, detail='Failed to delete job from Redis')

    return {'Deleted': job_id}


@jobRouter.get('/job/queue/{queue}', tags=['jobs'])
async def get_jobs_from_queue(queue):

    job_id = jobManager.get_job_from_queue(queue=queue)

    if job_id is None:
        log.error(f'No jobs in queue {queue}')
        raise HTTPException(status_code=404, detail='No jobs in queue')

    return {queue: job_id}


@jobRouter.get('/job/id/{job_id}/status', tags=['jobs'])
async def get_job_status(job_id):

    job = jobManager.get_job(job_id=job_id)

    if job is None:
        log.error(f'Job {job_id} not found')
        raise HTTPException(status_code=404, detail='Job not found')

    return {'status': job.job_status}


@jobRouter.get('/job/id/{job_id}/video', tags=['jobs'])
async def get_job_video(job_id):

    job = jobManager.get_job(job_id=job_id)

    if job is None:
        log.error(f'Job {job_id} not found')
        raise HTTPException(status_code=404, detail='Job not found')

    if job.job_status == "error":
        log.error(f'Job {job_id} errored before video creation')
        raise HTTPException(status_code=404, detail='Job errored before video creation')

    if job.job_status not in ["packed", "uploaded", "completed"]:
        log.error(f'Job {job_id} video not packed')
        raise HTTPException(status_code=404, detail='Video not created yet')

    if not job.video_urn:
        log.error(f'Job {job_id} video not found')
        raise HTTPException(status_code=404, detail='Video is expected, but not found')

    return FileResponse(job.video_urn)
