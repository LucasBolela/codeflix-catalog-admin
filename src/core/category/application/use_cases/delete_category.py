from uuid import UUID
from dataclasses import dataclass

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import (
    CategoryNotFound,
)


@dataclass
class DeleteCategoryRequest:
    id: UUID


class DeleteCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request=DeleteCategoryRequest) -> None:
        category = self.repository.get_by_id(id=request.id)

        if category is None:
            raise CategoryNotFound(f"Category with {request.id} not found")

        self.repository.delete(id=category.id)
