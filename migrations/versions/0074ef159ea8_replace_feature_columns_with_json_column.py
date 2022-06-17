"""replace feature columns with JSON column

Revision ID: 0074ef159ea8
Revises: c02d5d6a3b3c
Create Date: 2022-06-16 16:18:23.401913

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0074ef159ea8'
down_revision = 'c02d5d6a3b3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('features', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.drop_column('vehicles', 'has_power_outlets')
    op.drop_column('vehicles', 'has_tables')
    op.drop_column('vehicles', 'has_bluetooth')
    op.drop_column('vehicles', 'has_onboard_bar')
    op.drop_column('vehicles', 'is_children_allowed')
    op.drop_column('vehicles', 'is_food_allowed')
    op.drop_column('vehicles', 'has_dvd_player')
    op.drop_column('vehicles', 'is_smoking_allowed')
    op.drop_column('vehicles', 'has_gaming_console')
    op.drop_column('vehicles', 'has_dance_pole')
    op.drop_column('vehicles', 'has_air_conditioning')
    op.drop_column('vehicles', 'is_pets_allowed')
    op.drop_column('vehicles', 'has_luggage_space')
    op.drop_column('vehicles', 'has_trash_can')
    op.drop_column('vehicles', 'has_wifi')
    op.drop_column('vehicles', 'has_usb')
    op.drop_column('vehicles', 'has_aux')
    op.drop_column('vehicles', 'has_wheelchair_accessibility')
    op.drop_column('vehicles', 'has_onboard_bathroom')
    op.drop_column('vehicles', 'has_tv')
    op.drop_column('vehicles', 'has_ice_chest')
    op.drop_column('vehicles', 'has_refrigerator')
    op.drop_column('vehicles', 'has_karaoke')
    op.drop_column('vehicles', 'is_alcohol_allowed')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('is_alcohol_allowed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_karaoke', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_refrigerator', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_ice_chest', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_tv', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_onboard_bathroom', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_wheelchair_accessibility', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_aux', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_usb', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_wifi', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_trash_can', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_luggage_space', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('is_pets_allowed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_air_conditioning', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_dance_pole', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_gaming_console', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('is_smoking_allowed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_dvd_player', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('is_food_allowed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('is_children_allowed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_onboard_bar', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_bluetooth', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_tables', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('vehicles', sa.Column('has_power_outlets', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('vehicles', 'features')
    # ### end Alembic commands ###