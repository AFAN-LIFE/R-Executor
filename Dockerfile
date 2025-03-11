## Emacs, make this -*- mode: sh; -*-
FROM debian:testing

LABEL org.opencontainers.image.licenses="GPL-2.0-or-later" \
      org.opencontainers.image.source="https://github.com/rocker-org/rocker" \
      org.opencontainers.image.vendor="Rocker Project" \
      org.opencontainers.image.authors="Dirk Eddelbuettel <edd@debian.org>"

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

# Set a default user
RUN useradd -s /bin/bash -m docker \
    && usermod -a -G staff docker

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ed less locales vim-tiny wget ca-certificates fonts-texgyre \
    python3 python3-venv python3-dev python3-pip r-base r-base-dev r-base-core r-recommended \
    && rm -rf /var/lib/apt/lists/*

# Configure locale
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen en_US.utf8 \
    && /usr/sbin/update-locale LANG=en_US.UTF-8

# Create a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Install R packages from r_packages.txt
COPY r_packages.txt /app/r_packages.txt
RUN Rscript -e 'install.packages(readLines("/app/r_packages.txt"), repos="https://cloud.r-project.org/")'

# Set Flask app Dir
WORKDIR /app

# Expose the port for Flask
EXPOSE 5000

# Run the Flask app
CMD ["python3", "app.py"]
