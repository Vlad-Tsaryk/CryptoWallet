"""add_indexing_to_order

Revision ID: 5ef63b54f06f
Revises: 53058ed02046
Create Date: 2023-07-23 20:15:38.608536

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "5ef63b54f06f"
down_revision = "53058ed02046"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f("ix_order_tnx_hash"), "order", ["tnx_hash"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_order_tnx_hash"), table_name="order")
    # ### end Alembic commands ###