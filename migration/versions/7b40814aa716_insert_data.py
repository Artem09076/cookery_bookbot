"""insert data

Revision ID: 7b40814aa716
Revises: 95ddab1c7567
Create Date: 2024-12-09 17:15:39.681998

"""
from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b40814aa716'
down_revision: Union[str, None] = '95ddab1c7567'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Insert initial data into user table
    connection = op.get_bind()
    connection.execute(
        sa.text("""
        INSERT INTO "user" (user_id, registered) VALUES
        (1, :registered),
        (2, :registered);
        """),
        {'registered': datetime.utcnow()}
    )

    # Insert initial data into recipe table
    connection.execute(
        sa.text("""
        INSERT INTO "recipe" (id, recipe_title, ingredients, description_recipe, likes, dislikes, user_id) VALUES
        (:id1, 'Recipe 1', '["ingredient1", "ingredient2"]', 'Description for recipe 1', 0, 0, 1),
        (:id2, 'Recipe 2', '["ingredient3", "ingredient4"]', 'Description for recipe 2', 0, 0, 2);
        """),
        {
            'id1': str(uuid4()),
            'id2': str(uuid4())
        }
    )

def downgrade():
    connection = op.get_bind()
    connection.execute(sa.text('DELETE FROM "recipe" WHERE user_id IN (1, 2);'))
    connection.execute(sa.text('DELETE FROM public."user" WHERE user_id IN (1, 2);'))
