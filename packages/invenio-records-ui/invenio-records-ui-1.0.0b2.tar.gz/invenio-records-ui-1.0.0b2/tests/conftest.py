# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016, 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import json
import os

import pytest
from flask import Flask
from flask_babelex import Babel
from flask_celeryext import FlaskCeleryExt
from invenio_db import InvenioDB, db
from invenio_files_rest import InvenioFilesREST
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords


class DefaultJSONSerializer(object):
    """Simple JSON serializer for testing."""

    def serialize(self, pid, record):
        """Serialize object to JSON.

        :param pid: Persistent Identifier.
        :param record: The :class:`invenio_records.api.Record` instance.
        """
        return json.dumps(record, sort_keys=True,
                          indent=2, separators=(',', ': '))


@pytest.fixture()
def app(request):
    """Flask application fixture."""
    app = Flask('testapp')
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', 'sqlite://'
        ),
        CELERY_ALWAYS_EAGER=True,
        CELERY_RESULT_BACKEND='cache',
        CELERY_CACHE_BACKEND='memory',
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
        RECORDS_UI_DEFAULT_PERMISSION_FACTORY=None,  # No permission checking
    )
    FlaskCeleryExt(app)
    Babel(app)
    InvenioDB(app)
    InvenioPIDStore(app)
    InvenioRecords(app)
    InvenioFilesREST(app)

    with app.app_context():
        db.create_all()

    def finalize():
        with app.app_context():
            db.drop_all()

    request.addfinalizer(finalize)
    return app


@pytest.fixture()
def json_v1():
    """JSON serializer fixture."""
    return DefaultJSONSerializer()
