# coding: utf-8
# copyright 2015-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
from io import StringIO

from cubicweb.devtools import testlib
from cubicweb.cwconfig import CubicWebConfiguration
try:
    from cubicweb.devtools import PostgresApptestConfiguration, startpgcluster, stoppgcluster
except ImportError as exc:
    import pytest
    pytestmark = pytest.mark.skipif(True, reason=str(exc))
else:
    from cubes.skos import ccplugin


def setUpModule():
    startpgcluster(__file__)


def tearDownModule():
    stoppgcluster(__file__)


class ImportSkosDataCommandTC(testlib.CubicWebTC):
    configcls = PostgresApptestConfiguration

    def setup_database(self):
        super(ImportSkosDataCommandTC, self).setup_database()
        self.orig_config_for = CubicWebConfiguration.config_for
        config_for = lambda appid: self.config
        CubicWebConfiguration.config_for = staticmethod(config_for)

    def tearDown(self):
        CubicWebConfiguration.config_for = self.orig_config_for
        super(ImportSkosDataCommandTC, self).tearDown()

    def run_import_skos(self, fpath, *args, **kwargs):
        cmd = [self.appid, fpath] + list(args)
        sys.stdout = StringIO()
        try:
            ccplugin.ImportSkosData(None).main_run(cmd)
        finally:
            stdout_check = kwargs.pop('stdout_check', None)
            if stdout_check is not None:
                self.assertIn(stdout_check, sys.stdout.getvalue())
            sys.stdout = sys.__stdout__

    def _test_base(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.find('ConceptScheme').one()
            self.assertEqual(scheme.title, u"Thésaurus de test")
            concept = cnx.find('Concept', cwuri='http://mystery.com/ark:/kra/543').one()
            expected = {
                u'fr': u'économie',
                u'fr-fr': u'économie',
            }
            self.assertEqual(concept.labels, expected)

    def test_nooption(self):
        self.run_import_skos(self.datapath('skos.rdf'))
        self._test_base()

    def test_nohook(self):
        self.run_import_skos(self.datapath('skos.rdf'),
                             '--cw-store', 'nohook')
        self._test_base()

    def test_massive(self):
        self.run_import_skos(self.datapath('skos.rdf'),
                             '-s', 'massive')
        self._test_base()

    def test_lcsv(self):
        self.run_import_skos(self.datapath('lcsv_example_shortened.csv'),
                             '--format', 'lcsv')
        with self.admin_access.cnx() as cnx:
            rset = cnx.find('ConceptScheme', title=u'lcsv_example_shortened.csv')
            self.assertTrue(rset)
            scheme = rset.one()
            self.assertEqual(scheme.title, u'lcsv_example_shortened.csv')
            self.assertEqual(len(scheme.reverse_in_scheme), 5)

    def test_lcsv_rollback(self):
        self.run_import_skos(
            self.datapath('lcsv_example_missing_prolog.csv'),
            '--format', 'lcsv',
            stdout_check=u"Aborting due to: 'missing prolog column (#)'",
        )
        with self.admin_access.cnx() as cnx:
            rset = cnx.find('ConceptScheme',
                            title=u'lcsv_example_missing_prolog.csv')
        self.assertFalse(rset)


if __name__ == '__main__':
    from unittest import main
    main()
