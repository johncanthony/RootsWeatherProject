from JobHandler.managers.RegionURLManager import RegionURLManager


def test_getitem():
    manager = RegionURLManager()

    regionMap = [("alaska", "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/SECTOR/ak/GEOCOLOR/"),
                 ("central_alaska", "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/SECTOR/cak/GEOCOLOR/"),
                 ("south_mississippi_valley", "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/smv/GEOCOLOR/"),
                 ("north_mississippi_valley", "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/umv/GEOCOLOR/"),
                 ("pac_west", "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/SECTOR/wus/GEOCOLOR/"),
                 ("mexico", "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/mex/GEOCOLOR/"),
                 ("conus", "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/"),
                 ("conus_west", "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/CONUS/GEOCOLOR/"),
                 ("southern_plains", "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/sp/GEOCOLOR/"),
                 ("gulf_of_america", "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/ga/GEOCOLOR/"),
                 ("great_lakes", "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/cgl/GEOCOLOR/"),
                 ("northeast", "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/ne/GEOCOLOR/"),
                 ("storm","https://cdn.star.nesdis.noaa.gov/FLOATER/{}/GEOCOLOR/")]

    for region in regionMap:
        assert manager[region[0]] == region[1]


def test_valid_region():
    manager = RegionURLManager()

    regions = [("alaska", True),
               ("central_alaska", True),
               ("south_mississippi_valley", True),
               ("north_mississippi_valley", True),
               ("pac_west", True), ("conus", True),
               ("mexico", True),("conus_west", True),
               ("southern_plains", True),
               ("gulf_of_america", True),
               ("great_lakes", True),
               ("northeast",True),
               ("storm",True),
               ("invalid_region", False)]

    for region in regions:
        assert manager.valid_region(region[0]) is region[1]
