"""add_private_key_to_wallet

Revision ID: d68b9f8cef91
Revises: 0ebecc2fd018
Create Date: 2023-06-16 19:23:43.812573

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d68b9f8cef91"
down_revision = "0ebecc2fd018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        op.f("ix_transaction_from_address"),
        "transaction",
        ["from_address"],
        unique=False,
    )
    op.create_index(
        op.f("ix_transaction_to_address"), "transaction", ["to_address"], unique=False
    )
    op.add_column(
        "wallet", sa.Column("private_key", sa.String(length=64), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("wallet", "private_key")
    op.drop_index(op.f("ix_transaction_to_address"), table_name="transaction")
    op.drop_index(op.f("ix_transaction_from_address"), table_name="transaction")
    # ### end Alembic commands ###
