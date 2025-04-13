# syntax=docker/dockerfile:1.9
FROM ubuntu:noble AS build

SHELL ["sh", "-exc"]

# Ensure apt-get doesn't open a menu on you.
ENV DEBIAN_FRONTEND=noninteractive

### Start build prep.
### This should be a separate build container for better reuse.

RUN <<EOT
apt-get update -y
apt-get install -y \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    build-essential \
    ca-certificates \
    python3-setuptools \
    python3.12-dev
EOT

# Security-conscious organizations should package/review uv themselves.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# - Silence uv complaining about not being able to use hard links,
# - tell uv to byte-compile packages for faster application startups,
# - prevent uv from accidentally downloading isolated Python builds,
# - pick a Python (use `/usr/bin/python3.12` on uv 0.5.0 and later),
# - and finally declare `/app` as the target for `uv sync`.
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=/usr/bin/python3.12 \
    UV_PROJECT_ENVIRONMENT=/app

### End build prep -- this is where your app Dockerfile should start.

# Synchronize DEPENDENCIES without the application itself.
# This layer is cached until uv.lock or pyproject.toml change, which are
# only temporarily mounted into the build container since we don't need
# them in the production one.
# You can create `/app` using `uv venv` in a separate `RUN`
# step to have it cached, but with uv it's so fast, it's not worth
# it, so we let `uv sync` create it for us automagically.
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
        --locked \
        --no-dev \
        --no-install-project

# Now install the rest from `/src`: The APPLICATION w/o dependencies.
# `/src` will NOT be copied into the runtime container.
# LEAVE THIS OUT if your application is NOT a proper Python package.
# COPY . /src
# WORKDIR /src
# RUN --mount=type=cache,target=/root/.cache \
#     uv sync \
#         --locked \
#         --no-dev \
#         --no-editable

##########################################################################

FROM ubuntu:noble
SHELL ["sh", "-exc"]

# Optional: add the application virtualenv to search path.
ENV PATH=/app/bin:$PATH

# Don't run your app as root.
RUN <<EOT
groupadd -r app
useradd -r -d /app -g app -N app
EOT

ENTRYPOINT ["/app/docker-entrypoint.sh"]
# See <https://hynek.me/articles/docker-signals/>.
STOPSIGNAL SIGINT

# Note how the runtime dependencies differ from build-time ones.
# Notably, there is no uv either!
RUN <<EOT
apt-get update -y
apt-get install -y \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    python3.12 \
    libpython3.12 \
    libpcre3 \
    libxml2 \
    netcat-traditional

apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOT

COPY --chmod=777 docker-entrypoint.sh /app/docker-entrypoint.sh
# COPY uwsgi/uwsgi.ini /app/etc/uwsgi.ini

# Copy the pre-built `/app` directory to the runtime container
# and change the ownership to user app and group app in one step.
COPY --from=build --chown=app:app /app /app


# If your application is NOT a proper Python package that got
# pip-installed above, you need to copy your application into
# the container HERE:
COPY . /app
RUN <<EOT
chmod +x /app/docker-entrypoint.sh
touch /app/db.sqlite3
chmod +rw /app/db.sqlite3
chown -R app:app /app
EOT

# RUN <<EOT
# mkdir -p /opt/app/static/
# chmod o+r -R /opt/app/static/
# mkdir -p /var/www/static/
# chmod o+r -R /var/www/static/
# EOT

RUN <<EOT
mkdir -p /app/django_config/static
chmod o+rw -R /app/django_config/static
mkdir -p /app/static
chmod o+rw -R /app/static
EOT

USER app
WORKDIR /app

# CMD ["tail", "-f", "/dev/null"]

# Strictly optional, but I like it for introspection of what I've built
# and run a smoke test that the application can, in fact, be imported.
# RUN <<EOT
# python -V
# python -Im site
# python -Ic 'import movies'
# EOT

# CMD ["bash", "run_uwsgi.sh"]
