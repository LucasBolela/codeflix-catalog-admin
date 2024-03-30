from uuid import uuid4
import pytest
from rest_framework.test import APIClient
from rest_framework import status

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_movie() -> Category:
    return Category(name="Movie", description="Movie description")


@pytest.fixture
def category_documentary() -> Category:
    return Category(name="Documentary", description="Documentary description")


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:

        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = "/api/categories/"
        response = APIClient().get(url)

        expected_data = [
            {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            },
            {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active,
            },
        ]
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_when_id_is_invalid_return_400(self):
        url = f"/api/categories/123123123/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exists(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = f"/api/categories/{category_documentary.id}/"
        response = APIClient().get(url)

        expected_data = {
            "id": str(category_documentary.id),
            "name": category_documentary.name,
            "description": category_documentary.description,
            "is_active": category_documentary.is_active,
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_not_exists(self) -> None:
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
