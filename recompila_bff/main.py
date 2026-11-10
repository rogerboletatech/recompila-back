"""Ponto de entrada para uvicorn: uvicorn recompila_bff.main:app"""

from recompila_bff.app import create_app

app = create_app()
