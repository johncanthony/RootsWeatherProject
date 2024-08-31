from uuid import uuid4
from datetime import datetime
from time import time
from pydantic import BaseModel, Field
from typing import Union, Optional


class ManagedJobModel(BaseModel):
    job_id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    job_status: Union[str, None] = "new"
    job_start_time: Optional[int] = Field(default_factory=lambda: int(time()))
    job_end_time: Union[int, None] = -1
    job_error: Union[str, None] = ''
    img_date: str
    image_links: Union[str, None] = ''
    gif_urn: Union[str, None] = ''
    video_urn: Union[str, None] = ''
    img_resolution: str
    yt_video_id: Union[str, None] = ''
    publish_public: Union[str, None] = ''
    region: str

    class Config:
        orm_mode = True

    def get_formatted_date(self):
        date_str = self.img_date.split("-")
        return datetime(int(date_str[0]), int(date_str[1]), int(date_str[2])).strftime("%Y%j")

    def get_title_date(self):
        date_str = self.img_date.split("-")
        return datetime(int(date_str[0]), int(date_str[1]), int(date_str[2])).strftime("%b %d %Y")