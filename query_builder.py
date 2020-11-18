import datetime

class QueryBuilder():
    """
    This class builds the query filters for the base url so that we request only the filtered data.
    """
    def __init__(self, base_url, fields, n_results, order_by, ascending = True):
        self.datetime_now = datetime.datetime.now()
        self.base_url = base_url
        self.fields = fields
        self.n_results = int(n_results)
        self.order_by = order_by
        self.ascending = ascending
        self.offset = int(0)

    def format_time(self):
        """
        This function converts the current datetime to 24 hour format HH:MM
        """
        time_filter = "\'{0}:{1}\'".format(
            str(self.datetime_now.hour).zfill(2),
            str(self.datetime_now.minute).zfill(2)
        )

        return time_filter

    def get_dayorder(self):
        """
        Return 1 for Monday, 2 for Tuesday, etc.
        """
        return self.datetime_now.isoweekday()

    def query(self):
        """
        Appends all the filters for fields, time filter, order by clause, number of results, and offset.
        This also handles increasing the offset for the next query.
        """
        query_url = (
            "?$select={0}"
            "&$where={1} BETWEEN start24 AND end24 AND dayorder={5}"
            "&$order={2}"
            "&$limit={3}"
            "&$offset={4}").format(
                                    ", ".join(self.fields),
                                    self.format_time(),
                                    self.order_by + (" ASC" if self.ascending else " DESC"),
                                    self.n_results,
                                    self.offset,
                                    self.get_dayorder())

        self.offset += self. n_results

        return query_url