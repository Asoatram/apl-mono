import json
import re

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from repository.PantryRepository import PantryRepository
from repository.RecipeRepository import RecipeRepository
import os
from openai import OpenAI
load_dotenv()
client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_URL")
    )

class RecipeService:


    @staticmethod
    async def get_recipe_from_id(db:AsyncSession, id):
        return await RecipeRepository.get_recipe_details(db, id)

    @staticmethod
    async def get_recipe_paginated(db:AsyncSession, page, per_page):
        return await RecipeRepository.get_recipe_pagination(db, page, per_page)

    @staticmethod
    async def post_recipe(db:AsyncSession, recipe):
        return await RecipeRepository.create_recipe(db, recipe)

    @staticmethod
    async def delete_recipe(db:AsyncSession, recipe_id):
        return await RecipeRepository.delete_recipe(db, recipe_id)

    @staticmethod
    async def save_recipe(db:AsyncSession, user_id, recipe_id):
        return await RecipeRepository.save_recipe(db, user_id, recipe_id)

    @staticmethod
    async def ask_for_tips(user_message):
        message = [
            {"role": "system", "content": """
            You are a highly trained culinary expert with professional kitchen experience. Your role is to help a home cook solve specific cooking problems with clear, precise, and technically accurate advice. Keep it short and simple. Speak with authority, avoid casual language or personal stories, and focus only on practical, reliable solutions suitable for a home kitchen. Do not use emojis or unnecessary flourishes.
            """},
            {"role": "user", "content": user_message}
        ]
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=message,
        )
        return response.choices[0].message.content

    @staticmethod
    async def ask_for_recipe(db, user_id):
        available_ingredients_list = []
        ingredients_list = await PantryRepository.get_pantry_ingredients_by_userid(db, user_id)
        for ingredient in ingredients_list.pantry_ingredients:
            available_ingredients_list.append(ingredient.ingredient.name)
        message = [
            {"role": "system", "content": """
            You are a highly trained culinary expert with professional kitchen experience. Your role is to help a home cook solve specific cooking problems with clear, precise, and technically accurate advice. Keep it short and simple. Speak with authority, avoid casual language or personal stories, and focus only on practical, reliable solutions suitable for a home kitchen. Do not use emojis or unnecessary flourishes.
            Return raw JSON, Do not wrap it in a code block or any markdown. Make sure that the result is possible with `json.loads`, the json have the following formats:
            {
                "recipe_name": "Spaghetti Bolognese",
                "description": "A classic Italian pasta dish with a rich meat sauce.",
                "ingredients": [
                    {
                        "ingredient_name": "Spaghetti"
                    },
                    {
                        "ingredient_name": "Ground Beef"
                    },
                    {
                        "ingredient_name": "Tomato Sauce"
                    },
                    {
                        "ingredient_name": "Onion"
                    },
                    {
                        "ingredient_name": "Garlic"
                    }
                ],
                "steps": [
                    {
                        "step_order": 1,
                        "step_description": "Boil spaghetti until al dente."
                    },
                    {
                        "step_order": 2,
                        "step_description": "Sauté onion and garlic."
                    },
                    {
                        "step_order": 3,
                        "step_description": "Add ground beef and cook thoroughly."
                    },
                    {
                        "step_order": 4,
                        "step_description": "Stir in tomato sauce and simmer."
                    },
                    {
                        "step_order": 5,
                        "step_description": "Combine with spaghetti and serve."
                    }
                ]
            }
            """
            },
            {"role": "user", "content": f"I have a {[ingredient for ingredient in available_ingredients_list]}"}
        ]
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=message,
        )
        result = response.choices[0].message.content
        cleaned = re.sub(r'^```(?:json)?\n|\n```$', '', result.strip())
        print(cleaned)
        result = json.loads(cleaned)
        return result

