import logging
from enum import Enum

from fastapi import APIRouter, Depends, Body, Query
from pony.orm import db_session, select, commit
from app.models import Recipe, Ingredient, CookingStep, Measure, Country
import app.schemas as schemas

logger = logging.getLogger(__name__) 
router = APIRouter()


def clear_dict(source_dict):
    dict_without_nones = {}
    for k, v in source_dict.items():
        if v:
            dict_without_nones[k] = v
    return dict_without_nones


# Measure CRUD

@router.get('/measure')
@db_session
def get_measures(model: schemas.GetMeasure = Depends()) -> list[schemas.GetMeasure]:
    data_for_filter = clear_dict(model.dict())
    measures = list(select(m for m in Measure).filter(**data_for_filter))
    return measures


@router.post('/measure')
@db_session
def get_or_create_measure(model: schemas.CreateMeasure) -> schemas.GetMeasure:
    measure_data = model.dict(exclude={'id'})
    if measure_data.get('country'):
        logger.error(measure_data)
        measure_data['country'] = get_or_create_country(schemas.CreateCountry(**measure_data.get('country')))
        
    measure_in_db = select(m for m in Measure).filter(**measure_data)
    if not measure_in_db.exists():
        measure = Measure(**measure_data)
    else:
        measure = measure_in_db.first()
    return measure


@router.put('/measure')
@db_session
def update_measure(update_model: schemas.GetMeasure, model: schemas.GetMeasure = Depends()) -> schemas.GetMeasure:
    model_data = clear_dict(model.dict())
    update_model_data = clear_dict(update_model.dict())
    measure = Measure.get(**model_data)
    for k, v in update_model_data.items():
        setattr(measure, k, v)
    return measure


@router.patch('/measure')
@db_session
def delete_measure(model: schemas.GetMeasure = Depends()):
    model_data = clear_dict(model.dict())
    measure = Measure.get(**model_data)
    measure.delete()
    commit()
    return {'response': 'measure deleted successfully'}


# Recipes CRUD

@router.get('/recipe')
@db_session
def get_recipes(model: schemas.GetRecipe = Depends()) -> list[schemas.GetRecipe]:
    data_for_filter = clear_dict(model.dict())
    recipes = list(select(r for r in Recipe).filter(**data_for_filter))
    return recipes


@router.post('/recipe')
@db_session
def get_or_create_recipe(model: schemas.CreateRecipe) -> schemas.GetRecipe:
    recipe_data = clear_dict(model.dict(exclude={'id'}))
    if recipe_data.get('ingredients'):
        ingredient_objects = []
        for ingredient in recipe_data.get('ingredients'):
            ingredient_objects.append(get_or_create_ingredient(schemas.CreateIngredient(**ingredient)))
        recipe_data['ingredients'] = ingredient_objects
    if recipe_data.get('steps'):
        step_objects = []
        for step in recipe_data.get('steps'):
            step_objects.append(get_or_create_cooking_step(schemas.CreateCookingStep(**step)))
        recipe_data['steps'] = step_objects
    recipe_in_db = select(r for r in Recipe).filter(**recipe_data)
    if not recipe_in_db.exists():
        recipe = Recipe(**recipe_data)
    else:
        recipe = recipe_in_db.first()
    return recipe


@router.put('/recipe')
@db_session
def update_recipe(update_model: schemas.GetRecipe, model: schemas.GetRecipe = Depends()) -> schemas.GetRecipe:
    model_data = clear_dict(model.dict())
    update_model_data = clear_dict(update_model.dict())
    recipe = Recipe.get(**model_data)
    for k, v in update_model_data.items():
        setattr(recipe, k, v)
    return recipe


@router.patch('/recipe')
@db_session
def delete_recipe(model: schemas.GetRecipe = Depends()):
    model_data = clear_dict(model.dict())
    country = Recipe.get(**model_data)
    country.delete()
    commit()
    return {'response': 'deleted successfully'}


# Ingredients CRUD

@router.get('/ingredient')
@db_session
def get_ingredients(model: schemas.GetIngredient = Depends()) -> list[schemas.GetIngredient]:
    data_for_filter = clear_dict(model.dict())
    recipes = list(select(i for i in Ingredient).filter(**data_for_filter))
    return recipes


@router.post('/ingredient')
@db_session
def get_or_create_ingredient(model: schemas.CreateIngredient) -> schemas.GetIngredient:
    ingredient_data = clear_dict(model.dict(exclude={'id'}))
    ingredient_in_db = select(i for i in Ingredient).filter(**ingredient_data)
    if not ingredient_in_db.exists():
        ingredient = Ingredient(**ingredient_data)
    else:
        ingredient = ingredient_in_db.first()
    return ingredient


@router.put('/ingredient')
@db_session
def update_ingredient(update_model: schemas.GetIngredient, model: schemas.GetIngredient = Depends()) -> schemas.GetIngredient:
    model_data = clear_dict(model.dict())
    update_model_data = clear_dict(update_model.dict())
    recipe = Ingredient.get(**model_data)
    for k, v in update_model_data.items():
        setattr(recipe, k, v)
    return recipe


@router.patch('/ingredient')
@db_session
def delete_ingredient(model: schemas.GetIngredient = Depends()):
    model_data = clear_dict(model.dict())
    country = Ingredient.get(**model_data)
    country.delete()
    commit()
    return {'response': 'deleted successfully'}


# Steps CRUD

@router.get('/cooking_step')
@db_session
def get_step(model: schemas.GetCookingStep = Depends()) -> list[schemas.GetCookingStep]:
    data_for_filter = clear_dict(model.dict())
    cooking_steps = list(select(c for c in CookingStep).filter(**data_for_filter))
    return cooking_steps


@router.post('/cooking_step')
@db_session
def get_or_create_cooking_step(model: schemas.CreateCookingStep) -> schemas.GetCookingStep:
    cooking_step_data = clear_dict(model.dict(exclude={'id'}))
    if cooking_step_data.get('ingredients'):
        ingredient_objects = []
        for ingredient in cooking_step_data.get('ingredients'):
            ingredient_objects.append(get_or_create_ingredient(schemas.CreateIngredient(**ingredient)))
        cooking_step_data['ingredients'] = ingredient_objects
    cooking_step_in_db = select(c for c in CookingStep).filter(**cooking_step_data)
    if not cooking_step_in_db.exists():
        cooking_step = CookingStep(**cooking_step_data)
    else:
        cooking_step = cooking_step_in_db.first()
    return cooking_step


@router.put('/cooking_step')
@db_session
def update_cooking_step(update_model: schemas.GetCookingStep,
                        model: schemas.GetCookingStep = Depends()) -> schemas.GetCookingStep:
    model_data = clear_dict(model.dict())
    update_model_data = clear_dict(update_model.dict())
    cooking_step = CookingStep.get(**model_data)
    for k, v in update_model_data.items():
        setattr(cooking_step, k, v)
    return cooking_step


@router.patch('/cooking_step')
@db_session
def delete_cooking_step(model: schemas.GetCookingStep = Depends()):
    model_data = clear_dict(model.dict())
    cooking_step = CookingStep.get(**model_data)
    cooking_step.delete()
    commit()
    return {'response': 'deleted successfully'}


