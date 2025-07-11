"""setting cascading deletes for event-related relationships

Revision ID: 760bee3701a9
Revises: be1c730cc2ef
Create Date: 2025-05-06 06:54:44.684550

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "760bee3701a9"
down_revision: Union[str, None] = "be1c730cc2ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("event_instances_series_id_fkey", "event_instances", type_="foreignkey")
    op.create_foreign_key(
        "event_instances_series_id_fkey",
        "event_instances",
        "events",
        ["series_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(
        "event_instances_x_event_types_event_instance_id_fkey", "event_instances_x_event_types", type_="foreignkey"
    )
    op.create_foreign_key(
        "event_instances_x_event_types_event_instance_id_fkey",
        "event_instances_x_event_types",
        "event_instances",
        ["event_instance_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(
        "event_tags_x_event_instances_event_instance_id_fkey", "event_tags_x_event_instances", type_="foreignkey"
    )
    op.create_foreign_key(
        "event_tags_x_event_instances_event_instance_id_fkey",
        "event_tags_x_event_instances",
        "event_instances",
        ["event_instance_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint("events_x_event_types_event_id_fkey", "events_x_event_types", type_="foreignkey")
    op.create_foreign_key(
        "events_x_event_types_event_id_fkey",
        "events_x_event_types",
        "events",
        ["event_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint("event_tags_x_events_event_id_fkey", "event_tags_x_events", type_="foreignkey")
    op.create_foreign_key(
        "event_tags_x_events_event_id_fkey",
        "event_tags_x_events",
        "events",
        ["event_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(
        "attendance_x_attendance_types_attendance_id_fkey", "attendance_x_attendance_types", type_="foreignkey"
    )
    op.create_foreign_key(
        "attendance_x_attendance_types_attendance_id_fkey",
        "attendance_x_attendance_types",
        "attendance",
        ["attendance_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint("event_instance_id_fkey", "attendance", type_="foreignkey")
    op.create_foreign_key(
        "event_instance_id_fkey",
        "attendance",
        "event_instances",
        ["event_instance_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
