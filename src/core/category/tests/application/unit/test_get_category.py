import uuid
import pytest
from uuid import UUID
from unittest.mock import create_autospec


from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from src.core.category.domain.category import Category


class TestGetCategory:
    def test_return_found_category(self):
        category = Category(
            name="Filme", description="Categoria para filmes", is_active=True
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=category.id)
        response = use_case.execute(request=request)

        assert response.id is not None
        assert isinstance(response, GetCategoryResponse)
        assert isinstance(response.id, UUID)
        assert response == GetCategoryResponse(
            id=category.id,
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )

    def test_return_category_not_found(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryNotFound):
            use_case.execute(request)
