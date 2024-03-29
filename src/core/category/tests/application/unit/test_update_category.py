from unittest.mock import create_autospec
import uuid

import pytest
from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import (
    CategoryNotFound,
    InvalidCategory,
)
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category


class TestUpdateCategory:
    @pytest.fixture
    def category(self) -> Category:
        return Category(
            name="Filme", description="Categoria para filmes", is_active=True
        )

    @pytest.fixture
    def mock_repository(self, category: Category) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category
        return repository

    def test_update_category_name(
        self, category: Category, mock_repository: CategoryRepository
    ):

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, name="Série")
        use_case.execute(request=request)

        assert category.name == "Série"
        assert category.description == "Categoria para filmes"
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(
        self, category: Category, mock_repository: CategoryRepository
    ):

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id, description="Categoria para séries"
        )
        use_case.execute(request=request)

        assert category.name == "Filme"
        assert category.description == "Categoria para séries"
        mock_repository.update.assert_called_once_with(category)

    def test_can_deactivate_category(
        self, category: Category, mock_repository: CategoryRepository
    ):

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, is_active=False)
        use_case.execute(request=request)

        assert category.is_active == False
        assert category.name == "Filme"
        assert category.description == "Categoria para filmes"
        mock_repository.update.assert_called_once_with(category)

    def test_can_activate_category(
        self, category: Category, mock_repository: CategoryRepository
    ):

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, is_active=True)
        use_case.execute(request=request)

        assert category.is_active == True
        assert category.name == "Filme"
        assert category.description == "Categoria para filmes"
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_name_and_description(
        self, category: Category, mock_repository: CategoryRepository
    ):
        use_case = UpdateCategory(mock_repository)
        use_case.execute(
            UpdateCategoryRequest(
                id=category.id, name="Séries", description="Categoria de séries"
            )
        )

        assert category.name == "Séries"
        assert category.description == "Categoria de séries"
        mock_repository.update.assert_called_once_with(category)

    def test_when_category_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)

        mock_repository.update.assert_not_called()
        assert str(exc.value) == f"Category with {request.id} not found"

    def test_when_category_is_updated_to_invalid_state_then_raise_exception(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ) -> None:
        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="",  # Invalid
        )

        with pytest.raises(InvalidCategory) as exc:
            use_case.execute(request)

        mock_repository.update.assert_not_called()
        assert str(exc.value) == "name cannot be empty"
