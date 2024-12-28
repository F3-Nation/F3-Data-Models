from datetime import datetime, date, time
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    JSON,
    TEXT,
    TIME,
    VARCHAR,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    func,
    UniqueConstraint,
)
from typing_extensions import Annotated
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    relationship,
)

# Custom Annotations
time_notz = Annotated[time, TIME]
text = Annotated[str, TEXT]
intpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
dt_create = Annotated[
    datetime, mapped_column(DateTime, server_default=func.timezone("utc", func.now()))
]
dt_update = Annotated[
    datetime,
    mapped_column(
        DateTime,
        server_default=func.timezone("utc", func.now()),
        server_onupdate=func.timezone("utc", func.now()),
    ),
]


class Base(DeclarativeBase):
    """
    Base class for all models, providing common methods.

    Methods:
        get_id: Get the primary key of the model.
        get: Get the value of a specified attribute.
        to_json: Convert the model instance to a JSON-serializable dictionary.
        __repr__: Get a string representation of the model instance.
        _update: Update the model instance with the provided fields.
    """

    type_annotation_map = {
        Dict[str, Any]: JSON,
    }

    def get_id(self):
        """
        Get the primary key of the model.

        Returns:
            int: The primary key of the model.
        """
        return self.id

    def get(self, attr):
        """
        Get the value of a specified attribute.

        Args:
            attr (str): The name of the attribute.

        Returns:
            Any: The value of the attribute if it exists, otherwise None.
        """
        if attr in [c.key for c in self.__table__.columns]:
            return getattr(self, attr)
        return None

    def to_json(self):
        """
        Convert the model instance to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary representation of the model instance.
        """
        return {
            c.key: self.get(c.key)
            for c in self.__table__.columns
            if c.key not in ["created", "updated"]
        }

    def __repr__(self):
        """
        Get a string representation of the model instance.

        Returns:
            str: A string representation of the model instance.
        """
        return str(self.to_json())

    def _update(self, fields):
        """
        Update the model instance with the provided fields.

        Args:
            fields (dict): A dictionary of fields to update.

        Returns:
            Base: The updated model instance.
        """
        for k, v in fields.items():
            attr_name = str(k).split(".")[-1]
            setattr(self, attr_name, v)
        return self


