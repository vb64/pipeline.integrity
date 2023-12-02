# -*- coding: utf-8 -*-
"""Material of the pipe."""


class Material:
    """Pipe material."""

    def __init__(self, name, smys):
        """Create new material."""
        self.name = name
        self.smys = smys  # предел текучести
        self.smts = None  # предел прочности при растяжении
        self.toughness = None  # вязкость

    def __str__(self):
        """Return as text."""
        return "{} smys {} smts {}".format(
          self.name,
          round(self.smys, 2) if self.smys else '',
          round(self.smts, 2) if self.smts else ''
        )
