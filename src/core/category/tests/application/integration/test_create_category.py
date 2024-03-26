from uuid import UUID

import pytest
from src.core.category.application.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
)
from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestCreateCategroy:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="Filme",
            description="Filmes em geral",
            is_active=True,
        )

        response = use_case.execute(request=request)

        assert response.id is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1

        persisted_category = repository.categories[0]
        assert persisted_category.id == response.id
        assert persisted_category.name == "Filme"
        assert persisted_category.description == "Filmes em geral"
        assert persisted_category.is_active == True

    def test_create_category_with_invalid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)

        with pytest.raises(InvalidCategoryData, match="name cannot be empty"):
            use_case.execute(CreateCategoryRequest(name=""))

        assert len(repository.categories) == 0
