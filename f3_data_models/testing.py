from f3_data_models.models import User
from f3_data_models.utils import DbManager


def test_update_event():
    user = User(
        email="evan.Petzoldt@protonmail.com",
    )
    DbManager.create_record(user)


if __name__ == "__main__":
    test_update_event()
