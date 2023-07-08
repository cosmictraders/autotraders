import math


class PaginatedList:  # TODO: Don't use :param: for attrs
    """
    :param page: The current page
    :param num_per_page: The number of items per a page
    :param total: Total number of items
    :param pages: number of pages
    """

    def __init__(self, func, page, num_per_page=20):
        """
        A paginated list with caching
        :param func: Function to get page (must accept two ints denoting the page number and number of items per page
        and should return the data and total number of items)
        :param page: Page to start on
        :param num_per_page: How many items per a page
        """
        self.page = page
        self.func = func
        self.num_per_page = num_per_page
        data, total = self.func(self.page, self.num_per_page)
        self.inner = {self.page: data}
        self.total = total
        self.pages = math.ceil(self.total // self.num_per_page)

    def clear_cache(self):
        self.inner = {}

    def next(self):
        self.page += 1
        return self.current()

    def prev(self):
        self.page -= 1
        return self.current()

    def all(self):
        """Gets all the pages and returns the list of all pages"""
        for page in range(1, self.pages):
            self.page = page
            self.current()
        return self.stitch()

    def __getitem__(self, key):
        assert type(key) is int
        self.page = key
        return self.current()

    def current(self):
        if self.inner.get(self.page) is None:
            data, total = self.func(self.page, self.num_per_page)
            self.inner[self.page] = data
            self.total = total
            self.pages = math.ceil(self.total // self.num_per_page)
            return data
        else:
            return self.inner[self.page]

    def get(self):
        return self.current()

    def stitch(self):
        complete = []
        for key in self.inner:
            [complete.append(item) for item in self.inner[key]]
        return complete
