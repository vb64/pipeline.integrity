"""Material of the pipe."""


class Material:
    """Pipe material."""

    def __init__(self, name, yield_strength):
        """New material."""
        self.name = name
        self.yield_strength = yield_strength  # tekuchest
        self.durability = None  # prochnost
        self.toughness = None  # viazkost
        self.design_factor = 1  # from ASME B31.4, ASME B31.8 t or ASME B31.11
