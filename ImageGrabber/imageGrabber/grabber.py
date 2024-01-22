from JobHandler.jobHandler import JobHandler
from JobHandler.managers.RegionURLManager import RegionURLManager
from LogHandler.logHandler import LogHandler
from ManagerAPI.api.models.managedJob import ManagedJobModel

import logging as log
from time import sleep
import requests
import os
import threading


'''
Iterate over the image links and download the images to the attached longhorn volume at /images
'''


def grab_images(job: ManagedJobModel, request_base_url: str, request_timeout: int = 10, max_threads: int = 10):

    log.info(f'Grabbing images for job: {job.job_id}')

    IMAGE_DIR = os.getenv("IMAGE_DESTINATION", "./images")

    IMAGE_DESTINATION = f'{IMAGE_DIR}/{job.job_id}/'
    if not os.path.exists(IMAGE_DESTINATION):
        os.makedirs(IMAGE_DESTINATION)

    def download_image(image_name):
        url = request_base_url + image_name
        filename = IMAGE_DESTINATION + image_name

        try:
            response = requests.get(url, timeout=request_timeout)
        except requests.exceptions.ConnectionError as err:
            log.error(f'[HTTP Connection] Unable to fetch image: [{job.job_id}] {image_name} - {err}')
            job.job_status = "error"
            job.job_error += f'Unable to fetch image: {image_name} - {err} ,'
            return
        except requests.exceptions.ReadTimeout as err:
            log.error(f'[HTTP Timeout] Unable to fetch image: [{job.job_id}] {image_name} - {err}')
            job.job_status = "error"
            job.job_error += f'Timed out fetching image: {image_name} - {err} ,'
            return

        with open(filename, 'wb') as f:
            f.write(response.content)

    threads = []

    for image_name in job.image_links.split(","):
        thread = threading.Thread(target=download_image, args=(image_name,))
        threads.append(thread)
        thread.start()

        if len(threads) >= max_threads:
            for thread in threads:
                thread.join()
            threads = []

    return


def run():

    jobHandler = JobHandler("imgresolved")
    regionalURLManager = RegionURLManager()

    log.info('Checking for new jobs')

    if not jobHandler.available_job():
        log.debug('No new jobs found')
        return

    new_job = jobHandler.fetch_job()

    if not new_job:
        log.error(f'Failed to fetch job {new_job.job_id}')
        return

    log.info(f'Fetched job {new_job.job_id}')

    if not regionalURLManager.valid_region(new_job.region):
        jobHandler.error_job(new_job, f'Invalid region: {new_job.region}')
        log.error(f'Invalid region: {new_job.region}')
        return

    grab_images(job=new_job, request_base_url=regionalURLManager[new_job.region])

    if new_job.job_status == "error":
        jobHandler.update_job(new_job)
        log.error(f'Updated job {new_job.job_id} with error')
        return

    new_job.job_status = "grabbed"
    jobHandler.update_job(new_job)
    log.debug(f'Updated job {new_job.job_id} with image links')

    return


def launch():

    LogHandler(service_name="imageGrabber").bootstrap()
    log.info('[BOOT] Starting image grabber')

    while True:
        sleep(5)
        run()


if __name__ == "__main__":

    launch()
