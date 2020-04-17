"""Remove old JH tables

Revision ID: 6a0a91fcca56
Revises: 8bd50951fa50
Create Date: 2020-04-17 18:52:05.423375

We renamed DailyReport to JHDailyReport. This migration ensures
that the old daily_reports table is gone.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a0a91fcca56'
down_revision = '8bd50951fa50'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("drop table if exists daily_reports cascade")


def downgrade():
    pass
