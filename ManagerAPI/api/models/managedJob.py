from uuid import uuid4
from datetime import datetime
from time import time
from pydantic import BaseModel, Field, model_validator, ValidationInfo
from typing import Union, Optional


class ManagedJobModel(BaseModel):
    job_id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    job_status: Union[str, None] = "new"
    job_start_time: Optional[int] = Field(default_factory=lambda: int(time()))
    job_end_time: Union[int, None] = -1
    job_error: Union[str, None] = ''
    #The img_date can be either a single date or comma separated list of dates
    # TODO - Create date validation to match (YEAR-MO-DA)
    img_date: str
    image_links: Union[str, None] = ''
    gif_urn: Union[str, None] = ''
    video_urn: Union[str, None] = ''
    img_resolution: str
    yt_video_id: Union[str, None] = ''
    publish_public: Union[str, None] = ''
    region: str
    storm_id : Union[str,None] = ''
    retries : Union[str,None] = '0'

    class Config:
        orm_mode = True

    #Custom model validation to ensure a storm_id is set if the storm region is set
    @model_validator(mode='after')
    def check_storm_id_present_if_storm_region_set(self):
        region = self.region
        storm_id = self.storm_id

        if region == "storm" and not storm_id:
            raise ValueError("Storm Region set, but no storm id provided")
        
        return self

    def get_formatted_date(self, date):
        date_str = date.split("-")
        return datetime(int(date_str[0]), int(date_str[1]), int(date_str[2])).strftime("%Y%j")

    def get_title_date(self):
        date_str = self.img_date.split("-")
        return datetime(int(date_str[0]), int(date_str[1]), int(date_str[2])).strftime("%b %d %Y")