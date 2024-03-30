import pytest
from uuid import UUID
from unittest.mock import MagicMock


from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
    InvalidCategory,
)


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name="Filme",
            description="Filmes em geral",
            is_active=True,
        )

        response = use_case.execute(request=request)

        assert response.id is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called is True

    def test_create_category_with_invalid_data(self):
        use_case = CreateCategory(repository=MagicMock(CategoryRepository))

        with pytest.raises(InvalidCategory, match="name cannot be empty"):
            use_case.execute(CreateCategoryRequest(name=""))
