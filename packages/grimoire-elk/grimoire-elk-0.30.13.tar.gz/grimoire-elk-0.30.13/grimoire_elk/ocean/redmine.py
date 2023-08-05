#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Redmine Ocean feeder
#
# Copyright (C) 2015 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#   Alvaro del Castillo San Felix <acs@bitergia.com>
#

from .elastic import ElasticOcean

class RedmineOcean(ElasticOcean):
    """Redmine Ocean feeder"""

    def _fix_item(self, item):
        item["ocean-unique-id"] = item["origin"]+"_"+str(item["data"]["id"])

    def get_elastic_mappings(self):
        # data.journals.notes
        mapping = '''
         {
            "dynamic":true,
                "properties": {
                    "data": {
                        "properties": {
                            "journals": {
                                "dynamic":false,
                                "properties": {}
                            }
                        }
                    }
                }
        }
        '''

        return {"items":mapping}
