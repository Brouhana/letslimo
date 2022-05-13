"""Initial migration.

Revision ID: 4ef28aacec3e
Revises: 
Create Date: 2022-05-11 21:51:43.265080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ef28aacec3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=255), nullable=False),
    sa.Column('company_address', sa.String(length=255), nullable=False),
    sa.Column('company_website_url', sa.String(length=255), nullable=False),
    sa.Column('company_general_email', sa.String(length=120), nullable=False),
    sa.Column('company_booking_email', sa.String(length=120), nullable=False),
    sa.Column('company_phone', sa.String(length=120), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('operator_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('first_name', sa.String(length=90), nullable=False),
    sa.Column('last_name', sa.String(length=90), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_owner', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_member', sa.Boolean(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('operator_users')
    op.drop_table('companies')
    # ### end Alembic commands ###
