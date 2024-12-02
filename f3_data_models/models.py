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
    UniqueConstraint,
    func,
)
from typing_extensions import Annotated
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped

# Custom Annotations
time_notz = Annotated[time, TIME]
text = Annotated[str, TEXT]


class Base(DeclarativeBase):
    """
    Base class for all models, providing common fields and methods.

    Attributes:
        id (int): Primary key of the model.
        created (datetime): Timestamp when the model was created.
        updated (datetime): Timestamp when the model was last updated.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # created: Mapped[datetime] = dt_create
    # updated: Mapped[datetime] = dt_update
    created: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.timezone("utc", func.now())
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.timezone("utc", func.now()),
        onupdate=func.timezone("utc", func.now()),
    )

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
        team_id (str): The Slack-internal unique identifier for the Slack team.
        workspace_name (Optional[str]): The name of the Slack workspace.
        bot_token (Optional[str]): The bot token for the Slack workspace.
        settings (Optional[Dict[str, Any]]): Slack Bot settings for the Slack workspace.

        org_x_slack (Org_x_Slack): The organization associated with this Slack workspace.
        org (Org): The organization associated with this Slack workspace.
    """

    __tablename__ = "slack_spaces"

    team_id: Mapped[str] = mapped_column(VARCHAR, unique=True)
    workspace_name: Mapped[Optional[str]]
    bot_token: Mapped[Optional[str]]
    settings: Mapped[Optional[Dict[str, Any]]]

    org_x_slack: Mapped["Org_x_Slack"] = relationship(back_populates="slack_space")
    org: Mapped["Org"] = relationship(
        back_populates="slack_space", secondary="org_x_slack", lazy="joined"
    )


class OrgType(Base):
    """
    Model representing an organization type / level. 1=AO, 2=Region, 3=Area, 4=Sector

    Attributes:
        name (str): The name of the organization type.
        description (Optional[text]): A description of the organization type.
    """

    __tablename__ = "org_types"

    name: Mapped[str]
    description: Mapped[Optional[text]]


class EventCategory(Base):
    """
    Model representing an event category. These are immutable cateogies that we will define at the Nation level.

    Attributes:
        name (str): The name of the event category.
        description (Optional[text]): A description of the event category.
        event_types (List[EventType]): A list of event types associated with this category.
    """

    __tablename__ = "event_categories"

    name: Mapped[str]
    description: Mapped[Optional[text]]

    event_types: Mapped[List["EventType"]] = relationship(
        back_populates="event_category"
    )


class Role(Base):
    """
    Model representing a role. A role is a set of permissions that can be assigned to users.

    Attributes:
        name (str): The name of the role.
        description (Optional[text]): A description of the role.
    """

    __tablename__ = "roles"

    name: Mapped[str]
    description: Mapped[Optional[text]]


class Permission(Base):
    """
    Model representing a permission.

    Attributes:
        name (str): The name of the permission.
        description (Optional[text]): A description of the permission.
    """

    __tablename__ = "permissions"

    name: Mapped[str]
    description: Mapped[Optional[text]]


class Role_x_Permission(Base):
    """
    Model representing the assignment of permissions to roles.

    Attributes:
        role_id (int): The ID of the associated role.
        permission_id (int): The ID of the associated permission.
        role (Role): The role associated with this relationship.
        permission (Permission): The permission associated with this relationship.
    """

    __tablename__ = "roles_x_permissions"
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="_role_permission_uc"),
    )

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"))

    role: Mapped["Role"] = relationship(
        back_populates="role_x_permission", lazy="joined"
    )
    permissions: Mapped[List["Permission"]] = relationship(
        back_populates="role_x_permission", lazy="joined"
    )


class Role_x_User_x_Org(Base):
    """
    Model representing the assignment of roles, users, and organizations.

    Attributes:
        role_id (int): The ID of the associated role.
        user_id (int): The ID of the associated user.
        org_id (int): The ID of the associated organization.
        role (Role): The role associated with this relationship.
        user (User): The user associated with this relationship.
        org (Org): The organization associated with this relationship.
    """

    __tablename__ = "roles_x_users_x_org"
    __table_args__ = (
        UniqueConstraint("role_id", "user_id", "org_id", name="_role_user_org_uc"),
    )

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))

    role: Mapped["Role"] = relationship(
        back_populates="role_x_user_x_org", lazy="joined"
    )
    user: Mapped["User"] = relationship(
        back_populates="role_x_user_x_org", lazy="joined"
    )
    org: Mapped["Org"] = relationship(back_populates="role_x_user_x_org", lazy="joined")


