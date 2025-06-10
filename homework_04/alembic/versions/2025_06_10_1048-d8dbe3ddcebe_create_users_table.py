"""create users table

Revision ID: d8dbe3ddcebe
Revises:
Create Date: 2025-06-10 10:48:30.282719

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d8dbe3ddcebe"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=150), server_default="", nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
