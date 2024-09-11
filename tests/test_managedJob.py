from ManagerAPI.api.models.managedJob import ManagedJobModel
import unittest

def test_all_model_class_variables_are_int_or_string_type():

    testjobModel = ManagedJobModel(img_date="2024-01-12", img_resolution="1250x750", region="CONUS")
    print(testjobModel)
    for key, value in testjobModel.__dict__.items():
        assert type(value) in [str, int]


class Storm_Region_Requirement(unittest.TestCase):

    def test_storm_region_with_no_storm_id(self):
        with self.assertRaises(Exception):
            testjobModel = ManagedJobModel(img_date="2024-01-12", img_resolution="2500x1500", region="storm")

    def test_storm_region_with_storm_id(self):
        try:
           testjobModel = ManagedJobModel(img_date="2024-01-12", img_resolution="2500x1500", region="storm",storm_id="AL062024")
        except Exception as e:
            self.fail("test_storm_region_with_storm_id() Unexpectadly raised exception : {}".format(e))

if __name__ == "__main__":
    unittest.main()

    