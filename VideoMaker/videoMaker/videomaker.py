from LogHandler.logHandler import LogHandler
from JobHandler.jobHandler import JobHandler
from ManagerAPI.api.models.managedJob import ManagedJobModel
from VideoMaker.videoMaker.managers.video_manager import VideoBase, VideoManager, ShortsVideoManager

from time import sleep
import logging as log


def create_video(job: ManagedJobModel):

    log.info(f'Creating video for job: {job.job_id}')
    job_resolution = job.img_resolution.split("x")

    if not VideoBase(video_name=str(job.job_id)).input_directory_exists() or not VideoBase(video_name=str(job.job_id)).input_directory_exists():
        log.error(f'No images found for job: {job.job_id}')
        job.job_status = "error"
        job.job_error += f'No images found for job: {job.job_id} ,'
        return

    log.debug(f'Job resolution: {job_resolution[0]}x{job_resolution[1]}')
    if job_resolution[0] != job_resolution[1]:
        VideoManager(video_name=str(job.job_id)).build()
    else:
        ShortsVideoManager(video_name=str(job.job_id)).build()

    job.job_status = "packed"
    job.video_urn = VideoBase(video_name=str(job.job_id)).output_file

    log.debug(f'Video created :{job.video_urn}')

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

    jobHandler.update_job(new_job)

    return


def launch():

    LogHandler(service_name="videoMaker").bootstrap()
    log.info("[Boot] Starting VideoMaker service")

    while True:
        sleep(5)
        run()


if __name__ == "__main__":

    launch()
