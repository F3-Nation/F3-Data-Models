from datetime import datetime, date, time
from typing import Any, Dict, List, Optional
from sqlalchemy import TEXT, TIME, DateTime, Integer, UniqueConstraint, func
from typing_extensions import Annotated
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped

# Custom Annotations
dt_create = Annotated[
    datetime, mapped_column(DateTime, server_default=func.timezone("utc", func.now()))
]
dt_update = Annotated[
    datetime,
    mapped_column(
        DateTime,
        server_default=func.timezone("utc", func.now()),
        onupdate=func.timezone("utc", func.now()),
    ),
]
intpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
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
    created: Mapped[datetime] = dt_create
    updated: Mapped[datetime] = dt_update

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
        team_id (str): The unique identifier for the Slack team.
        workspace_name (Optional[str]): The name of the Slack workspace.
        bot_token (Optional[str]): The bot token for the Slack workspace.
        settings (Optional[Dict[str, Any]]): Additional settings for the Slack workspace.
    """

    __tablename__ = "slack_spaces"

    team_id: Mapped[str] = mapped_column(primary_key=True)
    workspace_name: Mapped[Optional[str]]
    bot_token: Mapped[Optional[str]]
    settings: Mapped[Optional[Dict[str, Any]]]


class OrgType(Base):
    """
    Model representing an organization type.

    Attributes:
        name (str): The name of the organization type.
        description (Optional[text]): A description of the organization type.
    """

    __tablename__ = "org_types"

    name: Mapped[str]
    description: Mapped[Optional[text]]


class EventCategory(Base):
    """
    Model representing an event category.

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


class EventType(Base):
    """
    Model representing an event type.

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
    category_id: Mapped[int] = mapped_column(foreign_key="event_categories.id")

    event_category: Mapped["EventCategory"] = relationship(back_populates="event_types")


class Role(Base):
    """
    Model representing a role.

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
    Model representing the association between roles and permissions.

    Attributes:
        role_id (int): The ID of the associated role.
        permission_id (int): The ID of the associated permission.
        role (Role): The role associated with this relationship.
        permission (Permission): The permission associated with this relationship.
    """

    __tablename__ = "roles_x_permissions"

    role_id: Mapped[int] = mapped_column(foreign_key="roles.id")
    permission_id: Mapped[int] = mapped_column(foreign_key="permissions.id")

    role: Mapped["Role"] = relationship(back_populates="role_x_permission")
    permission: Mapped["Permission"] = relationship(back_populates="role_x_permission")


class Role_x_User_x_Org(Base):
    """
    Model representing the association between roles, users, and organizations.

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

    role_id: Mapped[int] = mapped_column(foreign_key="roles.id")
    user_id: Mapped[int] = mapped_column(foreign_key="users.id")
    org_id: Mapped[int] = mapped_column(foreign_key="orgs.id")

    role: Mapped["Role"] = relationship(back_populates="role_x_user_x_org")
    user: Mapped["User"] = relationship(back_populates="role_x_user_x_org")
    org: Mapped["Org"] = relationship(back_populates="role_x_user_x_org")


class Org(Base):
    """
    Model representing an organization.

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
    """

    __tablename__ = "orgs"

    parent_id: Mapped[Optional[int]] = mapped_column(foreign_key="orgs.id")
    org_type_id: Mapped[int] = mapped_column(foreign_key="org_types.id")
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
        "Org", back_populates="parent_org", join_depth=2
    )
    locations: Mapped[List["Location"]] = relationship(back_populates="org")


class EventType_x_Org(Base):
    """
    Model representing the association between event types and organizations.

    Attributes:
        event_type_id (int): The ID of the associated event type.
        org_id (int): The ID of the associated organization.
        is_default (bool): Whether this is the default event type for the organization.
        event_type (EventType): The event type associated with this relationship.
        org (Org): The organization associated with this relationship.
    """

    __tablename__ = "event_types_x_org"

    event_type_id: Mapped[int] = mapped_column(foreign_key="event_types.id")
    org_id: Mapped[int] = mapped_column(foreign_key="orgs.id")
    is_default: Mapped[bool]

    event_type: Mapped["EventType"] = relationship(back_populates="event_type_x_org")
    org: Mapped["Org"] = relationship(back_populates="event_type_x_org")


class EventTag(Base):
    """
    Model representing an event tag.

    Attributes:
        name (str): The name of the event tag.
        description (Optional[text]): A description of the event tag.
        color (Optional[str]): The color associated with the event tag.
    """

    __tablename__ = "event_tags"

    name: Mapped[str]
    description: Mapped[Optional[text]]
    color: Mapped[Optional[str]]


