# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

from .utils import RelatedStoresDataTool, RelatedTPsDataTool


class ProjectDataTool(RelatedTPsDataTool):
    """Retrieves aggregate stats for a Project"""

    cache_key_name = "project"

    def filter_data(self, qs):
        return qs.filter(tp__project=self.context)


class ProjectResourceDataTool(RelatedStoresDataTool):
    group_by = ("store__translation_project__language__code", )
    cache_key_name = "project_resource"

    @property
    def project_path(self):
        return (
            "/%s/%s%s"
            % (self.project_code,
               self.dir_path,
               self.filename))

    def filter_data(self, qs):
        regex = r"^/[^/]*%s" % self.project_path
        return (
            qs.filter(store__translation_project__project__code=self.project_code)
              .filter(store__pootle_path__contains=self.project_path)
              .filter(store__pootle_path__regex=regex))

    @property
    def context_name(self):
        return "/projects%s" % self.project_path


class ProjectSetDataTool(RelatedTPsDataTool):
    group_by = ("tp__project__code", )
    cache_key_name = "projects"

    def get_root_child_path(self, child):
        return child[self.group_by[0]]

    @property
    def context_name(self):
        return "ALL"
