class IngredientFrame:
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


class PotionFrame:
    def __init__(self, name: str, ingredients: int) -> None:
        super().__init__()
        self.name = name
        self.ingredients = [None] * ingredients