class EventTag_x_Org(Base):
    """
    Model representing the association between event tags and organizations.

    Attributes:
        event_tag_id (int): The ID of the associated event tag.
        org_id (int): The ID of the associated organization.
        color_override (Optional[str]): The color override for the event tag.
        event_tag (EventTag): The event tag associated with this relationship.
        org (Org): The organization associated with this relationship.
    """

    __tablename__ = "event_tags_x_org"

    event_tag_id: Mapped[int] = mapped_column(foreign_key="event_tags.id")
    org_id: Mapped[int] = mapped_column(foreign_key="orgs.id")
    color_override: Mapped[Optional[str]]

    event_tag: Mapped["EventTag"] = relationship(back_populates="event_tag_x_org")
    org: Mapped["Org"] = relationship(back_populates="event_tag_x_org")


class Org_x_Slack(Base):
    """
    Model representing the association between organizations and Slack workspaces.

    Attributes:
        org_id (int): The ID of the associated organization.
        slack_space_id (str): The ID of the associated Slack workspace.
        slack_space (SlackSpace): The Slack workspace associated with this relationship.
        org (Org): The organization associated with this relationship.
    """

    __tablename__ = "org_x_slack"

    org_id: Mapped[int] = mapped_column(foreign_key="orgs.id")
    slack_space_id: Mapped[str] = mapped_column(foreign_key="slack_spaces.team_id")

    slack_space: Mapped["SlackSpace"] = relationship(back_populates="org_x_slack")
    org: Mapped["Org"] = relationship(back_populates="org_x_slack")


