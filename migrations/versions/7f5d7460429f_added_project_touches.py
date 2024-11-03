"""added project touches

Revision ID: 7f5d7460429f
Revises: 2441a5cf9e6f
Create Date: 2024-11-02 10:42:42.378757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7f5d7460429f'
down_revision: Union[str, None] = '2441a5cf9e6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('category', 'id',
               existing_type=sa.UUID(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.drop_constraint('category_name_key', 'category', type_='unique')
    op.add_column('idea', sa.Column('project_id', sa.Uuid(), nullable=False))
    op.create_index('idx_idea_title_description', 'idea', ['title', 'description'], unique=False)
    op.drop_constraint('idea_category_id_fkey', 'idea', type_='foreignkey')
    op.create_foreign_key(None, 'idea', 'project', ['project_id'], ['id'])
    op.drop_column('idea', 'category_id')
    op.add_column('project', sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('project', sa.Column('url', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('project', sa.Column('creator_id', sa.Uuid(), nullable=False))
    op.add_column('project', sa.Column('creted_at', postgresql.TIMESTAMP(), nullable=True))
    op.create_foreign_key(None, 'project', 'user', ['creator_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project', type_='foreignkey')
    op.drop_column('project', 'creted_at')
    op.drop_column('project', 'creator_id')
    op.drop_column('project', 'url')
    op.drop_column('project', 'description')
    op.add_column('idea', sa.Column('category_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'idea', type_='foreignkey')
    op.create_foreign_key('idea_category_id_fkey', 'idea', 'category', ['category_id'], ['id'])
    op.drop_index('idx_idea_title_description', table_name='idea')
    op.drop_column('idea', 'project_id')
    op.create_unique_constraint('category_name_key', 'category', ['name'])
    op.alter_column('category', 'id',
               existing_type=sa.Integer(),
               type_=sa.UUID(),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###