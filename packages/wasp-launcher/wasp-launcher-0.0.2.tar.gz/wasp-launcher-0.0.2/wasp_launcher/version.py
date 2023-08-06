# -*- coding: utf-8 -*-
# wasp_launcher/version.py
#
# Copyright (C) 2016 the wasp-launcher authors and contributors
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


import subprocess


def revision():
	#return subprocess.getoutput("svnversion")
	status, output = subprocess.getstatusoutput("git rev-parse HEAD")
	if status == 0:
		return output[:7]
	return "--"


__author__ = "Ildar Gafurov"
__numeric_version__ = '0.0.2'
__version__ = ("%s.dev%s" % (__numeric_version__, revision()))
__credits__ = ["Ildar Gafurov"]
__license__ = "GNU Lesser General Public License v3"
__copyright__ = "Copyright 2016-2017, The Wasp-launcher"
__email__ = "dev@binblob.com"
__status__ = "Development"
