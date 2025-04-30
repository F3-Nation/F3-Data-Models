from f3_data_models.models import User
from f3_data_models.utils import DbManager


def test_update_event():
    records = DbManager.find_records(User, [User.id == 1], joinedloads=[User.home_region_org])
    print(records)
    print(records[0].home_region_org)


if __name__ == "__main__":
    test_update_event()
