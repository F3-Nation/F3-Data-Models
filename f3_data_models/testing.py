from f3_data_models.models import Location
from f3_data_models.utils import DbManager


def test_update_event():
    records = DbManager.find_records(Location, [True])
    print(records)


if __name__ == "__main__":
    test_update_event()
