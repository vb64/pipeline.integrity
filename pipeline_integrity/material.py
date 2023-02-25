# -*- coding: utf-8 -*-
"""Material of the pipe."""


class Material:
    """Pipe material."""

    def __init__(self, name, smys):
        """New material."""
        self.name = name
        self.smys = smys  # предел текучести
        self.smts = None  # предел прочности при растяжении
        self.toughness = None  # вязкость
