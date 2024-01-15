from uuid import uuid4
from datetime import datetime
from time import time
from pydantic import BaseModel
from typing import Union


class ManagedJobModel(BaseModel):
    job_id: Union[str, None] = str(uuid4())
    job_status: Union[str, None] = "new"
    job_start_time: Union[int, None] = int(time())
    job_end_time: Union[str, None] = ''
    job_error: Union[str, None] = ''
    img_date: str
    image_links: Union[str, None] = ''
    gif_urn: Union[str, None] = ''
    video_urn: Union[str, None] = ''
    img_resolution: str
    yt_video_id: Union[str, None] = ''
    region: str

    class Config:
        orm_mode = True

    def get_formatted_date(self):
        date_str = self.img_date.split("-")
        return datetime(int(date_str[0]), int(date_str[1]), int(date_str[2])).strftime("%Y%j")
