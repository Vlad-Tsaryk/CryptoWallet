"""add_parsed_block_table

Revision ID: 53058ed02046
Revises: 529f4cf16e27
Create Date: 2023-07-19 19:10:19.395925

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "53058ed02046"
down_revision = "529f4cf16e27"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "parsed_block",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("parsed_block")
    # ### end Alembic commands ###
