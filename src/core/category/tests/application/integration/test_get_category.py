from uuid import UUID
import uuid

import pytest
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from src.core.category.application.use_cases.exceptions import (
    CategoryNotFound,
    InvalidCategory,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestGetCategroy:
    def test_get_category_by_id(self):
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

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category_filme.id)

        response = use_case.execute(request=request)

        assert response == GetCategoryResponse(
            id=category_filme.id,
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )

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

        use_case = GetCategory(repository=repository)
        not_found_id = uuid.uuid4()
        request = GetCategoryRequest(id=not_found_id)

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)
