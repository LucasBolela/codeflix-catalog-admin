from uuid import UUID
import uuid

import pytest
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.application.use_cases.exceptions import (
    CategoryNotFound,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestDeleteCategroy:
    def test_delete_category_from_repository(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série",
            description="Categoria para séries",
        )

        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )

        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=category_filme.id)

        assert repository.get_by_id(id=category_filme.id) is not None
        response = use_case.execute(request=request)

        assert repository.get_by_id(id=category_filme.id) is None
        assert response is None

    def test_when_category_does_not_exists_then_raise_exception(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série",
            description="Categoria para séries",
        )

        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )

        use_case = DeleteCategory(repository=repository)
        not_found_id = uuid.uuid4()
        request = DeleteCategoryRequest(id=not_found_id)

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)