class SlackSpace(Base):
    """
    Model representing a Slack workspace.

    Attributes:
        id (int): Primary Key of the model.
        team_id (str): The Slack-internal unique identifier for the Slack team.
        workspace_name (Optional[str]): The name of the Slack workspace.
        bot_token (Optional[str]): The bot token for the Slack workspace.
        settings (Optional[Dict[str, Any]]): Slack Bot settings for the Slack workspace.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "slack_spaces"

    id: Mapped[intpk]
    team_id: Mapped[str] = mapped_column(VARCHAR, unique=True)
    workspace_name: Mapped[Optional[str]]
    bot_token: Mapped[Optional[str]]
    settings: Mapped[Optional[Dict[str, Any]]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class OrgType(Base):
    """
    Model representing an organization type / level. 1=AO, 2=Region, 3=Area, 4=Sector

    Attributes:
        id (int): Primary Key of the model.
        name (str): The name of the organization type.
        description (Optional[text]): A description of the organization type.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "org_types"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[Optional[text]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class EventCategory(Base):
    """
    Model representing an event category. These are immutable cateogies that we will define at the Nation level.

    Attributes:
        id (int): Primary Key of the model.
        name (str): The name of the event category.
        description (Optional[text]): A description of the event category.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "event_categories"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[Optional[text]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class Role(Base):
    """
    Model representing a role. A role is a set of permissions that can be assigned to users.

    Attributes:
        id (int): Primary Key of the model.
        name (str): The name of the role.
        description (Optional[text]): A description of the role.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "roles"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[Optional[text]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class Permission(Base):
    """
    Model representing a permission.

    Attributes:
        id (int): Primary Key of the model.
        name (str): The name of the permission.
        description (Optional[text]): A description of the permission.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "permissions"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[Optional[text]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class Role_x_Permission(Base):
    """
    Model representing the assignment of permissions to roles.

    Attributes:
        role_id (int): The ID of the associated role.
        permission_id (int): The ID of the associated permission.
    """

    __tablename__ = "roles_x_permissions"

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id"), primary_key=True
    )


class Role_x_User_x_Org(Base):
    """
    Model representing the assignment of roles, users, and organizations.

    Attributes:
        role_id (int): The ID of the associated role.
        user_id (int): The ID of the associated user.
        org_id (int): The ID of the associated organization.
    """

    __tablename__ = "roles_x_users_x_org"

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"), primary_key=True)


class Org(Base):
    """
    Model representing an organization. The same model is used for all levels of organization (AOs, Regions, etc.).

    Attributes:
        id (int): Primary Key of the model.
        parent_id (Optional[int]): The ID of the parent organization.
        org_type_id (int): The ID of the organization type.
        default_location_id (Optional[int]): The ID of the default location.
        name (str): The name of the organization.
        description (Optional[text]): A description of the organization.
        is_active (bool): Whether the organization is active.
        logo_url (Optional[str]): The URL of the organization's logo.
        website (Optional[str]): The organization's website.
        email (Optional[str]): The organization's email.
        twitter (Optional[str]): The organization's Twitter handle.
        facebook (Optional[str]): The organization's Facebook page.
        instagram (Optional[str]): The organization's Instagram handle.
        last_annual_review (Optional[date]): The date of the last annual review.
        meta (Optional[Dict[str, Any]]): Additional metadata for the organization.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.

        event_types (Optional[List[EventType]]): The event types associated with the organization. Used to control which event types are available for selection at the region level.
        event_tags (Optional[List[EventTag]]): The event tags associated with the organization. Used to control which event tags are available for selection at the region level.
        achievements (Optional[List[Achievement]]): The achievements available within the organization.
        parent_org (Optional[Org]): The parent organization.
    """

    __tablename__ = "orgs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("orgs.id"))
    org_type_id: Mapped[int] = mapped_column(ForeignKey("org_types.id"))
    default_location_id: Mapped[Optional[int]]
    name: Mapped[str]
    description: Mapped[Optional[text]]
    is_active: Mapped[bool]
    logo_url: Mapped[Optional[str]]
    website: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    twitter: Mapped[Optional[str]]
    facebook: Mapped[Optional[str]]
    instagram: Mapped[Optional[str]]
    last_annual_review: Mapped[Optional[date]]
    meta: Mapped[Optional[Dict[str, Any]]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]

    event_types: Mapped[Optional[List["EventType"]]] = relationship(
        "EventType", secondary="event_types_x_org", cascade="expunge"
    )
    event_tags: Mapped[Optional[List["EventTag"]]] = relationship(
        "EventTag", secondary="event_tags_x_org", cascade="expunge"
    )
    achievements: Mapped[Optional[List["Achievement"]]] = relationship(
        "Achievement", secondary="achievements_x_org", cascade="expunge"
    )
    parent_org: Mapped[Optional["Org"]] = relationship(
        "Org", remote_side=[id], cascade="expunge"
    )


class EventType(Base):
    """
    Model representing an event type. Event types can be shared by regions or not, and should roll up into event categories.

    Attributes:
        id (int): Primary Key of the model.
        name (str): The name of the event type.
        description (Optional[text]): A description of the event type.
        acronym (Optional[str]): Acronyms associated with the event type.
        category_id (int): The ID of the associated event category.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "event_types"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[Optional[text]]
    acronym: Mapped[Optional[str]]
    category_id: Mapped[int] = mapped_column(ForeignKey("event_categories.id"))
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class EventType_x_Event(Base):
    """
    Model representing the association between events and event types. The intention is that a single event can be associated with multiple event types.

    Attributes:
        event_id (int): The ID of the associated event.
        event_type_id (int): The ID of the associated event type.

        event (Event): The associated event.
    """

    __tablename__ = "events_x_event_types"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)
    event_type_id: Mapped[int] = mapped_column(
        ForeignKey("event_types.id"), primary_key=True
    )

    event: Mapped["Event"] = relationship(back_populates="event_x_event_types")


class EventType_x_Org(Base):
    """
    Model representing the association between event types and organizations. This controls which event types are available for selection at the region level, as well as default types for each AO.

    Attributes:
        event_type_id (int): The ID of the associated event type.
        org_id (int): The ID of the associated organization.
        is_default (bool): Whether this is the default event type for the organization. Default is False.
    """

    __tablename__ = "event_types_x_org"

    event_type_id: Mapped[int] = mapped_column(
        ForeignKey("event_types.id"), primary_key=True
    )
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"), primary_key=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)


class EventTag(Base):
    """
    Model representing an event tag. These are used to mark special events, such as anniversaries or special workouts.

    Attributes:
        id (int): Primary Key of the model.
        name (str): The name of the event tag.
        description (Optional[text]): A description of the event tag.
        color (Optional[str]): The color used for the calendar.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "event_tags"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[Optional[text]]
    color: Mapped[Optional[str]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class EventTag_x_Event(Base):
    """
    Model representing the association between event tags and events. The intention is that a single event can be associated with multiple event tags.

    Attributes:
        event_id (int): The ID of the associated event.
        event_tag_id (int): The ID of the associated event tag.

        event (Event): The associated event.
    """

    __tablename__ = "event_tags_x_events"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)
    event_tag_id: Mapped[int] = mapped_column(
        ForeignKey("event_tags.id"), primary_key=True
    )

    event: Mapped["Event"] = relationship(back_populates="event_x_event_tags")


class EventTag_x_Org(Base):
    """
    Model representing the association between event tags and organizations. Controls which event tags are available for selection at the region level.

    Attributes:
        event_tag_id (int): The ID of the associated event tag.
        org_id (int): The ID of the associated organization.
        color_override (Optional[str]): The calendar color override for the event tag (if the region wants to use something other than the default).
    """

    __tablename__ = "event_tags_x_org"

    event_tag_id: Mapped[int] = mapped_column(
        ForeignKey("event_tags.id"), primary_key=True
    )
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"), primary_key=True)
    color_override: Mapped[Optional[str]]


class Org_x_SlackSpace(Base):
    """
    Model representing the association between organizations and Slack workspaces. This is currently meant to be one to one, but theoretically could support multiple workspaces per organization.

    Attributes:
        org_id (int): The ID of the associated organization.
        slack_space_id (str): The ID of the associated Slack workspace.
    """

    __tablename__ = "orgs_x_slack_spaces"

    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"), primary_key=True)
    slack_space_id: Mapped[int] = mapped_column(
        ForeignKey("slack_spaces.id"), primary_key=True
    )


class Location(Base):
    """
    Model representing a location. Locations are expected to belong to a single organization (region).

    Attributes:
        id (int): Primary Key of the model.
        org_id (int): The ID of the associated organization.
        name (str): The name of the location.
        description (Optional[text]): A description of the location.
        is_active (bool): Whether the location is active.
        lat (Optional[float]): The latitude of the location.
        lon (Optional[float]): The longitude of the location.
        address_street (Optional[str]): The street address of the location.
        address_city (Optional[str]): The city of the location.
        address_state (Optional[str]): The state of the location.
        address_zip (Optional[str]): The ZIP code of the location.
        address_country (Optional[str]): The country of the location.
        meta (Optional[Dict[str, Any]]): Additional metadata for the location.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "locations"

    id: Mapped[intpk]
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    name: Mapped[str]
    description: Mapped[Optional[text]]
    is_active: Mapped[bool]
    lat: Mapped[Optional[float]]
    lon: Mapped[Optional[float]]
    address_street: Mapped[Optional[str]]
    address_city: Mapped[Optional[str]]
    address_state: Mapped[Optional[str]]
    address_zip: Mapped[Optional[str]]
    address_country: Mapped[Optional[str]]
    meta: Mapped[Optional[Dict[str, Any]]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class Event(Base):
    """
    Model representing an event or series; the same model is used for both with a self-referential relationship for series.

    Attributes:
        id (int): Primary Key of the model.
        org_id (int): The ID of the associated organization.
        location_id (Optional[int]): The ID of the associated location.
        series_id (Optional[int]): The ID of the associated event series.
        is_series (bool): Whether this record is a series or single occurrence. Default is False.
        is_active (bool): Whether the event is active. Default is True.
        highlight (bool): Whether the event is highlighted. Default is False.
        start_date (date): The start date of the event.
        end_date (Optional[date]): The end date of the event.
        start_time (Optional[time_notz]): The start time of the event.
        end_time (Optional[time_notz]): The end time of the event.
        day_of_week (Optional[int]): The day of the week of the event. (0=Monday, 6=Sunday)
        name (str): The name of the event.
        description (Optional[text]): A description of the event.
        recurrence_pattern (Optional[str]): The recurrence pattern of the event. Current options are 'weekly' or 'monthly'.
        recurrence_interval (Optional[int]): The recurrence interval of the event (e.g. every 2 weeks).
        index_within_interval (Optional[int]): The index within the recurrence interval. (e.g. 2nd Tuesday of the month).
        pax_count (Optional[int]): The number of participants.
        fng_count (Optional[int]): The number of first-time participants.
        preblast (Optional[text]): The pre-event announcement.
        backblast (Optional[text]): The post-event report.
        preblast_rich (Optional[Dict[str, Any]]): The rich text pre-event announcement (e.g. Slack message).
        backblast_rich (Optional[Dict[str, Any]]): The rich text post-event report (e.g. Slack message).
        preblast_ts (Optional[float]): The Slack post timestamp of the pre-event announcement.
        backblast_ts (Optional[float]): The Slack post timestamp of the post-event report.
        meta (Optional[Dict[str, Any]]): Additional metadata for the event.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.

        org (Org): The associated organization.
        location (Location): The associated location.
        event_types (List[EventType]): The associated event types.
        event_tags (Optional[List[EventTag]]): The associated event tags.
        event_x_event_types (List[EventType_x_Event]): The association between the event and event types.
        event_x_event_tags (Optional[List[EventTag_x_Event]]): The association between the event and event tags.
    """

    __tablename__ = "events"

    id: Mapped[intpk]
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey("locations.id"))
    series_id: Mapped[Optional[int]] = mapped_column(ForeignKey("events.id"))
    is_series: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    highlight: Mapped[bool] = mapped_column(Boolean, default=False)
    start_date: Mapped[date]
    end_date: Mapped[Optional[date]]
    start_time: Mapped[Optional[time_notz]]
    end_time: Mapped[Optional[time_notz]]
    day_of_week: Mapped[Optional[int]]
    name: Mapped[str]
    description: Mapped[Optional[text]]
    recurrence_pattern: Mapped[Optional[str]]
    recurrence_interval: Mapped[Optional[int]]
    index_within_interval: Mapped[Optional[int]]
    pax_count: Mapped[Optional[int]]
    fng_count: Mapped[Optional[int]]
    preblast: Mapped[Optional[text]]
    backblast: Mapped[Optional[text]]
    preblast_rich: Mapped[Optional[Dict[str, Any]]]
    backblast_rich: Mapped[Optional[Dict[str, Any]]]
    preblast_ts: Mapped[Optional[float]]
    backblast_ts: Mapped[Optional[float]]
    meta: Mapped[Optional[Dict[str, Any]]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]

    org: Mapped[Org] = relationship(innerjoin=True, cascade="expunge", viewonly=True)
    location: Mapped[Location] = relationship(
        innerjoin=True, cascade="expunge", viewonly=True
    )
    event_types: Mapped[List[EventType]] = relationship(
        secondary="events_x_event_types",
        innerjoin=True,
        cascade="expunge",
        viewonly=True,
    )
    event_tags: Mapped[Optional[List[EventTag]]] = relationship(
        secondary="event_tags_x_events", cascade="expunge", viewonly=True
    )
    event_x_event_types: Mapped[List[EventType_x_Event]] = relationship(
        back_populates="event"
    )
    event_x_event_tags: Mapped[Optional[List[EventTag_x_Event]]] = relationship(
        back_populates="event"
    )


class AttendanceType(Base):
    """
    Model representing an attendance type. Basic types are 1='PAX', 2='Q', 3='Co-Q'

    Attributes:
        type (str): The type of attendance.
        description (Optional[str]): A description of the attendance type.
    """

    __tablename__ = "attendance_types"

    id: Mapped[intpk]
    type: Mapped[str]
    description: Mapped[Optional[str]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class Attendance_x_AttendanceType(Base):
    """
    Model representing the association between attendance and attendance types.

    Attributes:
        attendance_id (int): The ID of the associated attendance.
        attendance_type_id (int): The ID of the associated attendance type.

        attendance (Attendance): The associated attendance.
    """

    __tablename__ = "attendance_x_attendance_types"

    attendance_id: Mapped[int] = mapped_column(
        ForeignKey("attendance.id"), primary_key=True
    )
    attendance_type_id: Mapped[int] = mapped_column(
        ForeignKey("attendance_types.id"), primary_key=True
    )

    attendance: Mapped["Attendance"] = relationship(
        back_populates="attendance_x_attendance_types"
    )


class User(Base):
    """
    Model representing a user.

    Attributes:
        id (int): Primary Key of the model.
        f3_name (Optional[str]): The F3 name of the user.
        first_name (Optional[str]): The first name of the user.
        last_name (Optional[str]): The last name of the user.
        email (str): The email of the user.
        phone (Optional[str]): The phone number of the user.
        home_region_id (Optional[int]): The ID of the home region.
        avatar_url (Optional[str]): The URL of the user's avatar.
        meta (Optional[Dict[str, Any]]): Additional metadata for the user.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "users"

    id: Mapped[intpk]
    f3_name: Mapped[Optional[str]]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(VARCHAR, unique=True)
    phone: Mapped[Optional[str]]
    emergency_contact: Mapped[Optional[str]]
    emergency_phone: Mapped[Optional[str]]
    emergency_notes: Mapped[Optional[str]]
    home_region_id: Mapped[Optional[int]] = mapped_column(ForeignKey("orgs.id"))
    avatar_url: Mapped[Optional[str]]
    meta: Mapped[Optional[Dict[str, Any]]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class SlackUser(Base):
    """
    Model representing a Slack user.

    Attributes:
        id (int): Primary Key of the model.
        slack_id (str): The Slack ID of the user.
        user_name (str): The username of the Slack user.
        email (str): The email of the Slack user.
        is_admin (bool): Whether the user is an admin.
        is_owner (bool): Whether the user is the owner.
        is_bot (bool): Whether the user is a bot.
        user_id (Optional[int]): The ID of the associated user.
        avatar_url (Optional[str]): The URL of the user's avatar.
        slack_team_id (str): The ID of the associated Slack team.
        strava_access_token (Optional[str]): The Strava access token of the user.
        strava_refresh_token (Optional[str]): The Strava refresh token of the user.
        strava_expires_at (Optional[datetime]): The expiration time of the Strava token.
        strava_athlete_id (Optional[int]): The Strava athlete ID of the user.
        meta (Optional[Dict[str, Any]]): Additional metadata for the Slack user.
        slack_updated (Optional[datetime]): The last update time of the Slack user.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "slack_users"

    id: Mapped[intpk]
    slack_id: Mapped[str]
    user_name: Mapped[str]
    email: Mapped[str]
    is_admin: Mapped[bool]
    is_owner: Mapped[bool]
    is_bot: Mapped[bool]
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    avatar_url: Mapped[Optional[str]]
    slack_team_id: Mapped[str] = mapped_column(ForeignKey("slack_spaces.team_id"))
    strava_access_token: Mapped[Optional[str]]
    strava_refresh_token: Mapped[Optional[str]]
    strava_expires_at: Mapped[Optional[datetime]]
    strava_athlete_id: Mapped[Optional[int]]
    meta: Mapped[Optional[Dict[str, Any]]]
    slack_updated: Mapped[Optional[datetime]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class Attendance(Base):
    """
    Model representing an attendance record.

    Attributes:
        id (int): Primary Key of the model.
        event_id (int): The ID of the associated event.
        user_id (Optional[int]): The ID of the associated user.
        is_planned (bool): Whether this is planned attendance (True) vs actual attendance (False).
        meta (Optional[Dict[str, Any]]): Additional metadata for the attendance.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.

        event (Event): The associated event.
        user (User): The associated user.
        slack_user (Optional[SlackUser]): The associated Slack user.
        attendance_x_attendance_types (List[Attendance_x_AttendanceType]): The association between the attendance and attendance types.
        attendance_types (List[AttendanceType]): The associated attendance types.
    """

    __tablename__ = "attendance"
    __table_args__ = (UniqueConstraint("event_id", "user_id", "is_planned"),)

    id: Mapped[intpk]
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_planned: Mapped[bool]
    meta: Mapped[Optional[Dict[str, Any]]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]

    event: Mapped[Event] = relationship(
        innerjoin=True, cascade="expunge", viewonly=True
    )
    user: Mapped[User] = relationship(innerjoin=True, cascade="expunge", viewonly=True)
    slack_user: Mapped[Optional[SlackUser]] = relationship(
        innerjoin=False, cascade="expunge", secondary="users", viewonly=True
    )
    attendance_x_attendance_types: Mapped[List[Attendance_x_AttendanceType]] = (
        relationship(back_populates="attendance")
    )
    attendance_types: Mapped[List[AttendanceType]] = relationship(
        secondary="attendance_x_attendance_types",
        innerjoin=True,
        cascade="expunge",
        viewonly=True,
    )


class Achievement(Base):
    """
    Model representing an achievement.

    Attributes:
        id (int): Primary Key of the model.
        name (str): The name of the achievement.
        description (Optional[str]): A description of the achievement.
        verb (str): The verb associated with the achievement.
        image_url (Optional[str]): The URL of the achievement's image.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "achievements"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[Optional[str]]
    verb: Mapped[str]
    image_url: Mapped[Optional[str]]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class Achievement_x_User(Base):
    """
    Model representing the association between achievements and users.

    Attributes:
        achievement_id (int): The ID of the associated achievement.
        user_id (int): The ID of the associated user.
        date_awarded (date): The date the achievement was awarded. Default is the current date.
    """

    __tablename__ = "achievements_x_users"

    achievement_id: Mapped[int] = mapped_column(
        ForeignKey("achievements.id"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    date_awarded: Mapped[date] = mapped_column(
        DateTime, server_default=func.timezone("utc", func.now())
    )


class Achievement_x_Org(Base):
    """
    Model representing the association between achievements and organizations.

    Attributes:
        achievement_id (int): The ID of the associated achievement.
        org_id (int): The ID of the associated organization.
    """

    __tablename__ = "achievements_x_org"

    achievement_id: Mapped[int] = mapped_column(
        ForeignKey("achievements.id"), primary_key=True
    )
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"), primary_key=True)


class Position(Base):
    """
    Model representing a position.

    Attributes:
        name (str): The name of the position.
        description (Optional[str]): A description of the position.
        org_type_id (Optional[int]): The ID of the associated organization type. This is used to limit the positions available to certain types of organizations. If null, the position is available to all organization types.
        org_id (Optional[int]): The ID of the associated organization. This is used to limit the positions available to certain organizations. If null, the position is available to all organizations.
    """

    __tablename__ = "positions"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[Optional[str]]
    org_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("org_types.id"))
    org_id: Mapped[Optional[int]] = mapped_column(ForeignKey("orgs.id"))
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class Position_x_Org_x_User(Base):
    """
    Model representing the association between positions, organizations, and users.

    Attributes:
        position_id (int): The ID of the associated position.
        org_id (int): The ID of the associated organization.
        user_id (int): The ID of the associated user.
    """

    __tablename__ = "positions_x_orgs_x_users"

    position_id: Mapped[int] = mapped_column(
        ForeignKey("positions.id"), primary_key=True
    )
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class Expansion(Base):
    """
    Model representing an expansion.

    Attributes:
        id (int): Primary Key of the model.
        area (str): The area of the expansion.
        pinned_lat (float): The pinned latitude of the expansion.
        pinned_lon (float): The pinned longitude of the expansion.
        user_lat (float): The user's latitude.
        user_lon (float): The user's longitude.
        interested_in_organizing (bool): Whether the user is interested in organizing.
        created (datetime): The timestamp when the record was created.
        updated (datetime): The timestamp when the record was last updated.
    """

    __tablename__ = "expansions"

    id: Mapped[intpk]
    area: Mapped[str]
    pinned_lat: Mapped[float]
    pinned_lon: Mapped[float]
    user_lat: Mapped[float]
    user_lon: Mapped[float]
    interested_in_organizing: Mapped[bool]
    created: Mapped[dt_create]
    updated: Mapped[dt_update]


class Expansion_x_User(Base):
    """
    Model representing the association between expansions and users.

    Attributes:
        expansion_id (int): The ID of the associated expansion.
        user_id (int): The ID of the associated user.
        requst_date (date): The date of the request. Default is the current date.
        notes (Optional[text]): Additional notes for the association.
    """

    __tablename__ = "expansions_x_users"

    expansion_id: Mapped[int] = mapped_column(
        ForeignKey("expansions.id"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    request_date: Mapped[date] = mapped_column(
        DateTime, server_default=func.timezone("utc", func.now())
    )
    notes: Mapped[Optional[text]]


class MagicLinkAuthRecord(Base):
    """
    Model representing a Magic Link Auth Record.

    Attributes:
        id (int): Primary Key of the model.
        email (str): The email of the user.
        otp_hash (bytes): The hash of the OTP.
        created (datetime): The timestamp when the record was created.
        expiration (datetime): The timestamp when the record expires.
        client_ip (str): The client IP address.
        recent_attempts (int): The number of recent attempts.
    """

    __tablename__ = "magiclinkauthrecord"

    id: Mapped[intpk]
    email: Mapped[str]
    otp_hash: Mapped[bytes]
    created: Mapped[dt_create]
    expiration: Mapped[dt_create]
    client_ip: Mapped[str]
    recent_attempts: Mapped[int]


class MagicLinkAuthSession(Base):
    """
    Model representing a Magic Link Auth Session.

    Attributes:
        id (int): Primary Key of the model.
        email (str): The email of the user.
        persistent_id (str): The persistent ID.
        session_token (str): The session token.
        created (datetime): The timestamp when the record was created.
        expiration (datetime): The timestamp when the record expires.
    """

    __tablename__ = "magiclinkauthsession"

    id: Mapped[intpk]
    email: Mapped[str]
    persistent_id: Mapped[str]
    session_token: Mapped[str]
    created: Mapped[dt_create]
    expiration: Mapped[dt_create]


# class Org_x_SlackChannel(Base):
#     """
#     Model representing the association between organizations (specifically AOs) and Slack channels.

#     Attributes:
#         org_id (int): The ID of the associated organization.
#         slack_channel_id (str): The Slack-internal ID of the associated Slack channel.
#     """

#     __tablename__ = "orgs_x_slack_channels"

#     org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"), primary_key=True)
#     slack_channel_id: Mapped[str] = mapped_column(
#         primary_key=True
#     )  # Do we need a slack channel table?
