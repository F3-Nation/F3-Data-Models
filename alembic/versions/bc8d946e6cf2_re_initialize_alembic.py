"""Re-Initialize Alembic

Revision ID: bc8d946e6cf2
Revises:
Create Date: 2024-12-11 07:51:18.059779

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bc8d946e6cf2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    achievements_table = op.create_table(
        "achievements",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("verb", sa.String(), nullable=False),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    attendance_types_table = op.create_table(
        "attendance_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    event_categories_table = op.create_table(
        "event_categories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    event_tags_table = op.create_table(
        "event_tags",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("color", sa.String(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "expansions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("area", sa.String(), nullable=False),
        sa.Column("pinned_lat", sa.Float(), nullable=False),
        sa.Column("pinned_lon", sa.Float(), nullable=False),
        sa.Column("user_lat", sa.Float(), nullable=False),
        sa.Column("user_lon", sa.Float(), nullable=False),
        sa.Column("interested_in_organizing", sa.Boolean(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "magiclinkauthrecord",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("otp_hash", sa.LargeBinary(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "expiration",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column("client_ip", sa.String(), nullable=False),
        sa.Column("recent_attempts", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "magiclinkauthsession",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("persistent_id", sa.String(), nullable=False),
        sa.Column("session_token", sa.String(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "expiration",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    org_types_table = op.create_table(
        "org_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    permissions_table = op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    roles_table = op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "slack_spaces",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("team_id", sa.VARCHAR(), nullable=False),
        sa.Column("workspace_name", sa.String(), nullable=True),
        sa.Column("bot_token", sa.String(), nullable=True),
        sa.Column("settings", sa.JSON(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("team_id"),
    )
    event_types_table = op.create_table(
        "event_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("acronym", sa.String(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["event_categories.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "orgs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("org_type_id", sa.Integer(), nullable=False),
        sa.Column("default_location_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.Column("website", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("twitter", sa.String(), nullable=True),
        sa.Column("facebook", sa.String(), nullable=True),
        sa.Column("instagram", sa.String(), nullable=True),
        sa.Column("last_annual_review", sa.Date(), nullable=True),
        sa.Column("meta", sa.JSON(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["org_type_id"],
            ["org_types.id"],
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["orgs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    roles_x_permissions_table = op.create_table(
        "roles_x_permissions",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["permissions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )
    op.create_table(
        "achievements_x_org",
        sa.Column("achievement_id", sa.Integer(), nullable=False),
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["achievement_id"],
            ["achievements.id"],
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["orgs.id"],
        ),
        sa.PrimaryKeyConstraint("achievement_id", "org_id"),
    )
    op.create_table(
        "event_tags_x_org",
        sa.Column("event_tag_id", sa.Integer(), nullable=False),
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.Column("color_override", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["event_tag_id"],
            ["event_tags.id"],
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["orgs.id"],
        ),
        sa.PrimaryKeyConstraint("event_tag_id", "org_id"),
    )
    op.create_table(
        "event_types_x_org",
        sa.Column("event_type_id", sa.Integer(), nullable=False),
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_type_id"],
            ["event_types.id"],
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["orgs.id"],
        ),
        sa.PrimaryKeyConstraint("event_type_id", "org_id"),
    )
    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("lat", sa.Float(), nullable=True),
        sa.Column("lon", sa.Float(), nullable=True),
        sa.Column("address_street", sa.String(), nullable=True),
        sa.Column("address_city", sa.String(), nullable=True),
        sa.Column("address_state", sa.String(), nullable=True),
        sa.Column("address_zip", sa.String(), nullable=True),
        sa.Column("address_country", sa.String(), nullable=True),
        sa.Column("meta", sa.JSON(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["orgs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "org_x_slack",
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.Column("slack_space_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["orgs.id"],
        ),
        sa.ForeignKeyConstraint(
            ["slack_space_id"],
            ["slack_spaces.id"],
        ),
        sa.PrimaryKeyConstraint("org_id", "slack_space_id"),
    )
    positions_table = op.create_table(
        "positions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("org_type_id", sa.Integer(), nullable=True),
        sa.Column("org_id", sa.Integer(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["orgs.id"],
        ),
        sa.ForeignKeyConstraint(
            ["org_type_id"],
            ["org_types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("f3_name", sa.String(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("email", sa.VARCHAR(), nullable=False),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("home_region_id", sa.Integer(), nullable=True),
        sa.Column("avatar_url", sa.String(), nullable=True),
        sa.Column("meta", sa.JSON(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["home_region_id"],
            ["orgs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "achievements_x_users",
        sa.Column("achievement_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "date_awarded",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["achievement_id"],
            ["achievements.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("achievement_id", "user_id"),
    )
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.Column("location_id", sa.Integer(), nullable=True),
        sa.Column("series_id", sa.Integer(), nullable=True),
        sa.Column("is_series", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("highlight", sa.Boolean(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("start_time", sa.Time(), nullable=True),
        sa.Column("end_time", sa.Time(), nullable=True),
        sa.Column("day_of_week", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("recurrence_pattern", sa.String(), nullable=True),
        sa.Column("recurrence_interval", sa.Integer(), nullable=True),
        sa.Column("index_within_interval", sa.Integer(), nullable=True),
        sa.Column("pax_count", sa.Integer(), nullable=True),
        sa.Column("fng_count", sa.Integer(), nullable=True),
        sa.Column("preblast", sa.String(), nullable=True),
        sa.Column("backblast", sa.String(), nullable=True),
        sa.Column("preblast_rich", sa.JSON(), nullable=True),
        sa.Column("backblast_rich", sa.JSON(), nullable=True),
        sa.Column("preblast_ts", sa.Float(), nullable=True),
        sa.Column("backblast_ts", sa.Float(), nullable=True),
        sa.Column("meta", sa.JSON(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["location_id"],
            ["locations.id"],
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["orgs.id"],
        ),
        sa.ForeignKeyConstraint(
            ["series_id"],
            ["events.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "expansions_x_users",
        sa.Column("expansion_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "request_date",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column("notes", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["expansion_id"],
            ["expansions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("expansion_id", "user_id"),
    )
    op.create_table(
        "positions_x_orgs_x_users",
        sa.Column("position_id", sa.Integer(), nullable=False),
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["orgs.id"],
        ),
        sa.ForeignKeyConstraint(
            ["position_id"],
            ["positions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("position_id", "org_id", "user_id"),
    )
    op.create_table(
        "roles_x_users_x_org",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["orgs.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("role_id", "user_id", "org_id"),
    )
    op.create_table(
        "slack_users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slack_id", sa.String(), nullable=False),
        sa.Column("user_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("is_owner", sa.Boolean(), nullable=False),
        sa.Column("is_bot", sa.Boolean(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("avatar_url", sa.String(), nullable=True),
        sa.Column("slack_team_id", sa.VARCHAR(), nullable=False),
        sa.Column("strava_access_token", sa.String(), nullable=True),
        sa.Column("strava_refresh_token", sa.String(), nullable=True),
        sa.Column("strava_expires_at", sa.DateTime(), nullable=True),
        sa.Column("strava_athlete_id", sa.Integer(), nullable=True),
        sa.Column("meta", sa.JSON(), nullable=True),
        sa.Column("slack_updated", sa.DateTime(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["slack_team_id"],
            ["slack_spaces.team_id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "attendance",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("is_planned", sa.Boolean(), nullable=False),
        sa.Column("meta", sa.JSON(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id", "user_id", "is_planned"),
    )
    op.create_table(
        "event_tags_x_events",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("event_tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
        sa.ForeignKeyConstraint(
            ["event_tag_id"],
            ["event_tags.id"],
        ),
        sa.PrimaryKeyConstraint("event_id", "event_tag_id"),
    )
    op.create_table(
        "events_x_event_types",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("event_type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
        sa.ForeignKeyConstraint(
            ["event_type_id"],
            ["event_types.id"],
        ),
        sa.PrimaryKeyConstraint("event_id", "event_type_id"),
    )
    op.create_table(
        "attendance_x_attendance_types",
        sa.Column("attendance_id", sa.Integer(), nullable=False),
        sa.Column("attendance_type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["attendance_id"],
            ["attendance.id"],
        ),
        sa.ForeignKeyConstraint(
            ["attendance_type_id"],
            ["attendance_types.id"],
        ),
        sa.PrimaryKeyConstraint("attendance_id", "attendance_type_id"),
    )
    op.bulk_insert(
        table=org_types_table,
        rows=[
            {"name": "AO"},
            {"name": "Region"},
            {"name": "Area"},
            {"name": "Sector"},
            {"name": "Nation"},
        ],
    )
    op.bulk_insert(
        table=achievements_table,
        rows=[
            {
                "name": "The Priest",
                "description": "Post for 25 QSource lessons",
                "verb": "posting for 25 QSource lessons",
            },
            {
                "name": "The Monk",
                "description": "Post at 4 QSources in a month",
                "verb": "posting at 4 QSources in a month",
            },
            {
                "name": "Leader of Men",
                "description": "Q at 4 beatdowns in a month",
                "verb": "Qing at 4 beatdowns in a month",
            },
        ],
    )
    op.bulk_insert(
        table=event_categories_table,
        rows=[
            {
                "name": "1st F - Core Workout",
                "description": "The core F3 activity - must meet all 5 core principles.",
            },
            {
                "name": "2nd F - Fellowship",
                "description": "General category for 2nd F events.",
            },
            {
                "name": "3rd F - Faith",
                "description": "General category for 3rd F events.",
            },
        ],
    )
    op.bulk_insert(
        table=event_types_table,
        rows=[
            {"name": "Bootcamp", "category_id": 1, "acronym": "BC"},
            {"name": "Run", "category_id": 1, "acronym": "RU"},
            {"name": "Ruck", "category_id": 1, "acronym": "RK"},
            {"name": "QSource", "category_id": 3, "acronym": "QS"},
            {"name": "Swimming", "category_id": 1, "acronym": "SW"},
            {"name": "Mobility", "category_id": 1, "acronym": "MO"},
            {"name": "Bike", "category_id": 1, "acronym": "BI"},
            {"name": "Gear", "category_id": 1, "acronym": "GE"},
            {"name": "Wild Card", "category_id": 1, "acronym": "WC"},
            {"name": "Sports", "category_id": 1, "acronym": "SP"},
        ],
    )
    op.bulk_insert(
        table=attendance_types_table,
        rows=[
            {"type": "PAX"},
            {"type": "Q"},
            {"type": "Co-Q"},
        ],
    )
    op.bulk_insert(
        table=event_tags_table,
        rows=[
            {"name": "Open", "color": "Green"},
            {"name": "Pre-Workout", "color": "Black"},
            {"name": "Off-The-Books", "color": "Black"},
            {"name": "VQ", "color": "Blue"},
            {"name": "Manniversary", "color": "Red"},
            {"name": "Convergence", "color": "Orange"},
        ],
    )
    op.bulk_insert(
        table=permissions_table,
        rows=[
            {"name": "All"},
        ],
    )
    op.bulk_insert(
        table=roles_table,
        rows=[
            {"name": "Admin"},
        ],
    )
    op.bulk_insert(
        table=roles_x_permissions_table,
        rows=[
            {"role_id": 1, "permission_id": 1},
        ],
    )
    op.bulk_insert(
        table=positions_table,
        rows=[
            {"name": "Nantan", "org_type_id": 2},
            {"name": "Weasel Shaker", "org_type_id": 2},
            {"name": "Site Q", "org_type_id": 1},
            {"name": "QSource Q", "org_type_id": None},
            {"name": "1st-F Q", "org_type_id": None},
            {"name": "2nd-F Q", "org_type_id": None},
            {"name": "3rd-F Q", "org_type_id": None},
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("attendance_x_attendance_types")
    op.drop_table("events_x_event_types")
    op.drop_table("event_tags_x_events")
    op.drop_table("attendance")
    op.drop_table("slack_users")
    op.drop_table("roles_x_users_x_org")
    op.drop_table("positions_x_orgs_x_users")
    op.drop_table("expansions_x_users")
    op.drop_table("events")
    op.drop_table("achievements_x_users")
    op.drop_table("users")
    op.drop_table("positions")
    op.drop_table("org_x_slack")
    op.drop_table("locations")
    op.drop_table("event_types_x_org")
    op.drop_table("event_tags_x_org")
    op.drop_table("achievements_x_org")
    op.drop_table("roles_x_permissions")
    op.drop_table("orgs")
    op.drop_table("event_types")
    op.drop_table("slack_spaces")
    op.drop_table("roles")
    op.drop_table("permissions")
    op.drop_table("org_types")
    op.drop_table("magiclinkauthsession")
    op.drop_table("magiclinkauthrecord")
    op.drop_table("expansions")
    op.drop_table("event_tags")
    op.drop_table("event_categories")
    op.drop_table("attendance_types")
    op.drop_table("achievements")
    # ### end Alembic commands ###
