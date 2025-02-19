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
        start_time="0500",
        end_time="0600",
        event_x_event_types=[
            EventType_x_Event(event_type_id=4),
        ],
        recurrence_pattern=Event_Cadence.weekly,
        day_of_week=Day_Of_Week.monday,
        recurrence_interval=1,
        index_within_interval=1,
        name="Test Event",
    )
    update_dict = event.__dict__
    DbManager.update_records(Event, [Event.id == 3], update_dict)

    # with get_session() as session:
    #     # delete event_x_event_types
    #     session.query(EventType_x_Event).filter(
    #         EventType_x_Event.event_id == 3
    #     ).delete()
    #     # add event_x_event_types
    #     session.add(EventType_x_Event(event_id=3, event_type_id=4))
    #     session.commit()


if __name__ == "__main__":
    test_update_event()
