# Estructura de directorios recomendada para un proyecto FastAPI

1. pip install uv -> si no está instalado aún
2. uv init
3. uv venv
4. uv add dependencias -> agregar librerías, pero si simplemente quieres usar lo que ya existe en otro proyecto, solo copia el archivo pyproject y el uv.lock y pegalo en este proyecto, después solo ejecuta uv sync.

5. uv add alembic
6. uv run alembic init migrations
7. realiza los cambios en los archivos alembic.ini y env.py de versions con el fin de que se conecte alembic con sqlalchemy y se detecten lso cambios.
8. uv run alembic revision --autogenerate -m "comments" -> crea las migraciones automática
9. uv run alembic upgrade head -> carga los cambios en los modelos usados
10. uv run pre-commit install -> instala los pre-commit hooks, para que se ejecuten antes de cada commit con el fin de que se ejecuten las pruebas y se corrijan los errores.
11. ejecutar los test, solo es usar el comando pytest
12. uv run uvicorn src.app.main:app --app-dir src -> ejecuta la aplicación
13. git status -> ver los cambios
14. git add . -> agrega los archivos modificados al stage
15. git commit -m "message" -> crea el commit con el mensaje de los cambios
16. git push -> sube los cambios al repositorio



¿Qué ganas con esta estructura?

✅ Async real
✅ Escala mejor
✅ Ideal para IA
✅ API limpia
✅ Fácil testing
✅ Swagger automático
✅ Preparada para microservicios
