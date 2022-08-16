"""empty message

Revision ID: dfc7e51aa780
Revises: 787f2df67866
Create Date: 2022-08-12 19:59:58.645021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfc7e51aa780'
down_revision = '787f2df67866'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('connected_account', sa.String(length=255), nullable=True))
    op.drop_column('companies', 'stripe_account')
    op.add_column('contacts_customers', sa.Column('customer_id', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contacts_customers', 'customer_id')
    op.add_column('companies', sa.Column('stripe_account', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('companies', 'connected_account')
    # ### end Alembic commands ###
