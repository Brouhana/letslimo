"""empty message

Revision ID: 289f1fd81bef
Revises: 4ab2589c4bc8
Create Date: 2022-05-22 22:13:39.450609

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '289f1fd81bef'
down_revision = '4ab2589c4bc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trips_stops')
    op.drop_column('trips', 'has_stops')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trips', sa.Column('has_stops', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.create_table('trips_stops',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('trip_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('is_flight', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('airport', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('flight_code', sa.VARCHAR(length=6), autoincrement=False, nullable=True),
    sa.Column('stop_datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('stop_pax', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('last_updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='trips_stops_company_id_fkey'),
    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], name='trips_stops_trip_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='trips_stops_pkey')
    )
    # ### end Alembic commands ###