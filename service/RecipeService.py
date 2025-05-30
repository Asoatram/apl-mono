from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

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