class Org(Base):
    """
    Model representing an organization. The same model is used for all levels of organization (AOs, Regions, etc.).

    Attributes:
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
        parent_org (Optional[Org]): The parent organization.
        child_orgs (List[Org]): The child organizations.
        locations (List[Location]): The locations associated with the organization.
        event_tags (List[EventTag]): The event tags associated with the organization.
        event_types (List[EventType]): The event types associated with the organization.
        events (List[Event]): The events associated with the organization.
    """

    __tablename__ = "orgs"

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

    parent_org: Mapped[Optional["Org"]] = relationship(
        "Org", remote_side="Org.id", back_populates="child_orgs"
    )
    child_orgs: Mapped[List["Org"]] = relationship(
        "Org", back_populates="parent_org", join_depth=3
    )
    locations: Mapped[List["Location"]] = relationship(
        back_populates="org", lazy="joined"
    )
    event_tags: Mapped[List["EventTag"]] = relationship(
        back_populates="org", secondary="event_tags_x_org", lazy="joined"
    )
    event_types: Mapped[List["EventType"]] = relationship(
        back_populates="org", secondary="event_types_x_org", lazy="joined"
    )
    events: Mapped[List["Event"]] = relationship(back_populates="org", lazy="joined")


class EventType(Base):
    """
    Model representing an event type. Event types can be shared by regions or not, and should roll up into event categories.

    Attributes:
        name (str): The name of the event type.
        description (Optional[text]): A description of the event type.
        acronyms (Optional[str]): Acronyms associated with the event type.
        category_id (int): The ID of the associated event category.
        event_category (EventCategory): The event category associated with this event type.
    """

    __tablename__ = "event_types"

    name: Mapped[str]
    description: Mapped[Optional[text]]
    acronyms: Mapped[Optional[str]]
    category_id: Mapped[int] = mapped_column(ForeignKey("event_categories.id"))

    event_category: Mapped["EventCategory"] = relationship(
        back_populates="event_types", lazy="joined"
    )


class EventType_x_Event(Base):
    """
    Model representing the association between events and event types. The intention is that a single event can be associated with multiple event types.

    Attributes:
        event_id (int): The ID of the associated event.
        event_type_id (int): The ID of the associated event type.
        event (Event): The event associated with this relationship.
        event_type (EventType): The event type associated with this relationship.
    """

    __tablename__ = "events_x_event_types"
    __table_args__ = (
        UniqueConstraint("event_id", "event_type_id", name="_event_event_type_uc"),
    )

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event_type_id: Mapped[int] = mapped_column(ForeignKey("event_types.id"))

    event: Mapped["Event"] = relationship(
        back_populates="events_x_event_types", lazy="joined"
    )
    event_type: Mapped["EventType"] = relationship(
        back_populates="events_x_event_types", lazy="joined"
    )


class EventType_x_Org(Base):
    """
    Model representing the association between event types and organizations. This controls which event types are available for selection at the region level, as well as default types for each AO.

    Attributes:
        event_type_id (int): The ID of the associated event type.
        org_id (int): The ID of the associated organization.
        is_default (bool): Whether this is the default event type for the organization.
        event_type (EventType): The event type associated with this relationship.
        org (Org): The organization associated with this relationship.
    """

    __tablename__ = "event_types_x_org"
    __table_args__ = (
        UniqueConstraint("event_type_id", "org_id", name="_event_type_org_uc"),
    )

    event_type_id: Mapped[int] = mapped_column(ForeignKey("event_types.id"))
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    is_default: Mapped[bool]

    event_type: Mapped["EventType"] = relationship(
        back_populates="event_type_x_org", lazy="joined"
    )
    org: Mapped["Org"] = relationship(back_populates="event_type_x_org", lazy="joined")


class EventTag(Base):
    """
    Model representing an event tag. These are used to mark special events, such as anniversaries or special workouts.

    Attributes:
        name (str): The name of the event tag.
        description (Optional[text]): A description of the event tag.
        color (Optional[str]): The color used for the calendar.
    """

    __tablename__ = "event_tags"

    name: Mapped[str]
    description: Mapped[Optional[text]]
    color: Mapped[Optional[str]]


