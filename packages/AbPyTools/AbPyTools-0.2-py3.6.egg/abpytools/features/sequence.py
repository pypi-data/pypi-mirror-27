from abpytools import ChainCollection

AVAILABLE_DATABASES = ["charge", "hydrophobicity", "type"]


class ChainSequence(ChainCollection):

    """
    """

    def __init__(self, antibody_objects=None, path=None):
        super().__init__(antibody_objects=antibody_objects, path=path)

    def amino_acid_features(self, database, discrete=None):

        if database not in AVAILABLE_DATABASES:
            self._make_database(database)
        else:
            self.database = database

        if discrete is not None:
            self._make_discrete(self.database)

        pass

    def transform(self):
        pass

    def fit_transform(self, database):
        self.amino_acid_features(database=database)
        return self.transform()

    def _make_database(self, database):

        if not isinstance(database, dict):
            raise TypeError()

        if len(database) != 20:
            raise ValueError()

        self.database = database

    def _make_discrete(self, database, discrete_range):
        database = _check_range(database, discrete_range)


def _check_range(database, discrete_range):
    if discrete_range[0] < min(database):
        raise ValueError
    if discrete_range[-1] > max(database):
        raise ValueError

    return database
