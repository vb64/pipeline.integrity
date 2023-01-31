"""Material of the pipe."""


class Material:
    """Pipe material."""

    def __init__(self, name, yield_strength):
        """New material."""
        self.name = name
        self.yield_strength = yield_strength  # текучесть
        self.durability = None  # прочность
        self.toughness = None  # вязкость
        self.design_factor = 1  # from ASME B31.4, ASME B31.8 t or ASME B31.11