class EventTag_x_Event(Base):
    """
    Model representing the association between event tags and events. The intention is that a single event can be associated with multiple event tags.

    Attributes:
        event_id (int): The ID of the associated event.
        event_tag_id (int): The ID of the associated event tag.
        event (Event): The event associated with this relationship.
        event_tag (EventTag): The event tag associated with this relationship.
    """

    __tablename__ = "event_tags_x_events"
    __table_args__ = (
        UniqueConstraint("event_id", "event_tag_id", name="_event_event_tag_uc"),
    )

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event_tag_id: Mapped[int] = mapped_column(ForeignKey("event_tags.id"))

    event: Mapped["Event"] = relationship(
        back_populates="event_tag_x_event", lazy="joined"
    )
    event_tag: Mapped["EventTag"] = relationship(
        back_populates="event_tag_x_event", lazy="joined"
    )


class EventTag_x_Org(Base):
    """
    Model representing the association between event tags and organizations. Controls which event tags are available for selection at the region level.

    Attributes:
        event_tag_id (int): The ID of the associated event tag.
        org_id (int): The ID of the associated organization.
        color_override (Optional[str]): The color override for the event tag (if the region wants to use something other than the default).
        event_tag (EventTag): The event tag associated with this relationship.
        org (Org): The organization associated with this relationship.
    """

    __tablename__ = "event_tags_x_org"
    __table_args__ = (
        UniqueConstraint("event_tag_id", "org_id", name="_event_tag_org_uc"),
    )

    event_tag_id: Mapped[int] = mapped_column(ForeignKey("event_tags.id"))
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    color_override: Mapped[Optional[str]]

    event_tag: Mapped["EventTag"] = relationship(
        back_populates="event_tag_x_org", lazy="joined"
    )
    org: Mapped["Org"] = relationship(back_populates="event_tag_x_org", lazy="joined")


class Org_x_Slack(Base):
    """
    Model representing the association between organizations and Slack workspaces. This is currently meant to be one to one, but theoretically could support multiple workspaces per organization.

    Attributes:
        org_id (int): The ID of the associated organization.
        slack_space_id (str): The ID of the associated Slack workspace.
        slack_space (SlackSpace): The Slack workspace associated with this relationship.
        org (Org): The organization associated with this relationship.
    """

    __tablename__ = "org_x_slack"
    __table_args__ = (
        UniqueConstraint("org_id", "slack_space_id", name="_org_slack_uc"),
    )

    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    slack_space_id: Mapped[str] = mapped_column(ForeignKey("slack_spaces.id"))

    slack_space: Mapped["SlackSpace"] = relationship(
        back_populates="org_x_slack", lazy="joined"
    )
    org: Mapped["Org"] = relationship(back_populates="org_x_slack", lazy="joined")


class Location(Base):
    """
    Model representing a location. Locations are expected to belong to a single organization (region).

    Attributes:
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
        org (Org): The organization associated with this location.
    """

    __tablename__ = "locations"

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

    org: Mapped["Org"] = relationship(back_populates="locations", lazy="joined")


class Event(Base):
    """
    Model representing an event or series; the same model is used for both with a self-referential relationship for series.

    Attributes:
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
        org (Org): The organization associated with this event.
        location (Location): The location associated with this event.
        event_type (EventType): The event type associated with this event.
        event_tag (EventTag): Any event tags associated with this event.
        series (Event): The event series associated with this event.
        attendance (List[Attendance]): The attendance records for this event.
        event_tags_x_event (List[EventTag_x_Event]): The event tags associated with this event.
        event_types_x_event (List[EventType_x_Event]): The event types associated with this event.
        event_tags (List[EventTag]): The event tags associated with this event.
        event_types (List[EventType]): The event types associated with this event.
    """

    __tablename__ = "events"

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

    org: Mapped["Org"] = relationship(back_populates="events", lazy="joined")
    location: Mapped["Location"] = relationship(back_populates="events", lazy="joined")
    series: Mapped["Event"] = relationship(
        back_populates="events", remote_side="Event.id", lazy="joined"
    )
    occurences: Mapped[List["Event"]] = relationship(
        back_populates="series", lazy="joined"
    )
    attendance: Mapped[List["Attendance"]] = relationship(
        back_populates="events", lazy="joined"
    )
    event_tags_x_event: Mapped[List["EventTag_x_Event"]] = relationship(
        back_populates="events"
    )
    event_types_x_event: Mapped[List["EventType_x_Event"]] = relationship(
        back_populates="events"
    )
    event_tags: Mapped[List["EventTag"]] = relationship(
        back_populates="event", secondary="event_tags_x_event", lazy="joined"
    )
    event_types: Mapped[List["EventType"]] = relationship(
        back_populates="event", secondary="event_types_x_event", lazy="joined"
    )


