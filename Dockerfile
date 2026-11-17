FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv

# Installer les dépendances avant de copier le code permet de réutiliser le cache.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd --system app \
    && useradd --system --gid app --create-home app

COPY --chown=app:app app/ ./app/

USER app

EXPOSE 8000

# Serveur de développement pour l'utilisation locale du projet.
# 0.0.0.0 permet l'accès à Flask depuis l'extérieur du conteneur.
CMD ["python", "-m", "flask", "--app", "app:app", "run", "--host=0.0.0.0", "--port=8000"]
