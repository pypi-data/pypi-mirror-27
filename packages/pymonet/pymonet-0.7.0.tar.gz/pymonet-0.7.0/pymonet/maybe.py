class Maybe():

    def __init__(self, value, is_nothing):
        self.is_nothing = is_nothing
        if not is_nothing:
            self.value = value

    def __eq__(self, other):
        return isinstance(other, Maybe) and \
            self.is_nothing == other.is_nothing and \
            (self.is_nothing or self.value == other.value)

    @classmethod
    def just(cls, value):
        """
        creates not empty maybe
        :params value: value to store in Maybe
        :type Any
        :return Maybe<Any>
        """
        return Maybe(value, False)

    @classmethod
    def nothing(cls):
        """
        creates empty maybe
        :return Maybe<None>
        """
        return Maybe(None, True)

    def map(self, mapper):
        """
        if Maybe is empty return new empty Maybe, in other case
        takes mapper function and returns new instance of Maybe
        with result of mapper
        :params mapper: function to call with Maybe value
        :type (A) -> B
        :return Maybe<B | None>
        """
        if self.is_nothing:
            return Maybe.nothing()
        return Maybe.just(
            mapper(self.value)
        )

    def bind(self, mapper):
        """
        if Maybe is empty return new empty Maybe, in other case
        takes mapper function and returns result of mapper
        :params mapper: function to call with Maybe.value
        :type (A) -> Maybe<B>
        :return Maybe<B | None>
        """
        if self.is_nothing:
            return Maybe.nothing()
        return mapper(self.value)

    def filter(self, filterer):
        """
        if Maybe is empty or filterer returns False return default_value, in other case
        return new instance of Maybe with the same value
        :params filterer:
        :type (A) -> Boolean
        :returns Maybe<A> | Maybe<None>
        """
        if self.is_nothing or not filterer(self.value):
            return Maybe.nothing()
        return Maybe.just(self.value)

    def get_or_else(self, default_value):
        """
        if Maybe is empty return default_value, in other case
        returns Maybe.value
        :params default_value: value to return if Maybe is empty
        :type Any
        :returns A | Any
        """
        if self.is_nothing:
            return default_value
        return self.value

    def to_either(self):
        """
        Transform Maybe to Either
        :return Right monad with previous value when Maybe is not empty,
        in other case Left with None
        :type Either[A | None]
        """
        from pymonet.either import Left, Right

        if self.is_nothing:
            return Left(None)
        return Right(self.value)

    def to_box(self):
        """
        Transform Maybe to Box
        :return Box monad with previous value when Maybe is not empty,
        in other case Box with None
        :type Box[A | None]
        """
        from pymonet.box import Box

        if self.is_nothing:
            return Box(None)
        return Box(self.value)

    def to_lazy(self):
        """
        Transform Maybe to Try
        :return Lazy monad with function returning previous value
        in other case Left with None
        :type Lazy[() -> (A | None)]
        """
        from pymonet.lazy import Lazy

        if self.is_nothing:
            return Lazy(lambda: None)
        return Lazy(lambda: self.value)

    def to_try(self):
        """
        Transform Maybe to Try
        :return successfully Try with previous value when Maybe is not empty,
        in other case not successfully Try with None
        :type Try[A]
        """
        from pymonet.monad_try import Try

        if self.is_nothing:
            return Try(None, is_success=False)
        return Try(self.value, is_success=True)