class AttendanceType(Base):
    """
    Model representing an attendance type. Basic types are 1='PAX', 2='Q', 3='Co-Q'

    Attributes:
        type (str): The type of attendance.
        description (Optional[str]): A description of the attendance type.
    """

    __tablename__ = "attendance_types"

    type: Mapped[str]
    description: Mapped[Optional[str]]


class Attendance(Base):
    """
    Model representing an attendance record.

    Attributes:
        event_id (int): The ID of the associated event.
        user_id (Optional[int]): The ID of the associated user.
        attendance_type_id (int): The ID of the associated attendance type.
        is_planned (bool): Whether this is planned attendance (True) vs actual attendance (False).
        meta (Optional[Dict[str, Any]]): Additional metadata for the attendance.
        event (Event): The event associated with this attendance.
        user (User): The user associated with this attendance.
        attendance_type (AttendanceType): The attendance type associated with this attendance.
    """

    __tablename__ = "attendance"
    __table_args__ = (
        UniqueConstraint(
            "event_id", "user_id", "is_planned", name="_event_user_planned_uc"
        ),
    )

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    attendance_type_id: Mapped[int] = mapped_column(ForeignKey("attendance_types.id"))
    is_planned: Mapped[bool]
    meta: Mapped[Optional[Dict[str, Any]]]

    event: Mapped["Event"] = relationship(back_populates="attendance", lazy="joined")
    user: Mapped["User"] = relationship(back_populates="attendance", lazy="joined")
    attendance_type: Mapped["AttendanceType"] = relationship(
        back_populates="attendance", lazy="joined"
    )


class User(Base):
    """
    Model representing a user.

    Attributes:
        f3_name (Optional[str]): The F3 name of the user.
        first_name (Optional[str]): The first name of the user.
        last_name (Optional[str]): The last name of the user.
        email (str): The email of the user.
        phone (Optional[str]): The phone number of the user.
        home_region_id (Optional[int]): The ID of the home region.
        avatar_url (Optional[str]): The URL of the user's avatar.
        meta (Optional[Dict[str, Any]]): Additional metadata for the user.
        home_region (Org): The home region associated with this user.
        attendance (List[Attendance]): The attendance records for this user.
        slack_users (List[SlackUser]): The Slack users associated with this user.
        achievements_x_user (List[Achievement_x_User]): The achievements associated with this user.
        positions_x_orgs_x_users (List[Position_x_Org_x_User]): The positions associated with this user.
        roles_x_users_x_org (List[Role_x_User_x_Org]): The roles associated with this user.
        positions (List[Position]): The positions associated with this user.
        roles (List[Role]): The roles associated with this user.
    """

    __tablename__ = "users"

    f3_name: Mapped[Optional[str]]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(VARCHAR, unique=True)
    phone: Mapped[Optional[str]]
    home_region_id: Mapped[Optional[int]] = mapped_column(ForeignKey("orgs.id"))
    avatar_url: Mapped[Optional[str]]
    meta: Mapped[Optional[Dict[str, Any]]]

    home_region: Mapped["Org"] = relationship(back_populates="users", lazy="joined")
    attendance: Mapped[List["Attendance"]] = relationship(
        back_populates="users", lazy="joined"
    )
    slack_users: Mapped[List["SlackUser"]] = relationship(
        back_populates="users", lazy="joined"
    )
    achievements_x_user: Mapped[List["Achievement_x_User"]] = relationship(
        back_populates="user"
    )
    positions_x_orgs_x_users: Mapped[List["Position_x_Org_x_User"]] = relationship(
        back_populates="user"
    )
    roles_x_users_x_org: Mapped[List["Role_x_User_x_Org"]] = relationship(
        back_populates="user"
    )
    achievements: Mapped[List["Achievement"]] = relationship(
        back_populates="user", secondary="achievements_x_users", lazy="joined"
    )
    positions: Mapped[List["Position"]] = relationship(
        back_populates="user", secondary="positions_x_orgs_x_users", lazy="joined"
    )
    roles: Mapped[List["Role"]] = relationship(
        back_populates="user", secondary="roles_x_users_x_org", lazy="joined"
    )


class SlackUser(Base):
    """
    Model representing a Slack user.

    Attributes:
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
        slack_space (SlackSpace): The Slack workspace associated with this user.
        user (User): The user associated with this Slack user.
    """

    __tablename__ = "slack_users"

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

    slack_space: Mapped["SlackSpace"] = relationship(
        back_populates="slack_users", lazy="joined"
    )
    user: Mapped["User"] = relationship(back_populates="slack_users", lazy="joined")


