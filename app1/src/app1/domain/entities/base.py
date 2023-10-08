class Entity:
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __repr__(self):
        return (
            self.__class__.__qualname__
            + "("
            + ", ".join(
                "{0}={1!r}".format(*item) for item in self.__dict__.items()
            )
            + ")"
        )


class Value:
    def __repr__(self):
        return (
            self.__class__.__qualname__
            + "("
            + ", ".join(
                "{0}={1!r}".format(*item) for item in self.__dict__.items()
            )
            + ")"
        )
