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
