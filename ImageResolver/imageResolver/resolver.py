from JobHandler.jobHandler import JobHandler
import requests
from time import sleep
from bs4 import BeautifulSoup
import logging as log
from datetime import date


log.basicConfig(filename=f'logs/ImageResolver-service.{date.today()}.log', level=log.INFO, format='%(asctime)s %(levelname)s %(message)s')

'''
Pull the image urls matching the jobs date and resolution from the GOES16 ABI CONUS GEOCOLOR directory
'''


def fetch_NOAA_GOES_image_data(jobHandler, job):

    BASE_URL = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/"
    matched_img_links = []

    log.debug(f'Fetching image for date: {job.img_date} and resolution: {job.img_resolution} from {BASE_URL}')

    try:
        raw_data = requests.get(BASE_URL)
    except requests.exceptions.ConnectionError as err:
        jobHandler.error_job(job, f'Unable to fetch image data: {err}')
        log.error(f'Unable to fetch image data: {err}')
        return matched_img_links

    log.debug('Parsing image data')
    soup = BeautifulSoup(raw_data.content, 'html.parser')
    links = soup.find_all("a")

    matched_img_links = [img_link.get("href") for img_link in links if job.get_formatted_date() in img_link.get("href") and
                         job.img_resolution in img_link.get("href") and "jpg" in img_link.get("href")]

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

    img_urls = fetch_NOAA_GOES_image_data(jobHandler, new_job)
    log.debug(f'Found {len(img_urls)} images for date: {new_job.img_date} and resolution: {new_job.img_resolution}')

    if len(img_urls) == 0:
        jobHandler.error_job(new_job, f'No images found for date: {new_job.img_date} and resolution: {new_job.img_resolution}')
        log.error(f'No images found for date: {new_job.img_date} and resolution: {new_job.img_resolution}')
        return

    new_job.image_links = ",".join(img_urls)
    new_job.job_status = "imgresolved"
    jobHandler.update_job(new_job)
    log.debug(f'Updated job {new_job.job_id} with image links')

    return


if __name__ == "__main__":
    while True:
        sleep(5)
        run()
