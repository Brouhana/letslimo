"""add tables

Revision ID: bbb667cce98b
Revises: 952d8fbcef9d
Create Date: 2022-05-12 22:22:51.319493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbb667cce98b'
down_revision = '952d8fbcef9d'
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
    op.create_table('driver_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('first_name', sa.String(length=90), nullable=False),
    sa.Column('last_name', sa.String(length=90), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('DL_number', sa.String(length=255), nullable=True),
    sa.Column('DL_state', sa.String(length=2), nullable=True),
    sa.Column('DL_expr', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('creation_code', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
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
    sa.Column('creation_code', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('pax_capacity', sa.Integer(), nullable=False),
    sa.Column('license_plate_number', sa.String(length=12), nullable=False),
    sa.Column('exterior_color', sa.String(length=120), nullable=True),
    sa.Column('vin_number', sa.String(length=20), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('has_air_conditioning', sa.Boolean(), nullable=True),
    sa.Column('has_dance_pole', sa.Boolean(), nullable=True),
    sa.Column('has_luggage_space', sa.Boolean(), nullable=True),
    sa.Column('has_tables', sa.Boolean(), nullable=True),
    sa.Column('has_onboard_bathroom', sa.Boolean(), nullable=True),
    sa.Column('has_onboard_bar', sa.Boolean(), nullable=True),
    sa.Column('has_refrigerator', sa.Boolean(), nullable=True),
    sa.Column('has_trash_can', sa.Boolean(), nullable=True),
    sa.Column('has_ice_chest', sa.Boolean(), nullable=True),
    sa.Column('has_wheelchair_accessibility', sa.Boolean(), nullable=True),
    sa.Column('has_aux', sa.Boolean(), nullable=True),
    sa.Column('has_bluetooth', sa.Boolean(), nullable=True),
    sa.Column('has_dvd_player', sa.Boolean(), nullable=True),
    sa.Column('has_karaoke', sa.Boolean(), nullable=True),
    sa.Column('has_usb', sa.Boolean(), nullable=True),
    sa.Column('has_power_outlets', sa.Boolean(), nullable=True),
    sa.Column('has_wifi', sa.Boolean(), nullable=True),
    sa.Column('has_tv', sa.Boolean(), nullable=True),
    sa.Column('has_gaming_console', sa.Boolean(), nullable=True),
    sa.Column('is_alcohol_allowed', sa.Boolean(), nullable=True),
    sa.Column('is_smoking_allowed', sa.Boolean(), nullable=True),
    sa.Column('is_pets_allowed', sa.Boolean(), nullable=True),
    sa.Column('is_food_allowed', sa.Boolean(), nullable=True),
    sa.Column('is_children_allowed', sa.Boolean(), nullable=True),
    sa.Column('min_total_base_rate', sa.Integer(), nullable=True),
    sa.Column('deadhead_rate_per_mile', sa.Integer(), nullable=True),
    sa.Column('trip_rate_per_mile', sa.Integer(), nullable=True),
    sa.Column('weekend_hourly_rate', sa.Integer(), nullable=True),
    sa.Column('weekend_hourly_min', sa.Integer(), nullable=True),
    sa.Column('weekday_hourly_rate', sa.Integer(), nullable=True),
    sa.Column('weekday_hourly_min', sa.Integer(), nullable=True),
    sa.Column('total_deadhead_duration', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicles')
    op.drop_table('operator_users')
    op.drop_table('driver_users')
    op.drop_table('companies')
    # ### end Alembic commands ###
