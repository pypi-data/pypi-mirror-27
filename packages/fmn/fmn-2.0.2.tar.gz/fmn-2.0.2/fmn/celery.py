# This file is part of the FMN project.
# Copyright (C) 2017 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""The Celery application."""
from __future__ import absolute_import

from celery import Celery
from kombu.common import Broadcast, Queue

from . import config


RELOAD_CACHE_EXCHANGE_NAME = 'fmn.tasks.reload_cache'


#: The celery application object
app = Celery('FMN')
app.conf.task_queues = (
    Broadcast(RELOAD_CACHE_EXCHANGE_NAME),
    Queue('fmn.tasks.unprocessed_messages'),
)
app.conf.update(**config.app_conf['celery'])
