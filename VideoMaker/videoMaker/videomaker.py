from LogHandler.logHandler import LogHandler
from JobHandler.jobHandler import JobHandler
from ManagerAPI.api.models.managedJob import ManagedJobModel
from VideoMaker.videoMaker.managers.video_manager import VideoBase, VideoManager, ShortsVideoManager

from time import sleep
import logging as log


def create_video(job: ManagedJobModel):

    log.info(f'Creating video for job: {job.job_id}')
    job_resolution = job.job_resolution.split("x")

    if not VideoBase(video_name=str(job.job_id)).input_directory_exists() or not VideoBase(video_name=str(job.job_id)).input_directory_exists():
        log.error(f'No images found for job: {job.job_id}')
        job.job_status = "error"
        job.job_error += f'No images found for job: {job.job_id} ,'
        return

    if job_resolution[0] == job_resolution[1]:
        VideoManager(str(job.job_id)).build()
    else:
        ShortsVideoManager(str(job.job_id)).build()

    return


def run():
    jobHandler = JobHandler("grabbed")
    log.info('Checking for grabbed jobs')

    if not jobHandler.available_job():
        log.debug('No grabbed jobs found')
        return

    new_job = jobHandler.fetch_job()

    if not new_job:
        log.error(f'Failed to fetch job {new_job.job_id}')
        return

    create_video(new_job)

    if new_job.job_status == "error":
        jobHandler.update_job(new_job)
        log.error(f'Updated job {new_job.job_id} with error')
        return

    new_job.job_status = "packed"
    jobHandler.update_job(new_job)

    return


if __name__ == "__main__":

    LogHandler(service_name="videoMaker", log_level="DEBUG", dir="log").bootstrap()
    log.info("Starting VideoMaker service")

    while True:
        sleep(5)
        run()
