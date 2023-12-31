"""add_order_model

Revision ID: c16a0c0f2053
Revises: f46e010772fb
Create Date: 2023-07-18 15:41:41.299678

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c16a0c0f2053"
down_revision = "f46e010772fb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "order",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.Column("time", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=10), nullable=False),
        sa.Column("return_address", sa.String(length=42), nullable=False),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("order")
    # ### end Alembic commands ###
