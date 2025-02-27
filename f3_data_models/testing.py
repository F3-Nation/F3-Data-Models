from f3_data_models.models import Event, Day_Of_Week, Event_Cadence, EventType_x_Event
import datetime
from f3_data_models.utils import DbManager


def test_update_event():
    event = Event(
        org_id=3,
        location_id=2,
        is_series=True,
        is_active=True,
        highlight=True,
        start_date=datetime.date(2025, 2, 17),
        end_date=datetime.date(2026, 2, 17),
        start_time="0400",
        end_time="0600",
        event_x_event_types=[
            EventType_x_Event(event_type_id=3),
        ],
        recurrence_pattern=Event_Cadence.weekly,
        day_of_week=Day_Of_Week.monday,
        recurrence_interval=1,
        index_within_interval=1,
        name="Test Event",
    )
    update_dict = event.to_update_dict()
    DbManager.update_record(Event, 3, update_dict)

    # event = DbManager.get(Event, 3)
    DbManager.delete_records(Event, [Event.series_id == 3])


if __name__ == "__main__":
    test_update_event()
