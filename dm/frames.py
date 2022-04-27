class IngredientFrame:
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


class PolyjuiceFrame:
    name = 'polyjuice'

    def __init__(self) -> None:
        super().__init__()
        self._ingredient1 = None
        self._ingredient2 = None
        self._ingredient3 = None
        self._ingredient4 = None
        self._ingredient5 = None
        self._ingredient6 = None
        self._ingredient7 = None

    def set_ingredient(self, ingredient):
        for attribute, value in self.__dict__.items():
            if value is None:
                setattr(self, attribute, ingredient)
                break

    def is_complete(self):
        ing = 0
        for attribute, value in self.__dict__.items():
            if value is not None:
                ing += 1
        return float(ing * 100 / len(self.__dict__.items()))

    def show_attributes(self):
        for attribute, value in self.__dict__.items():
            if value is not None:
                print(attribute, '=', value.name)
            else:
                print(attribute, '=', value)


class ArmadilloBileMixtureFrame:
    name = 'armadillo bile mixture'

    def __init__(self) -> None:
        super().__init__()
        self._ingredient1 = None
        self._ingredient2 = None
        self._ingredient3 = None
        self._ingredient4 = None
        self._ingredient5 = None
        self._ingredient6 = None
        self._ingredient7 = None

    def set_ingredient(self, ingredient):
        for attribute, value in self.__dict__.items():
            if value is None:
                setattr(self, attribute, ingredient)
                break

    def is_complete(self):
        ing = 0
        for attribute, value in self.__dict__.items():
            if value is not None:
                ing += 1
        return float(ing * 100 / len(self.__dict__.items()))

    def show_attributes(self):
        for attribute, value in self.__dict__.items():
            if value is not None:
                print(type(value))
                print(attribute, '=', value.name)
            else:
                print(attribute, '=', value)


class AnimagusFrame:
    name = 'animagus'

    def __init__(self) -> None:
        super().__init__()
        self._ingredient1 = None
        self._ingredient2 = None
        self._ingredient3 = None
        self._ingredient4 = None

    def set_ingredient(self, ingredient):
        for attribute, value in self.__dict__.items():
            if value is None:
                setattr(self, attribute, ingredient)
                break

    def is_complete(self):
        ing = 0
        for attribute, value in self.__dict__.items():
            if value is not None:
                ing += 1
        return float(ing * 100 / len(self.__dict__.items()))

    def show_attributes(self):
        for attribute, value in self.__dict__.items():
            print(type(value))
            if value is not None:
                print(attribute, '=', value.name)
            else:
                print(attribute, '=', value)
