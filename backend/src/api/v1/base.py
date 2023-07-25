from fastapi import Query


class Paginator:
    """Класс для получения запроса страницы."""

    def __init__(
        self,
        page_number: int = Query(default=1, description='Номер страницы', ge=1),
        page_size: int = Query(default=10, description='Размер страницы', ge=1, le=100),
    ):
        """
        При инициализации класса принимает в запросе параметры номера страницы и её размера.

        Args:
            page_number: Номер страницы
            page_size: Размер страницы
        """
        self.offset = (page_number - 1) * page_size if page_number > 1 else 0
        self.limit = page_size

    @property
    def slice(self) -> slice:
        """Срез/часть списка объектов для получения требуемой страницы.

        Returns:
            slice: Срез списка
        """
        return slice(self.offset, self.offset + self.limit)
