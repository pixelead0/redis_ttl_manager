.PHONY: all init run logs test cov

all: help

## Modo de uso de make
##---------------------------------------------------
##   make help                           | Muestra una lista de todos los comandos disponibles de make y su descripción.
help: Makefile
	@sed -n 's/^##//p' $< | cat

##   make init                           | Crea un entorno virtual, instala Poetry, y las dependencias del proyecto.
init:
	@rm -rf .venv && python3 -m venv .venv && . .venv/bin/activate && pip install poetry && poetry lock --no-update && poetry install
##   make run                            | Inicia la aplicación FastAPI con recarga automática.
run:
	@ . .venv/bin/activate && poetry run uvicorn main:app --reload

##   make test                           | Ejecuta todas las pruebas del proyecto usando Pytest.
##   make test FILE=tests/test_module.py | También puedes ejecutar un archivo de prueba específico.
test:
	@ . .venv/bin/activate && poetry run pytest $(FILE)
##   make cov                            | Genera un informe de cobertura de pruebas y un informe HTML.
cov:
	@ . .venv/bin/activate && poetry run coverage run -m pytest && poetry run coverage report -m && poetry run coverage html

