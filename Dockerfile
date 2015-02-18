# This file is part of JSONAlchemy.
# Copyright (C) 2015 CERN.
#
# JSONAlchemy is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# JSONAlchemy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JSONAlchemy; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

# Use Python-2.7:
FROM python:2.7

# Install some prerequisites ahead of `setup.py` in order to profit
# from the docker build cache:
RUN pip install cerberus \
                coveralls \
                ipython \
                lxml \
                pep257 \
                pyparsing==2.0.1 \
                pytest \
                pytest-cache \
                pytest-cov \
                pytest-pep8 \
                six \
                sphinx_rtd_theme

# Add sources to `code` and work there:
WORKDIR /code
ADD . /code

# Install jsonalchemy:
RUN pip install -e .[docs]

# Run container as user `jsonalchemy` with UID `1000`, which should match
# current host user in most situations:
RUN adduser --uid 1000 --disabled-password --gecos '' jsonalchemy && \
    chown -R jsonalchemy:jsonalchemy /code

# Run test suite instead of starting the application:
USER jsonalchemy
CMD ["python", "setup.py", "test"]
