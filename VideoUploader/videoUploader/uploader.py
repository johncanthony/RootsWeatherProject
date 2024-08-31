from LogHandler.logHandler import LogHandler
from JobHandler.jobHandler import JobHandler
from ManagerAPI.api.models.managedJob import ManagedJobModel
from VideoUploader.videoUploader.managers.upload_manager import YTAuthManager, YTVideoManager
from time import sleep, time
import logging as log


def get_video_type(job: ManagedJobModel):

    resolution = job.img_resolution.split("x")

    if resolution[0] == resolution[1]:
        return "shorts"

    return "normal"


def get_title(job: ManagedJobModel):
    title_base = f'{job.region.replace("_", " ").upper()} {job.get_title_date()} - 24 Hour Timelapse'
    title_base_shorts = f'{job.region.replace("_", " ").title()} {job.get_title_date()} Weather Timelapse #weathertoday'

    if get_video_type(job) == "shorts":
        return title_base_shorts

    return title_base


def publish_privacy_status(job: ManagedJobModel):
    if job.publish_public:
        return "public"

    return "private"


def get_description(job: ManagedJobModel):
    
    description = f' Timelapse of the {job.region.replace("_", " ").title()} weather for {job.get_title_date()} \n Imagery credit to NOAA / NESDIS Center for Satellite Applications and Research.'
    log.debug(f"Attached Description for {job.job_id} - Description: {description}")
    return description


def upload_video(job: ManagedJobModel):
    log.debug(f'Uploading video for job: {job.job_id}')

    ytAuthManager = YTAuthManager().bootstrap()
    ytVideoManager = YTVideoManager(title=get_title(job=job),
                                    description=get_description(job=job),
                                    video_type=get_video_type(job=job),
                                    privacy_status=publish_privacy_status(job=job),
                                    video_file=job.video_urn,
                                    auth_manager=ytAuthManager)

    video_id = ytVideoManager.upload_video(ytAuthManager.fetch_credentials())
    log.info(f'Uploaded video {video_id}')

    if not video_id:
        log.error(f'Failed to upload video for job: {job.job_id}')
        job.job_status = "error"
        job.job_error += f'Failed to upload video {job.job_id}'
        return False

    job.yt_video_id = video_id

    return video_id


def run():

    jobHandler = JobHandler("packed")

    if not jobHandler.available_job():
        log.info('No jobs available')
        return

    job = jobHandler.fetch_job()

    if not job:
        log.info('No jobs available')
        return

    log.info(f'Processing job: {job.job_id}')
    upload_video(job=job)

    if job.job_status == "error":
        log.error(f'Job {job.job_id} failed')
        jobHandler.error_job(job, "Job failed")
        return

    job.job_status = "uploaded"
    job.job_end_time = int(time())
    jobHandler.update_job(job)


def launch():

    LogHandler(service_name="videoUploader").bootstrap()
    log.info('[Boot] Starting video uploader')

    while True:
        sleep(5)
        run()


if __name__ == "__main__":

    launch()
