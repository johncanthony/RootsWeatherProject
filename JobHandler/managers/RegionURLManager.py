from dataclasses import dataclass


@dataclass
class RegionURLManager:
    alaska: str = "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/SECTOR/ak/GEOCOLOR/"
    central_alaska: str = "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/SECTOR/cak/GEOCOLOR/"
    south_mississippi_valley: str = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/smv/GEOCOLOR/"
    north_mississippi_valley: str = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/umv/GEOCOLOR/"
    pac_west: str = "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/SECTOR/wus/GEOCOLOR/"
    mexico: str = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/mex/GEOCOLOR/"
    conus: str = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/"
    conus_west: str = "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/CONUS/GEOCOLOR/"
    southern_plains: str = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/sp/GEOCOLOR/"
    gulf_of_america: str = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/ga/GEOCOLOR/"
    great_lakes: str = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/cgl/GEOCOLOR/"
    northeast: str = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/ne/GEOCOLOR/"
    #Link Template for hurricanes/tropical storms
    # {} is replaced by the STORM ID (example : stormid=AL062024)
    storm: str = "https://cdn.star.nesdis.noaa.gov/FLOATER/{}/GEOCOLOR/"

    def __getitem__(self, item):
        return getattr(self, item)

    def valid_region(self, region: str):
        return region in self.__dict__.keys()
