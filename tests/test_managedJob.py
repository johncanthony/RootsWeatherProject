from ManagerAPI.api.models.managedJob import ManagedJobModel


def test_all_model_class_variables_are_int_or_string_type():

    testjobModel = ManagedJobModel(img_date="2024-01-12", img_resolution="1250x750", region="CONUS")
    print(testjobModel)
    for key, value in testjobModel.__dict__.items():
        assert type(value) in [str, int]
