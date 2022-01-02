from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    '''
    Стандартный пагинатор.
    Переименовано имя параметра под требования фронтенда.
    '''
    page_size_query_param = 'limit'
