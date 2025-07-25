"""question

Revision ID: 72da1063738d
Revises: c9420169fd1d
Create Date: 2025-07-10 18:53:46.916379

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = "72da1063738d"
down_revision: Union[str, Sequence[str], None] = "c9420169fd1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("date_time", sa.DateTime(), nullable=False),
        sa.Column(
            "question_type",
            sa.Enum(
                "TEXT",
                "NUMBER",
                "DATE",
                "EMAIL",
                "PASSWORD",
                "CHECKBOX",
                "RADIO",
                "SELECT",
                "TEXTAREA",
                name="questiontypes",
            ),
            nullable=False,
        ),
        sa.Column("question", sa.String(length=255), nullable=False),
        sa.Column(
            "embeddings", pgvector.sqlalchemy.vector.VECTOR(dim=758), nullable=True
        ),
        sa.Column("response", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("questions")
    # ### end Alembic commands ###