class Location(Base):
    """
    Model representing a location.

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

    org_id: Mapped[int] = mapped_column(foreign_key="orgs.id")
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

    org: Mapped["Org"] = relationship(back_populates="locations")


class Event(Base):
    """
    Model representing an event.

    Attributes:
        org_id (int): The ID of the associated organization.
        location_id (Optional[int]): The ID of the associated location.
        event_type_id (int): The ID of the associated event type.
        event_tag_id (Optional[int]): The ID of the associated event tag.
        series_id (Optional[int]): The ID of the associated event series.
        is_series (bool): Whether the event is part of a series.
        is_active (bool): Whether the event is active.
        highlight (bool): Whether the event is highlighted.
        start_date (date): The start date of the event.
        end_date (Optional[date]): The end date of the event.
        start_time (Optional[time_notz]): The start time of the event.
        end_time (Optional[time_notz]): The end time of the event.
        day_of_week (Optional[int]): The day of the week of the event.
        name (str): The name of the event.
        description (Optional[text]): A description of the event.
        recurrence_pattern (Optional[str]): The recurrence pattern of the event.
        recurrence_interval (Optional[int]): The recurrence interval of the event.
        index_within_interval (Optional[int]): The index within the recurrence interval.
        pax_count (Optional[int]): The number of participants.
        fng_count (Optional[int]): The number of first-time participants.
        preblast (Optional[text]): The pre-event announcement.
        backblast (Optional[text]): The post-event report.
        preblast_rich (Optional[Dict[str, Any]]): The rich text pre-event announcement.
        backblast_rich (Optional[Dict[str, Any]]): The rich text post-event report.
        preblast_ts (Optional[float]): The timestamp of the pre-event announcement.
        backblast_ts (Optional[float]): The timestamp of the post-event report.
        meta (Optional[Dict[str, Any]]): Additional metadata for the event.
        org (Org): The organization associated with this event.
        location (Location): The location associated with this event.
        event_type (EventType): The event type associated with this event.
        event_tag (EventTag): The event tag associated with this event.
        series (Event): The event series associated with this event.
        attendance (List[Attendance]): The attendance records for this event.
    """

    __tablename__ = "events"

    org_id: Mapped[int] = mapped_column(foreign_key="orgs.id")
    location_id: Mapped[Optional[int]] = mapped_column(foreign_key="locations.id")
    event_type_id: Mapped[int] = mapped_column(foreign_key="event_types.id")
    event_tag_id: Mapped[Optional[int]] = mapped_column(foreign_key="event_tags.id")
    series_id: Mapped[Optional[int]] = mapped_column(foreign_key="events.id")
    is_series: Mapped[bool]
    is_active: Mapped[bool]
    highlight: Mapped[bool]
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

    org: Mapped["Org"] = relationship(back_populates="events")
    location: Mapped["Location"] = relationship(back_populates="events")
    event_type: Mapped["EventType"] = relationship(back_populates="events")
    event_tag: Mapped["EventTag"] = relationship(back_populates="events")
    series: Mapped["Event"] = relationship(back_populates="events")
    attendance: Mapped[List["Attendance"]] = relationship(back_populates="events")


class AttendanceType(Base):
    """
    Model representing an attendance type.

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
        is_planned (bool): Whether the attendance was planned.
        meta (Optional[Dict[str, Any]]): Additional metadata for the attendance.
        event (Event): The event associated with this attendance.
        user (User): The user associated with this attendance.
        attendance_type (AttendanceType): The attendance type associated with this attendance.
    """

    __tablename__ = "attendance"

    event_id: Mapped[int] = mapped_column(foreign_key="events.id")
    user_id: Mapped[Optional[int]] = mapped_column(foreign_key="users.id")
    attendance_type_id: Mapped[int] = mapped_column(foreign_key="attendance_types.id")
    is_planned: Mapped[bool]
    meta: Mapped[Optional[Dict[str, Any]]]

    event: Mapped["Event"] = relationship(back_populates="attendance")
    user: Mapped["User"] = relationship(back_populates="attendance")
    attendance_type: Mapped["AttendanceType"] = relationship(
        back_populates="attendance"
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
    """

    __tablename__ = "users"

    f3_name: Mapped[Optional[str]]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    email: Mapped[str]
    phone: Mapped[Optional[str]]
    home_region_id: Mapped[Optional[int]] = mapped_column(foreign_key="orgs.id")
    avatar_url: Mapped[Optional[str]]
    meta: Mapped[Optional[Dict[str, Any]]]

    home_region: Mapped["Org"] = relationship(back_populates="users")
    attendance: Mapped[List["Attendance"]] = relationship(back_populates="users")


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
    user_id: Mapped[Optional[int]] = mapped_column(foreign_key="users.id")
    avatar_url: Mapped[Optional[str]]
    slack_team_id: Mapped[str] = mapped_column(foreign_key="slack_spaces.team_id")
    strava_access_token: Mapped[Optional[str]]
    strava_refresh_token: Mapped[Optional[str]]
    strava_expires_at: Mapped[Optional[datetime]]
    strava_athlete_id: Mapped[Optional[int]]
    meta: Mapped[Optional[Dict[str, Any]]]
    slack_updated: Mapped[Optional[datetime]]

    slack_space: Mapped["SlackSpace"] = relationship(back_populates="slack_users")
    user: Mapped["User"] = relationship(back_populates="slack_users")


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
        org (Org): The organization associated with this relationship.
    """

    __tablename__ = "achievements_x_users"

    achievement_id: Mapped[int] = mapped_column(foreign_key="achievements.id")
    user_id: Mapped[int] = mapped_column(foreign_key="users.id")
    date_awarded: Mapped[date]

    achievement: Mapped["Achievement"] = relationship(
        back_populates="achievement_x_user"
    )
    user: Mapped["User"] = relationship(back_populates="achievement_x_user")
    org: Mapped["Org"] = relationship(back_populates="achievement_x_user")


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

    achievement_id: Mapped[int] = mapped_column(foreign_key="achievements.id")
    org_id: Mapped[int] = mapped_column(foreign_key="orgs.id")

    achievement: Mapped["Achievement"] = relationship(
        back_populates="achievement_x_org"
    )
    org: Mapped["Org"] = relationship(back_populates="achievement_x_org")


class Position(Base):
    """
    Model representing a position.

    Attributes:
        name (str): The name of the position.
        description (Optional[str]): A description of the position.
        org_type_id (int): The ID of the associated organization type.
        org_id (int): The ID of the associated organization.
    """

    __tablename__ = "positions"

    name: Mapped[str]
    description: Mapped[Optional[str]]
    org_type_id: Mapped[int] = mapped_column(foreign_key="org_types.id")
    org_id: Mapped[int] = mapped_column(foreign_key="orgs.id")


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

    position_id: Mapped[int] = mapped_column(foreign_key="positions.id")
    org_id: Mapped[int] = mapped_column(foreign_key="orgs.id")
    user_id: Mapped[int] = mapped_column(foreign_key="users.id")

    position: Mapped["Position"] = relationship(back_populates="position_x_org_x_user")
    org: Mapped["Org"] = relationship(back_populates="position_x_org_x_user")
    user: Mapped["User"] = relationship(back_populates="position_x_org_x_user")


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

    expansion_id: Mapped[int] = mapped_column(foreign_key="expansions.id")
    user_id: Mapped[int] = mapped_column(foreign_key="users.id")
    date: Mapped[date]
    notes: Mapped[Optional[text]]

    expansion: Mapped["Expansion"] = relationship(back_populates="expansion_x_user")
    user: Mapped["User"] = relationship(back_populates="expansion_x_user")
