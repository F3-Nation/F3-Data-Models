from f3_data_models.models import Location
from f3_data_models.utils import DbManager


def test_update_event():
    DbManager.update_record(
        Location,
        2,
        {
            "name": "The Beach",
            "description": None,
            "is_active": True,
            "latitude": 22.0356,
            "longitude": -159.3377,
            "address_street": None,
            "address_street2": None,
            "address_city": None,
            "address_state": None,
            "address_zip": None,
            "address_country": None,
            "org_id": 5,
        },
    )


if __name__ == "__main__":
    test_update_event()
