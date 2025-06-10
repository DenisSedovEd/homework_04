"""create posts table

Revision ID: 13d9db442029
Revises: d8dbe3ddcebe
Create Date: 2025-06-10 10:51:48.868149

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "13d9db442029"
down_revision: Union[str, None] = "d8dbe3ddcebe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=120), server_default="", nullable=False),
        sa.Column("body", sa.Text(), server_default="", nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_posts_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_posts")),
    )
    op.create_index(op.f("ix_posts_title"), "posts", ["title"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_posts_title"), table_name="posts")
    op.drop_table("posts")
