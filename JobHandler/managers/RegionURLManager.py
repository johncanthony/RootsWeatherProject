from dataclasses import dataclass


@dataclass
class RegionURLManager:
    conus: str = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/"
    south_mississippi: str = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/smv/GEOCOLOR/"

    def __getitem__(self, item):
        return getattr(self, item)

    def valid_region(self, region: str):
        return region in self.__dict__.keys()
