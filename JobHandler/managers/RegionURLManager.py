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
    conus_west: str = "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/CONUS/GEOCOLOR/"
    southern_plains: str = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/sp/GEOCOLOR/"
    gulf_of_mexico: str = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/gm/GEOCOLOR/"
    great_lakes: str = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/cgl/GEOCOLOR/"
    northeast: str = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/ne/GEOCOLOR/"
    # Temp link for the hurricane
    beryl: str = "https://cdn.star.nesdis.noaa.gov/FLOATER/AL022024/GEOCOLOR/"

    def __getitem__(self, item):
        return getattr(self, item)

    def valid_region(self, region: str):
        return region in self.__dict__.keys()
