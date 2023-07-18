"""add_product_model

Revision ID: f46e010772fb
Revises: d68b9f8cef91
Create Date: 2023-07-18 13:17:01.113177

"""
import sqlalchemy as sa
import sqlalchemy_file
from alembic import op

# revision identifiers, used by Alembic.
revision = "f46e010772fb"
down_revision = "d68b9f8cef91"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("photo", sqlalchemy_file.types.ImageField(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("wallet_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["wallet_id"],
            ["wallet.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_product_title"), "product", ["title"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_product_title"), table_name="product")
    op.drop_table("product")
    # ### end Alembic commands ###
