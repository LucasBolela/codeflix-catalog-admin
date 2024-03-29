import uuid
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestSave:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(name="Filme", description="Categoria para filmes")

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category


class TestGetById:
    def test_can_found_category_by_id(self):
        category = Category(name="Filme", description="Categoria para filmes")
        repository = InMemoryCategoryRepository(categories=[category])

        response = repository.get_by_id(id=category.id)

        assert len(repository.categories) == 1
        assert response == Category(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

    def test_when_category_does_not_exists_should_return_none(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
        )
        repository = InMemoryCategoryRepository(
            categories=[
                category_filme,
            ]
        )

        category = repository.get_by_id(uuid.uuid4())

        assert category is None


class TestDeleteCategory:
    def test_can_delete_category_by_id(self):
        category = Category(name="Filme", description="Categoria para filmes")
        repository = InMemoryCategoryRepository(categories=[category])

        assert len(repository.categories) == 1
        assert repository.get_by_id(id=category.id) is not None
        response = repository.delete(id=category.id)

        assert len(repository.categories) == 0
        assert repository.get_by_id(id=category.id) is None
        assert response is None


class TestUpdate:
    def test_update_category(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série",
            description="Categoria para séries",
        )
        repository = InMemoryCategoryRepository(
            categories=[
                category_filme,
                category_serie,
            ]
        )

        category_filme.name = "Filmes"
        category_filme.description = "Categoria para filmes e séries"
        repository.update(category_filme)

        assert len(repository.categories) == 2
        updated_category = repository.get_by_id(category_filme.id)
        assert updated_category.name == "Filmes"
        assert updated_category.description == "Categoria para filmes e séries"

    def test_update_non_existent_category_does_not_raise_exception(self):
        repository = InMemoryCategoryRepository(categories=[])

        category = Category(
            name="Documentário",
            description="Categoria para documentários",
        )
        repository.update(category)

        assert len(repository.categories) == 0
