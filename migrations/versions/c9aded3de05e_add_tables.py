"""add tables

Revision ID: c9aded3de05e
Revises: 2cfac45ff182
Create Date: 2022-05-13 15:24:26.881680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9aded3de05e'
down_revision = '2cfac45ff182'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver_invites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('first_name', sa.String(length=90), nullable=False),
    sa.Column('last_name', sa.String(length=90), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('DL_number', sa.String(length=255), nullable=True),
    sa.Column('DL_state', sa.String(length=2), nullable=True),
    sa.Column('DL_expr', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('has_accepted', sa.Boolean(), nullable=True),
    sa.Column('invited_by_member_id', sa.Integer(), nullable=False),
    sa.Column('invite_code', sa.String(length=255), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['invited_by_member_id'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('member_invites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('first_name', sa.String(length=90), nullable=False),
    sa.Column('last_name', sa.String(length=90), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.Column('is_owner', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('has_accepted', sa.Boolean(), nullable=True),
    sa.Column('invited_by_member_id', sa.Integer(), nullable=False),
    sa.Column('invite_code', sa.String(length=255), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['invited_by_member_id'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('member_invites')
    op.drop_table('driver_invites')
    # ### end Alembic commands ###
