from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import AuthController, RecipeController, IngredientController, PantryController, DietaryRestrictionController
from core.db import Base, engine
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthController.router, prefix="/auth", tags=["Authentication"])

app.include_router(RecipeController.router, prefix="/api/v1", tags=["Recipes"], )

app.include_router(PantryController.router, prefix="/api/v1", tags=["Pantry"])

app.include_router(IngredientController.router, prefix="/api/v1", tags=["Ingredients"])

app.include_router(DietaryRestrictionController.router, prefix="/api/v1", tags=["DietaryRestriction"])