class Achievement(Base):
    """
    Model representing an achievement.

    Attributes:
        name (str): The name of the achievement.
        description (Optional[str]): A description of the achievement.
        verb (str): The verb associated with the achievement.
        image_url (Optional[str]): The URL of the achievement's image.
    """

    __tablename__ = "achievements"

    name: Mapped[str]
    description: Mapped[Optional[str]]
    verb: Mapped[str]
    image_url: Mapped[Optional[str]]


class Achievement_x_User(Base):
    """
    Model representing the association between achievements and users.

    Attributes:
        achievement_id (int): The ID of the associated achievement.
        user_id (int): The ID of the associated user.
        date_awarded (date): The date the achievement was awarded.
        achievement (Achievement): The achievement associated with this relationship.
        user (User): The user associated with this relationship.
    """

    __tablename__ = "achievements_x_users"
    __table_args__ = (
        UniqueConstraint("achievement_id", "user_id", name="_achievement_user_uc"),
    )

    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievements.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_awarded: Mapped[date]

    achievement: Mapped["Achievement"] = relationship(
        back_populates="achievement_x_user", lazy="joined"
    )
    user: Mapped["User"] = relationship(
        back_populates="achievement_x_user", lazy="joined"
    )


class Achievement_x_Org(Base):
    """
    Model representing the association between achievements and organizations.

    Attributes:
        achievement_id (int): The ID of the associated achievement.
        org_id (int): The ID of the associated organization.
        achievement (Achievement): The achievement associated with this relationship.
        org (Org): The organization associated with this relationship.
    """

    __tablename__ = "achievements_x_org"
    __table_args__ = (
        UniqueConstraint("achievement_id", "org_id", name="_achievement_org_uc"),
    )

    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievements.id"))
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))

    achievement: Mapped["Achievement"] = relationship(
        back_populates="achievement_x_org", lazy="joined"
    )
    org: Mapped["Org"] = relationship(back_populates="achievement_x_org", lazy="joined")


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

    name: Mapped[str]
    description: Mapped[Optional[str]]
    org_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("org_types.id"))
    org_id: Mapped[Optional[int]] = mapped_column(ForeignKey("orgs.id"))


class Position_x_Org_x_User(Base):
    """
    Model representing the association between positions, organizations, and users.

    Attributes:
        position_id (int): The ID of the associated position.
        org_id (int): The ID of the associated organization.
        user_id (int): The ID of the associated user.
        position (Position): The position associated with this relationship.
        org (Org): The organization associated with this relationship.
        user (User): The user associated with this relationship.
    """

    __tablename__ = "positions_x_orgs_x_users"
    __table_args__ = (
        UniqueConstraint(
            "position_id", "user_id", "org_id", name="_position_user_org_uc"
        ),
    )

    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    position: Mapped["Position"] = relationship(
        back_populates="position_x_org_x_user", lazy="joined"
    )
    org: Mapped["Org"] = relationship(
        back_populates="position_x_org_x_user", lazy="joined"
    )
    user: Mapped["User"] = relationship(
        back_populates="position_x_org_x_user", lazy="joined"
    )


class Expansion(Base):
    """
    Model representing an expansion.

    Attributes:
        area (str): The area of the expansion.
        pinned_lat (float): The pinned latitude of the expansion.
        pinned_lon (float): The pinned longitude of the expansion.
        user_lat (float): The user's latitude.
        user_lon (float): The user's longitude.
        interested_in_organizing (bool): Whether the user is interested in organizing.
    """

    __tablename__ = "expansions"

    area: Mapped[str]
    pinned_lat: Mapped[float]
    pinned_lon: Mapped[float]
    user_lat: Mapped[float]
    user_lon: Mapped[float]
    interested_in_organizing: Mapped[bool]


class Expansion_x_User(Base):
    """
    Model representing the association between expansions and users.

    Attributes:
        expansion_id (int): The ID of the associated expansion.
        user_id (int): The ID of the associated user.
        date (date): The date of the association.
        notes (Optional[text]): Additional notes for the association.
        expansion (Expansion): The expansion associated with this relationship.
        user (User): The user associated with this relationship.
    """

    __tablename__ = "expansions_x_users"
    __table_args__ = (
        UniqueConstraint("expansion_id", "user_id", name="_expansion_user_uc"),
    )

    expansion_id: Mapped[int] = mapped_column(ForeignKey("expansions.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[date]
    notes: Mapped[Optional[text]]

    expansion: Mapped["Expansion"] = relationship(
        back_populates="expansion_x_user", lazy="joined"
    )
    user: Mapped["User"] = relationship(
        back_populates="expansion_x_user", lazy="joined"
    )
