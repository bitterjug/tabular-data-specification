class Column(object):

    def __init__(self, *input_keys, **kwargs):
        """

        positionalk params:

        :input_keys:
            a list of input data keys required in the context
            dictionary to produce the out put value

        keyword arguments:

        :header:
            text for the spreadsheet header row. If not specified the
            name of the first (only?) input_key is used

        :reduce:
            an optional function to reduce a list of values into one

        :function:
            is an optional transformation function to perform on the reduced
            value

        :default:
            is an optional value to use instead of null if an input key is not
            found in the context dictionary. Note that if the key is there with
            value None, then you still get None, not this default.

        """
        def first_identity(*x):
            """ like the identity function (lambda x: x)
            but works with multiple args too, in which case
            it returns the first
            """
            return x[0]
        self.fn = kwargs.get('function', first_identity)
        self.rx = kwargs.get('reduce', None)
        self.default = kwargs.get('default')
        self.keys = list(input_keys)
        self.header = kwargs.get('header', self.keys[0])

    def inputs(self):
        return self.keys

    def value(self, context):
        vals = [context.get(key, self.default) for key in self.keys]
        if self.rx:
            return self.fn(self.rx(vals))
        else:
            return self.fn(*vals)


class ColumnSpecification(object):
    """
    Columns specification for spreadsheet export.
    Spreadsheet wants list of lists with headers in first row.
    We can easily get a dictionary of data using queryset.values(...)
    These classes enable a declarative style specification of the
    mapping from these dicts to the spreadsheet rows.
    """

    def __init__(self, *cols):
        """
        Expects a list of Column() objects as parameters
        """
        self.cols = cols

    def inputs(self):
        """
        Returns a flat list of the input keys required in the
        context dictionary to satisfy all the cols
        """
        return sum([col.inputs() for col in self.cols], [])

    def values(self, context):
        """
        Returns the spreadsheet data row
        """
        return [col.value(context) for col in self.cols]

    def headers(self):
        """
        Returns the spreadsheet header row
        """
        return [col.header for col in self.cols]

    def related(self):
        """
        Returns the set of field names leading to relatd models
        to be included in the queryset. (derived from the prefixes
        up to double-underscore in the input keys)
        """
        sep = '__'
        return set([key.partition(sep)[0]
            for key in self.inputs()
            if key.find(sep) >= 0])
