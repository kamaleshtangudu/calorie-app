################# Builder ###############
FROM ubuntu:20.04 AS base

# Setting image timezone as UTC
ARG TZ=UTC

# Install global dependencies
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ >/etc/timezone \
  && apt-get update && apt-get clean && apt-get install -y --no-install-recommends -qq \
  curl \
  libturbojpeg \
  gettext \
  netcat \
  postgresql-client \
  python3-pip \
  python3-distutils \
  python3.9-dev \
  # Register the version in alternatives and set python 3 as the default python
  && update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 \
  && update-alternatives --set python /usr/bin/python3.9 \
  # Change user from root to appuser
  && useradd --create-home appuser

ENV PATH=/home/appuser/.local/bin:$PATH

################# Python Dependencies ###############
FROM base AS dependencies

# Install build dependencies
RUN apt-get install -y --no-install-recommends -qq \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libpcre++-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

USER appuser

COPY reqs ./reqs/
COPY requirements.txt .

RUN python -m pip install --no-cache-dir --user --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir --user -r requirements.txt

################# Release ###############
FROM base AS release

RUN rm -rf /var/lib/apt/lists/*

#Copy over all python dependencies
COPY --chown=appuser:appuser --from=dependencies /home/appuser/.local/bin/ /home/appuser/.local/bin/
COPY --chown=appuser:appuser --from=dependencies /home/appuser/.local/lib/python3.9/site-packages/ /home/appuser/.local/lib/python3.9/site-packages

#Copy over all the executable script
COPY --chown=appuser:appuser . /home/appuser/
COPY --chown=appuser:appuser ./deploy/entrypoint.sh /
COPY --chown=appuser:appuser ./deploy/wait-for /home/appuser/.local/bin/wait-for

#Grant executable permission to the startup script
RUN chmod +x /entrypoint.sh /home/appuser/.local/bin/wait-for

USER appuser
WORKDIR /home/appuser

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create static files
RUN python manage.py collectstatic --noinput --settings=calorie_app.settings.pipeline

#Run Startup script
ENTRYPOINT ["/entrypoint.sh"]
