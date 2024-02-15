# Use Python 3.12 as the base image
FROM python:3.12

# Install curl and wget
RUN apt-get update && apt-get install -y curl wget

# Add PostgreSQL repository for buster
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Install PostgreSQL client, MongoDB, and Python dependencies
RUN apt-get update && \
    apt-get install -y postgresql-client-10 && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install curl and wget
RUN apt-get update && apt-get install -y curl wget gnupg

# Add MongoDB repository key
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -

# Add MongoDB repository
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.2 main" > /etc/apt/sources.list.d/mongodb-org-4.2.list

# Install MongoDB tools
RUN apt-get update && \
    apt-get install -y mongodb-org-tools && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /srv/requirements.txt
WORKDIR /srv
RUN python -m pip install --no-cache-dir -r requirements.txt && \
    python -m pip install statsmodels
