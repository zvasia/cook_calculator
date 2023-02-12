from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, SecretStr, EmailStr, Field


class GetIngredient(BaseModel):
    id: int | None
    name: str | None
    standard_unit_weight: Decimal | None
    standard_unit_volume: Decimal | None

    class Config:
        orm_mode = True


class CreateIngredient(GetIngredient):
    name: str


class GetCountry(BaseModel):
    id: int | None
    name: str | None
    short_name: str | None

    class Config:
        orm_mode = True


class CreateCountry(GetCountry):
    name: str

    class Config:
        orm_mode = True


class GetCookingStep(BaseModel):
    id: int | None
    num: int | None
    title: str | None
    description: str | None
    ingredients: list[GetIngredient] | None
    cooking_time: int | None

    class Config:
        orm_mode = True


class CreateCookingStep(BaseModel):
    num: int
    title: str
    description: str | None
    ingredients: list[CreateIngredient] | None
    cooking_time: int | None


class GetMeasure(BaseModel):
    id: int | None
    name: str | None
    volume: Decimal | None
    weight: Decimal | None
    country: GetCountry | None

    class Config:
        orm_mode = True


class CreateMeasure(GetMeasure):
    name: str
    country: CreateCountry | None


class GetRecipe(BaseModel):
    id: int | None
    name: str | None
    description: str | None
    cook_time: int | None
    ingredients: list[GetIngredient] | None
    steps: list[GetCookingStep] | None

    class Config:
        orm_mode = True


class CreateRecipe(BaseModel):
    name: str
    description: str | None
    cook_time: int | None
    ingredients: list[CreateIngredient]
    steps: list[CreateCookingStep]


