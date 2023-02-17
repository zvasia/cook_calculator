import app.settings as settings
from datetime import datetime, date
from decimal import Decimal


from pony.orm import Database, Required, Optional, Set, LongStr, PrimaryKey, db_session

db = Database()
db.bind(
    provider='postgres',
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    database=settings.DB_NAME
)


class ModelMixin(object):
    pass
    # @db_session
    # def get_all(self):
    #     print(self.select()[:])


class User(db.Entity, ModelMixin):
    id = PrimaryKey(int, auto=True)
    login = Required(str, unique=True)
    name = Optional(str, nullable=True)
    password = Required(str)
    recipes = Set("Recipe")
    last_login = Optional(datetime)
    create_date = Required(date, default=datetime.now().date())


class Country(db.Entity, ModelMixin):
    _table_ = 'country'
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    short_name = Optional(str, nullable=True)
    code = Optional(int, nullable=True)
    measures = Set("Measure")


# class NameAlias(db.Entity, ModelMixin):
#     _table_ = 'name_alias'
#
#     id = PrimaryKey(int, auto=True)
#     name = Required(str)
#     measures = Set("Measure")
#     ingredients = Set("Ingredient")
#     recipe = Set("Recipe")


# class Tag(db.Entity, ModelMixin):
#     id = PrimaryKey(int, auto=True)
#     name = Required(str)
#     ingredients = Set("Ingredient")
#     recipe = Set("Recipe")


class Measure(db.Entity, ModelMixin):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    volume = Optional(Decimal, )
    weight = Optional(Decimal)
    country = Optional(Country)


class Ingredient(db.Entity, ModelMixin):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    standard_unit_weight = Optional(Decimal)
    standard_unit_volume = Optional(Decimal)
    # name_aliases = Set(NameAlias, table='ingredient_name_aliases')
    # tags = Set(Tag, table='ingredient_tags')
    create_date = Required(date, default=datetime.now().date())
    cooking_steps = Set("CookingStep")
    recipes = Set("Recipe", table='ingredient_recipes')


class CookingStep(db.Entity, ModelMixin):
    _table_ = 'cooking_step'

    id = PrimaryKey(int, auto=True)
    num = Required(int)
    title = Required(str)
    description = Required(LongStr)
    ingredients = Set(Ingredient, table='cooking_step_ingredients')
    recipe = Required("Recipe")


class Recipe(db.Entity, ModelMixin):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    # slug = Optional(str, sql_default=generate_slug)
    description = Optional(LongStr)
    cook_time = Optional(int)  # in minutes
    ingredients = Set(Ingredient)
    steps = Set(CookingStep)
    # name_aliases = Set(NameAlias, table='recipes_name_aliases')
    # tags = Set(Tag, table='recipe_tags')
    author = Optional(User, sql_default=1)
    source = Optional(LongStr)
    create_date = Required(date, default=datetime.now().date())


db.generate_mapping(create_tables=True)
