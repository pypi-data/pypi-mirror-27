# -*- coding: utf-8 -*-
# wasp_launcher/apps/web/debug.py
#
# Copyright (C) 2016-2017 the wasp-launcher authors and contributors
# <see AUTHORS file>
#
# This file is part of wasp-launcher.
#
# Wasp-launcher is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wasp-launcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with wasp-launcher.  If not, see <http://www.gnu.org/licenses/>.

# TODO: document the code
# TODO: write tests for the code

# noinspection PyUnresolvedReferences
from wasp_launcher.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
# noinspection PyUnresolvedReferences
from wasp_launcher.version import __status__

import os
import base64
import uuid

from wasp_general.verify import verify_type, verify_value

from wasp_general.network.web.service import WWebRoute
from wasp_general.template import WTemplateText
from wasp_general.network.web.template_response import WWebTemplateResponse

from wasp_launcher.core import WWebApp, WWebPresenter
from wasp_launcher.apps.web_debugger import WWebAppDebuggerDatastore
from wasp_launcher.apps.web.wasp import WErrorPresenter


class WDebugPresenter(WWebPresenter):

	def index(self):
		return self.__template_response__('mako::com.binblob.wasp-launcher.apps.wasp-debug::test.mako')

	def session(self, session_uuid):
		session_uuid = base64.decodebytes(session_uuid.encode('us-ascii'))
		self._context['uuid'] = str(session_uuid)

		query = {'uuid': uuid.UUID(bytes=session_uuid)}
		self._context['session'] = WWebAppDebuggerDatastore.__mongo_sessions__.find_one(query)
		self._context['request'] = WWebAppDebuggerDatastore.__mongo_requests__.find_one(query)
		self._context['response'] = WWebAppDebuggerDatastore.__mongo_responses__.find_one(query)
		self._context['target_route'] = WWebAppDebuggerDatastore.__mongo_target_routes__.find_one(query)
		self._context['wasp_exceptions'] = list(WWebAppDebuggerDatastore.__mongo_exceptions__.find(query))

		return self.__template_response__('mako::com.binblob.wasp-launcher.apps.wasp-debug::session.mako')

	@classmethod
	def __presenter_name__(cls):
		return 'com.binblob.wasp-launcher.apps.wasp-debug.debug-presenter'

	@classmethod
	def __public_routes__(cls):
		return [
			WWebRoute('/apps.wasp-debug.debug', cls.__presenter_name__()),
			WWebRoute(
				'/apps.wasp-debug.debug/session/{session_uuid: "([a-zA-Z0-9+=/]+)"}',
				cls.__presenter_name__(), action='session'
			),
			WWebRoute(
				'/static.wasp-debug.debug{path:"/?(.*)"}',
				'com.binblob.wasp-launcher.apps.wasp-basic.staticfiles-presenter',
				basedir=os.path.join(os.path.dirname(__file__), '..', 'static', 'debug'),
				listdir=False
			)
		]


class WDebugErrorPresenter(WErrorPresenter):

	@verify_type(code=int)
	@verify_value(code=lambda x: x > 0)
	def error_code(self, code):
		context = {
			'error_title': "Damn error page %i" % code,
			'error_header': "What has happened?",
			'error_footer': "WHY!?!?!",
			'error_messages': {
				('Error %i' % code): self.__message__(code)
			}
		}

		request = self.__request__()
		if hasattr(request, '__wlauncher_debugger_session__'):
			session = request.__wlauncher_debugger_session__
			session = base64.b64encode(session.uuid.bytes).decode('us-ascii')
			link = '/apps.wasp-debug.debug/session/%s' % session
			context['error_messages']['Debug'] = '<A href="%s">Debug information</A>' % link

		return WWebTemplateResponse(WTemplateText(self.__error_template__()), context=context)

	@classmethod
	def __presenter_name__(cls):
		return 'com.binblob.wasp-launcher.apps.wasp-debug.error-presenter'


class WWaspDebugApps(WWebApp):

	__registry_tag__ = 'com.binblob.wasp-launcher.apps.web.wasp-debug'

	@classmethod
	def public_presenters(cls):
		return [WDebugPresenter, WDebugErrorPresenter]

	@classmethod
	def template_path(cls):
		return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates', 'debug'))
