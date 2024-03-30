from uuid import uuid4
import pytest
from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category
from django_project.category_app.models import Category as CategoryModel


@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(self):
        category = Category(name="Movie", description="Movie description")
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category=category)

        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get()
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active


@pytest.mark.django_db
class TestGetById:
    def test_get_category_by_id_in_database(self):
        category_movie = Category(name="Movie", description="Movie description")
        category_documentary = Category(
            name="Documentary", description="Documentary description"
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category=category_movie)
        repository.save(category=category_documentary)

        assert CategoryModel.objects.count() == 2

        categories_db = repository.get_by_id(id=category_movie.id)
        assert categories_db == category_movie

    def test_get_invalid_category_by_id_in_database(self):
        category_movie = Category(name="Movie", description="Movie description")
        category_documentary = Category(
            name="Documentary", description="Documentary description"
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category=category_movie)
        repository.save(category=category_documentary)

        assert CategoryModel.objects.count() == 2

        categories_db = repository.get_by_id(id=uuid4())
        assert categories_db == None


@pytest.mark.django_db
class TestList:
    def test_list_all_categories_in_database(self):
        category_movie = Category(name="Movie", description="Movie description")
        category_documentary = Category(
            name="Documentary", description="Documentary description"
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category=category_movie)
        repository.save(category=category_documentary)

        assert CategoryModel.objects.count() == 2

        categories_db = repository.list()
        assert len(categories_db) == 2
        assert categories_db == [
            category_movie,
            category_documentary,
        ]

    def test_list_empty_categories_in_database(self):
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0

        categories_db = repository.list()
        assert len(categories_db) == 0
        assert categories_db == []


@pytest.mark.django_db
class TestDelete:
    def test_delete_category_in_database(self):
        category_movie = Category(name="Movie", description="Movie description")
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category=category_movie)

        assert CategoryModel.objects.count() == 1

        repository.delete(id=category_movie.id)
        assert CategoryModel.objects.count() == 0

    def test_delete_invalid_category_in_database(self):
        category_movie = Category(name="Movie", description="Movie description")
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category=category_movie)

        assert CategoryModel.objects.count() == 1

        repository.delete(id=uuid4())
        assert CategoryModel.objects.count() == 1


@pytest.mark.django_db
class TestUpdate:
    def test_update_name_and_description_from_category_in_database(self):
        category_movie = Category(name="Movie", description="Movie description")
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category=category_movie)

        assert CategoryModel.objects.count() == 1

        category_serie = category_movie
        category_serie.name = "Series"
        category_serie.descritption = "Series description"

        repository.update(category=category_serie)
        assert repository.get_by_id(id=category_serie.id) == category_serie

    def test_update_activate_category_in_database(self):
        category_movie = Category(
            name="Movie", description="Movie description", is_active=False
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category=category_movie)

        assert CategoryModel.objects.count() == 1

        current_category = category_movie
        current_category.is_active = True

        repository.update(category=current_category)
        updated_category = repository.get_by_id(id=current_category.id)
        assert updated_category == current_category
        assert updated_category.is_active == True

    def test_update_deactivate_category_in_database(self):
        category_movie = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category=category_movie)

        assert CategoryModel.objects.count() == 1

        current_category = category_movie
        current_category.is_active = False

        repository.update(category=current_category)
        updated_category = repository.get_by_id(id=current_category.id)
        assert updated_category == current_category
        assert updated_category.is_active == False
