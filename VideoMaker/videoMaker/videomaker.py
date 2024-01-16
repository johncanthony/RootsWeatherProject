from LogHandler.logHandler import LogHandler
from JobHandler.jobHandler import JobHandler
from ManagerAPI.api.models.managedJob import ManagedJobModel

from time import sleep
import logging as log


def create_video(job: ManagedJobModel):

    log.info(f'Creating video for job: {job.job_id}')
    return


def run():
    jobHandler = JobHandler("grabbed")
    log.info('Checking for grabbed jobs')

    if not jobHandler.available_job():
        log.debug('No grabbed jobs found')
        return

    return


if __name__ == "__main__":

    LogHandler(service_name="videoMaker", log_level="DEBUG", dir="log").bootstrap()
    log.info("Starting VideoMaker service")

    while True:
        sleep(5)
        run()
