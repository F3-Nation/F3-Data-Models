"""Insert Dummy Data

Revision ID: 893179b61ab1
Revises: bc8d946e6cf2
Create Date: 2024-12-11 07:51:38.531440

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from f3_data_models.models import Base


# revision identifiers, used by Alembic.
revision: str = "893179b61ab1"
down_revision: Union[str, None] = "bc8d946e6cf2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


metadata = Base.metadata


def upgrade() -> None:
    op.bulk_insert(
        table=sa.schema.Table("org_types", metadata),
        rows=[
            {"name": "AO"},
            {"name": "Region"},
            {"name": "Area"},
            {"name": "Sector"},
        ],
    )
    op.bulk_insert(
        table=sa.schema.Table("achievements", metadata),
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
        table=sa.schema.Table("event_categories", metadata),
        rows=[
            {
                "name": "1st F - Core Workout",
                "description": "The core F3 activity - must meet all 5 core principles.",
            },
            {
                "name": "1st F - Pre Workout",
                "description": "Pre-workout activities (pre-rucks, pre-runs, etc).",
            },
            {
                "name": "1st F - Off the books",
                "description": "Fitness activities that didn't meet all 5 core principles (unscheduled, open to all men, etc).",  # noqa: E501
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
        table=sa.schema.Table("event_types", metadata),
        rows=[
            {"name": "Bootcamp", "category_id": 1, "acronym": "BC"},
            {"name": "Run", "category_id": 1, "acronym": "RU"},
            {"name": "Ruck", "category_id": 1, "acronym": "RK"},
            {"name": "QSource", "category_id": 3, "acronym": "QS"},
        ],
    )
    op.bulk_insert(
        table=sa.schema.Table("attendance_types", metadata),
        rows=[
            {"type": "PAX"},
            {"type": "Q"},
            {"type": "Co-Q"},
        ],
    )
    op.bulk_insert(
        table=sa.schema.Table("event_tags", metadata),
        rows=[
            {"name": "Open", "color": "Green"},
            {"name": "VQ", "color": "Blue"},
            {"name": "Manniversary", "color": "Yellow"},
            {"name": "Convergence", "color": "Orange"},
        ],
    )
    op.bulk_insert(
        table=sa.schema.Table("permissions", metadata),
        rows=[
            {"name": "All"},
        ],
    )
    op.bulk_insert(
        table=sa.schema.Table("roles", metadata),
        rows=[
            {"name": "Admin"},
        ],
    )
    op.bulk_insert(
        table=sa.schema.Table("roles_x_permissions", metadata),
        rows=[
            {"role_id": 1, "permission_id": 1},
        ],
    )
    op.bulk_insert(
        table=sa.schema.Table("orgs", metadata),
        rows=[
            {
                "org_type_id": 2,
                "name": "Example Region 1",
                "is_active": True,
            },
            {
                "org_type_id": 2,
                "name": "Example Region 2",
                "is_active": True,
            },
            {
                "org_type_id": 2,
                "name": "Example Region 3",
                "is_active": True,
            },
        ],
    )
    op.bulk_insert(
        table=sa.schema.Table("event_types_x_org", metadata),
        rows=[
            {"event_type_id": i, "is_default": False, "org_id": j}
            for i in range(1, 5)
            for j in range(1, 4)
        ],
    )
    op.bulk_insert(
        table=sa.schema.Table("event_tags_x_org", metadata),
        rows=[
            {"event_tag_id": i, "org_id": j} for i in range(1, 5) for j in range(1, 4)
        ],
    )
    op.bulk_insert(
        table=sa.schema.Table("positions", metadata),
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


def downgrade() -> None:
    op.execute("TRUNCATE TABLE org_types CASCADE")
    op.execute("TRUNCATE TABLE achievements CASCADE")
    op.execute("TRUNCATE TABLE event_categories CASCADE")
    op.execute("TRUNCATE TABLE event_types CASCADE")
    op.execute("TRUNCATE TABLE attendance_types CASCADE")
    op.execute("TRUNCATE TABLE event_tags CASCADE")
    op.execute("TRUNCATE TABLE permissions CASCADE")
    op.execute("TRUNCATE TABLE roles CASCADE")
    op.execute("TRUNCATE TABLE roles_x_permissions CASCADE")
    op.execute("TRUNCATE TABLE orgs CASCADE")
    op.execute("TRUNCATE TABLE event_types_x_org CASCADE")
    op.execute("TRUNCATE TABLE event_tags_x_org CASCADE")
    op.execute("TRUNCATE TABLE positions CASCADE")
