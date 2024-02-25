import pytest
from unittest import mock
from JobHandler.jobHandler import JobHandler
from ManagerAPI.api.models.managedJob import ManagedJobModel


@pytest.fixture
def job_handler():
    return JobHandler("new")


def test_available_job(job_handler):
    # Mock the external request
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'jobs:NEW': ['b40df782-9c48-4159-bcc0-fc5cd55e0c82'], 'jobs:IMGRESOLVED': ['b40df782-9c48-4159-bcc0-fc5cd55e0c83'],
                                                   'jobs:GRABBED': ['b40df782-9c48-4159-bcc0-fc5cd55e0c84'], 'jobs:PACKED': ['b40df782-9c48-4159-bcc0-fc5cd55e0c85'],
                                                   'jobs:UPLOADED': ['b40df782-9c48-4159-bcc0-fc5cd55e0c86'], 'jobs:ERROR': ['b40df782-9c48-4159-bcc0-fc5cd55e0c87']}

        # Call the method under test
        status = job_handler.available_job()

        # Assert the expected result
        assert status is True
        mock_get.assert_called_once_with('http://localhost:8000/jobs')


def test_fetch_job_fields(job_handler):
    # Mock the external request
    with mock.patch('requests.get') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "new": {
                "job_id": "efb7f53b-e5a1-4c30-9f45-4b6c116a36ca",
                "job_status": "new",
                "job_start_time": 1705313815,
                "job_end_time": -1,
                "job_error": "",
                "img_date": "2024-01-12",
                "image_links": "",
                "gif_urn": "",
                "video_urn": "",
                "img_resolution": "1250x750",
                "yt_video_id": "",
                "publish_public": "False",
                "region": "CONUS"
                }
            }

        # Call the method under test
        job_id = job_handler.fetch_job()
        assert type(job_id) is ManagedJobModel

        # Assert the expected result
        mock_post.assert_called_once_with('http://localhost:8000/job/queue/new')


def test_update_job(job_handler):

    with mock.patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "new": {
                "job_id": "efb7f53b-e5a1-4c30-9f45-4b6c116a36ca",
                "job_status": "new",
                "job_start_time": 1705313815,
                "job_end_time": -1,
                "job_error": "",
                "img_date": "2024-01-12",
                "image_links": "",
                "gif_urn": "",
                "video_urn": "",
                "img_resolution": "1250x750",
                "yt_video_id": "",
                "publish_public": "False",
                "region": "CONUS"
                }
            }

        mock_job = ManagedJobModel(job_id="efb7f53b-e5a1-4c30-9f45-4b6c116a36ca", job_status="new", job_start_time=1705313815,
                                   job_end_time=-1, job_error="", img_date="2024-01-12", image_links="", gif_urn="", video_urn="",
                                   img_resolution="1250x750", yt_video_id="", region="CONUS")
        job_push = job_handler.update_job(mock_job)

        assert job_push is True
        mock_post.assert_called_once_with('http://localhost:8000/job', json=mock_job.model_dump())
