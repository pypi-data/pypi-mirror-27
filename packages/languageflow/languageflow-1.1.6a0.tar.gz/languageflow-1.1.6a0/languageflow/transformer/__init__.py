import abc


class Transformer(abc.ABC):
    @abc.abstractmethod
    def transform(self):
        pass

    @abc.abstractmethod
    def fit_transform(self):
        pass
