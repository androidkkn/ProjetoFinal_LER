"""Pacote de serviços do EduGrade."""

from services.calculadora import Calculadora
from services.boletim import GeradorBoletim
from services.persistencia import Persistencia

__all__ = ["Calculadora", "GeradorBoletim", "Persistencia"]
