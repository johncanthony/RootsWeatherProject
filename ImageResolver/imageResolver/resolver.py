from JobHandler.jobHandler import JobHandler
from JobHandler.managers.RegionURLManager import RegionURLManager
from LogHandler.logHandler import LogHandler
from ManagerAPI.api.models.managedJob import ManagedJobModel

import requests
from time import sleep
from bs4 import BeautifulSoup
import logging as log

'''
Pull the image urls matching the jobs date and resolution from the GOES16 ABI CONUS GEOCOLOR directory
'''


def fetch_NOAA_GOES_image_data(jobHandler: JobHandler, job: ManagedJobModel, request_base_url: str):

    matched_img_links = []

    log.debug(f'Fetching image for date: {job.img_date} and resolution: {job.img_resolution} from {request_base_url}')

    try:
        raw_data = requests.get(request_base_url, timeout=10)
    except requests.exceptions.ConnectionError as err:
        jobHandler.error_job(job, f'Unable to fetch image data: {err}')
        log.error(f'Unable to fetch image data: {err}')
        return matched_img_links
    except requests.exceptions.ReadTimeout as err:
        jobHandler.error_job(job, f'Timed out fetching image data: {err}')
        log.error(f'Timed out fetching image urls: {err}')
        return matched_img_links

    log.debug('Parsing image data')
    soup = BeautifulSoup(raw_data.content, 'html.parser')
    links = soup.find_all("a")

    # If the date field has been supplied with a comma separated list of dates, this allows us to iterate over each date to get applicable links
    for date in job.img_date.split(','):
        matched_img_links_date = [img_link.get("href") for img_link in links if job.get_formatted_date(date) in img_link.get("href") and
                                  job.img_resolution in img_link.get("href") and "jpg" in img_link.get("href")]
        matched_img_links = matched_img_links+ matched_img_links_date

    return matched_img_links


def run():

    jobHandler = JobHandler("new")
    log.info('Checking for new jobs')

    if not jobHandler.available_job():
        log.debug('No new jobs found')
        return

    new_job = jobHandler.fetch_job()
    log.info(f'Fetched job {new_job.job_id}')

    if not new_job:
        log.error(f'Failed to fetch job {new_job.job_id}')
        return

    #storm_id needs to be inserted into the RegionURLManager url string if the region is set to storm
    request_base_url = RegionURLManager()[new_job.region]
    if new_job.region == "storm":
        request_base_url = request_base_url.format(new_job.storm_id)
        log.debug(f'Storm region set. Added storm_id : {new_job.storm_id}. Updated URL: {request_base_url}')

    img_urls = fetch_NOAA_GOES_image_data(jobHandler=jobHandler, job=new_job, request_base_url=request_base_url)
    log.debug(f'Found {len(img_urls)} images for date: {new_job.img_date} and resolution: {new_job.img_resolution}')

    if len(img_urls) == 0:
        log.error(f'No images found for date: {new_job.img_date} and resolution: {new_job.img_resolution}')
        log.debug(f'Updating job {new_job.model_dump()} with error')
        jobHandler.error_job(new_job, f'No images found for date: {new_job.img_date} and resolution: {new_job.img_resolution}')
        return

    new_job.image_links = ",".join(img_urls)
    new_job.job_status = "imgresolved"
    jobHandler.update_job(new_job)
    log.debug(f'Updated job {new_job.job_id} with image links')

    return


def launch():

    LogHandler(service_name='resolver').bootstrap()
    log.info('[BOOT] Starting resolver service')

    while True:
        sleep(5)
        run()


if __name__ == "__main__":

    launch()
