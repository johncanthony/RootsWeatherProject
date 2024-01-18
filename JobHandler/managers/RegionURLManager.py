from dataclasses import dataclass


@dataclass
class RegionURLManager:
    alaska: str = "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/SECTOR/ak/GEOCOLOR/"
    central_alaska: str = "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/SECTOR/cak/GEOCOLOR/"
    south_mississippi_valley: str = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/smv/GEOCOLOR/"
    north_mississippi_valley: str = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/umv/GEOCOLOR/"
    pac_west: str = "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/SECTOR/wus/GEOCOLOR/"
    mexico: str = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/mex/GEOCOLOR/"
    conus: str = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/"

    def __getitem__(self, item):
        return getattr(self, item)

    def valid_region(self, region: str):
        return region in self.__dict__.keys()
