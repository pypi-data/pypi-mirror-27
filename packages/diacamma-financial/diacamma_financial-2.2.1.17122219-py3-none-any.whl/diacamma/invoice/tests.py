# -*- coding: utf-8 -*-
'''
diacamma.invoice tests package

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2015 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import unicode_literals
from shutil import rmtree
from datetime import date
from base64 import b64decode
from _io import StringIO

from django.utils import formats, six

from lucterios.framework.test import LucteriosTest
from lucterios.framework.xfergraphic import XferContainerAcknowledge
from lucterios.framework.filetools import get_user_dir
from lucterios.CORE.models import Parameter
from lucterios.CORE.parameters import Params

from diacamma.accounting.test_tools import initial_thirds, default_compta
from diacamma.accounting.views_entries import EntryAccountList
from diacamma.invoice.test_tools import default_articles, InvoiceTest, \
    default_categories, default_customize
from diacamma.invoice.views_conf import InvoiceConf, VatAddModify, VatDel, \
    CategoryAddModify, CategoryDel, ArticleImport, StorageAreaDel,\
    StorageAreaAddModify
from diacamma.invoice.views import ArticleList, ArticleAddModify, ArticleDel, \
    BillList, BillAddModify, BillShow, DetailAddModify, DetailDel, BillTransition, BillDel, BillFromQuotation, \
    BillStatistic, BillStatisticPrint, BillPrint, BillMultiPay, ArticleShow
from diacamma.payoff.views import PayoffAddModify, PayoffDel, SupportingThird, \
    SupportingThirdValid, PayableEmail
from diacamma.payoff.test_tools import default_bankaccount
from lucterios.mailing.tests import configSMTP, TestReceiver, decode_b64


class ConfigTest(LucteriosTest):

    def setUp(self):
        self.xfer_class = XferContainerAcknowledge
        LucteriosTest.setUp(self)
        default_compta()
        rmtree(get_user_dir(), True)

    def test_vat(self):
        self.factory.xfer = InvoiceConf()
        self.call('/diacamma.invoice/invoiceConf', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'invoiceConf')
        self.assert_count_equal('COMPONENTS/TAB', 5)
        self.assert_count_equal('COMPONENTS/*', 2 + 5 + 5 + 2 + 2)

        self.assert_count_equal('COMPONENTS/GRID[@name="vat"]/HEADER', 4)
        self.assert_xml_equal('COMPONENTS/GRID[@name="vat"]/HEADER[@name="name"]', "nom")
        self.assert_xml_equal('COMPONENTS/GRID[@name="vat"]/HEADER[@name="rate"]', "taux")
        self.assert_xml_equal('COMPONENTS/GRID[@name="vat"]/HEADER[@name="account"]', "compte de TVA")
        self.assert_xml_equal('COMPONENTS/GRID[@name="vat"]/HEADER[@name="isactif"]', "actif ?")
        self.assert_count_equal('COMPONENTS/GRID[@name="vat"]/RECORD', 0)

        self.factory.xfer = VatAddModify()
        self.call('/diacamma.invoice/vatAddModify', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'vatAddModify')
        self.assert_count_equal('COMPONENTS/*', 5)

        self.factory.xfer = VatAddModify()
        self.call('/diacamma.invoice/vatAddModify',
                  {'name': 'my vat', 'rate': '11.57', 'account': '4455', 'isactif': 1, 'SAVE': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'vatAddModify')

        self.factory.xfer = InvoiceConf()
        self.call('/diacamma.invoice/invoiceConf', {}, False)
        self.assert_count_equal('COMPONENTS/GRID[@name="vat"]/RECORD', 1)
        self.assert_xml_equal('COMPONENTS/GRID[@name="vat"]/RECORD[1]/VALUE[@name="name"]', 'my vat')
        self.assert_xml_equal('COMPONENTS/GRID[@name="vat"]/RECORD[1]/VALUE[@name="rate"]', '11.57')
        self.assert_xml_equal('COMPONENTS/GRID[@name="vat"]/RECORD[1]/VALUE[@name="account"]', '4455')
        self.assert_xml_equal('COMPONENTS/GRID[@name="vat"]/RECORD[1]/VALUE[@name="isactif"]', '1')

        self.factory.xfer = VatDel()
        self.call('/diacamma.invoice/vatDel', {'vat': 1, 'CONFIRME': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'vatDel')

        self.factory.xfer = InvoiceConf()
        self.call('/diacamma.invoice/invoiceConf', {}, False)
        self.assert_count_equal('COMPONENTS/GRID[@name="vat"]/RECORD', 0)

    def test_category(self):
        self.factory.xfer = InvoiceConf()
        self.call('/diacamma.invoice/invoiceConf', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'invoiceConf')
        self.assert_count_equal('COMPONENTS/TAB', 5)
        self.assert_count_equal('COMPONENTS/*', 2 + 5 + 5 + 2 + 2)

        self.assert_count_equal('COMPONENTS/GRID[@name="category"]/HEADER', 2)
        self.assert_xml_equal('COMPONENTS/GRID[@name="category"]/HEADER[@name="name"]', "nom")
        self.assert_xml_equal('COMPONENTS/GRID[@name="category"]/HEADER[@name="designation"]', "désignation")
        self.assert_count_equal('COMPONENTS/GRID[@name="category"]/RECORD', 0)

        self.factory.xfer = CategoryAddModify()
        self.call('/diacamma.invoice/categoryAddModify', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'categoryAddModify')
        self.assert_count_equal('COMPONENTS/*', 3)

        self.factory.xfer = CategoryAddModify()
        self.call('/diacamma.invoice/categoryAddModify',
                  {'name': 'my category', 'designation': "bla bla bla", 'SAVE': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'categoryAddModify')

        self.factory.xfer = InvoiceConf()
        self.call('/diacamma.invoice/invoiceConf', {}, False)
        self.assert_count_equal('COMPONENTS/GRID[@name="category"]/RECORD', 1)
        self.assert_xml_equal('COMPONENTS/GRID[@name="category"]/RECORD[1]/VALUE[@name="name"]', 'my category')
        self.assert_xml_equal('COMPONENTS/GRID[@name="category"]/RECORD[1]/VALUE[@name="designation"]', 'bla bla bla')

        self.factory.xfer = CategoryDel()
        self.call('/diacamma.invoice/categoryDel', {'category': 1, 'CONFIRME': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'categoryDel')

        self.factory.xfer = InvoiceConf()
        self.call('/diacamma.invoice/invoiceConf', {}, False)
        self.assert_count_equal('COMPONENTS/GRID[@name="category"]/RECORD', 0)

    def test_customize(self):
        default_customize()
        self.factory.xfer = InvoiceConf()
        self.call('/diacamma.invoice/invoiceConf', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'invoiceConf')
        self.assert_count_equal('COMPONENTS/TAB', 5)
        self.assert_count_equal('COMPONENTS/*', 2 + 5 + 5 + 2 + 2)

        self.assert_count_equal('COMPONENTS/GRID[@name="custom_field"]/HEADER', 2)
        self.assert_xml_equal('COMPONENTS/GRID[@name="custom_field"]/HEADER[@name="name"]', "nom")
        self.assert_xml_equal('COMPONENTS/GRID[@name="custom_field"]/HEADER[@name="kind_txt"]', "type")
        self.assert_count_equal('COMPONENTS/GRID[@name="custom_field"]/RECORD', 2)
        self.assert_xml_equal('COMPONENTS/GRID[@name="custom_field"]/RECORD[1]/VALUE[@name="name"]', 'couleur')
        self.assert_xml_equal('COMPONENTS/GRID[@name="custom_field"]/RECORD[1]/VALUE[@name="kind_txt"]', 'Sélection (---,noir,blanc,rouge,bleu,jaune)')
        self.assert_xml_equal('COMPONENTS/GRID[@name="custom_field"]/RECORD[2]/VALUE[@name="name"]', 'taille')
        self.assert_xml_equal('COMPONENTS/GRID[@name="custom_field"]/RECORD[2]/VALUE[@name="kind_txt"]', 'Entier [0;100]')

    def test_storagearea(self):
        self.factory.xfer = InvoiceConf()
        self.call('/diacamma.invoice/invoiceConf', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'invoiceConf')
        self.assert_count_equal('COMPONENTS/TAB', 5)
        self.assert_count_equal('COMPONENTS/*', 2 + 5 + 5 + 2 + 2)

        self.assert_count_equal('COMPONENTS/GRID[@name="storagearea"]/HEADER', 2)
        self.assert_xml_equal('COMPONENTS/GRID[@name="storagearea"]/HEADER[@name="name"]', "nom")
        self.assert_xml_equal('COMPONENTS/GRID[@name="storagearea"]/HEADER[@name="designation"]', "désignation")
        self.assert_count_equal('COMPONENTS/GRID[@name="v"]/RECORD', 0)

        self.factory.xfer = StorageAreaAddModify()
        self.call('/diacamma.invoice/storageAreaAddModify', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'storageAreaAddModify')
        self.assert_count_equal('COMPONENTS/*', 3)

        self.factory.xfer = StorageAreaAddModify()
        self.call('/diacamma.invoice/storageAreaAddModify',
                  {'name': 'my category', 'designation': "bla bla bla", 'SAVE': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'storageAreaAddModify')

        self.factory.xfer = InvoiceConf()
        self.call('/diacamma.invoice/invoiceConf', {}, False)
        self.assert_count_equal('COMPONENTS/GRID[@name="storagearea"]/RECORD', 1)
        self.assert_xml_equal('COMPONENTS/GRID[@name="storagearea"]/RECORD[1]/VALUE[@name="name"]', 'my category')
        self.assert_xml_equal('COMPONENTS/GRID[@name="storagearea"]/RECORD[1]/VALUE[@name="designation"]', 'bla bla bla')

        self.factory.xfer = StorageAreaDel()
        self.call('/diacamma.invoice/storageAreaDel', {'storagearea': 1, 'CONFIRME': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'storageAreaDel')

        self.factory.xfer = InvoiceConf()
        self.call('/diacamma.invoice/invoiceConf', {}, False)
        self.assert_count_equal('COMPONENTS/GRID[@name="storagearea"]/RECORD', 0)

    def test_article(self):
        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/*', 6)
        self.assert_count_equal('COMPONENTS/SELECT[@name="stockable"]/CASE', 4)
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/HEADER', 7)
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/HEADER[@name="reference"]', "référence")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/HEADER[@name="designation"]', "désignation")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/HEADER[@name="price_txt"]', "prix")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/HEADER[@name="unit"]', "unité")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/HEADER[@name="isdisabled"]', "désactivé ?")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/HEADER[@name="sell_account"]', "compte de vente")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/HEADER[@name="stockable"]', "stockable")
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 0)

        self.factory.xfer = ArticleAddModify()
        self.call('/diacamma.invoice/articleAddModify', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleAddModify')
        self.assert_count_equal('COMPONENTS/*', 10)

        self.factory.xfer = ArticleAddModify()
        self.call('/diacamma.invoice/articleAddModify',
                  {'reference': 'ABC001', 'designation': 'My beautiful article', 'price': '43.72', 'sell_account': '705', 'stockable': '1', 'SAVE': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'articleAddModify')

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 1)
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="reference"]', "ABC001")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="designation"]', "My beautiful article")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="price_txt"]', "43.72€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="unit"]', None)
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="sell_account"]', "705")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="stockable"]', "stockable")

        self.factory.xfer = ArticleShow()
        self.call('/diacamma.invoice/articleShow', {'article': '1'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleShow')
        self.assert_count_equal('COMPONENTS/*', 13)

        self.factory.xfer = ArticleDel()
        self.call('/diacamma.invoice/articleDel',
                  {'article': '1', 'CONFIRME': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'articleDel')

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 0)

    def test_article_with_cat(self):
        default_categories()
        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/*', 7)
        self.assert_count_equal('COMPONENTS/CHECKLIST[@name="cat_filter"]/CASE', 3)
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/HEADER', 8)
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/HEADER[@name="categories"]', "catégories")
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 0)

        self.factory.xfer = ArticleAddModify()
        self.call('/diacamma.invoice/articleAddModify', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleAddModify')
        self.assert_count_equal('COMPONENTS/*', 12)

        self.factory.xfer = ArticleAddModify()
        self.call('/diacamma.invoice/articleAddModify',
                  {'reference': 'ABC001', 'designation': 'My beautiful article', 'price': '43.72', 'sell_account': '705', 'stockable': '1', 'categories': '2;3', 'SAVE': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'articleAddModify')

        self.factory.xfer = ArticleShow()
        self.call('/diacamma.invoice/articleShow', {'article': '1'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleShow')
        self.assert_count_equal('COMPONENTS/*', 14)

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 1)
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="categories"]', "cat 2{[br/]}cat 3")

    def test_article_filter(self):
        default_categories()
        default_articles(with_storage=True)
        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/*', 7)
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 4)

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {'show_filter': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/*', 7)
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 5)

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {'show_filter': 1, 'stockable': 0}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/*', 7)
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 2)

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {'show_filter': 1, 'stockable': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/*', 7)
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 2)

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {'show_filter': 1, 'stockable': 2}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/*', 7)
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 1)

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {'show_filter': 1, 'cat_filter': '2'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/*', 7)
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 3)

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {'show_filter': 1, 'cat_filter': '2;3'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/*', 7)
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 2)

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {'show_filter': 1, 'cat_filter': '1;2;3'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/*', 7)
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 1)

    def test_article_import1(self):
        initial_thirds()
        default_categories()
        csv_content = """'num','comment','prix','unité','compte','stock?','categorie','fournisseur','ref'
'A123','article N°1','','Kg','701','stockable','cat 2','Dalton Avrel','POIYT'
'B234','article N°2','23,56','L','701','stockable','cat 3','',''
'C345','article N°3','45.74','','702','non stockable','cat 1','Dalton Avrel','MLKJH'
'D456','article N°4','56,89','m','701','stockable & non vendable','','Maximum','987654'
'A123','article N°1','13.57','Kg','701','stockable','cat 3','',''
'A123','article N°1','16,95','Kg','701','stockable','','Maximum','654321'
"""

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {'show_filter': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 0)

        self.factory.xfer = ArticleImport()
        self.call('/diacamma.invoice/articleImport', {'step': 1, 'modelname': 'invoice.Article', 'quotechar': "'",
                                                      'delimiter': ',', 'encoding': 'utf-8', 'dateformat': '%d/%m/%Y', 'csvcontent': StringIO(csv_content)}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleImport')
        self.assert_count_equal('COMPONENTS/*', 6 + 11)
        self.assert_count_equal('COMPONENTS/SELECT[@name="fld_reference"]/CASE', 9)
        self.assert_count_equal('COMPONENTS/SELECT[@name="fld_categories"]/CASE', 10)
        self.assert_count_equal('COMPONENTS/GRID[@name="CSV"]/HEADER', 9)
        self.assert_count_equal('COMPONENTS/GRID[@name="CSV"]/RECORD', 6)
        self.assert_count_equal('COMPONENTS/GRID[@name="CSV"]/ACTIONS', 0)
        self.assert_count_equal('ACTIONS/ACTION', 3)
        self.assert_action_equal('ACTIONS/ACTION[1]', (six.text_type(
            'Retour'), 'images/left.png', 'diacamma.invoice', 'articleImport', 0, 2, 1, {'step': '0'}))
        self.assert_action_equal('ACTIONS/ACTION[2]', (six.text_type(
            'Ok'), 'images/ok.png', 'diacamma.invoice', 'articleImport', 0, 2, 1, {'step': '2'}))
        self.assert_count_equal('CONTEXT/PARAM', 8)

        self.factory.xfer = ArticleImport()
        self.call('/diacamma.invoice/articleImport', {'step': 2, 'modelname': 'invoice.Article', 'quotechar': "'", 'delimiter': ',',
                                                      'encoding': 'utf-8', 'dateformat': '%d/%m/%Y', 'csvcontent0': csv_content,
                                                      "fld_reference": "num", "fld_designation": "comment", "fld_price": "prix",
                                                      "fld_unit": "unité", "fld_isdisabled": "", "fld_sell_account": "compte",
                                                      "fld_vat": "", "fld_stockable": "stock?", 'fld_categories': 'categorie',
                                                      'fld_provider.third.contact': 'fournisseur', 'fld_provider.reference': 'ref', }, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleImport')
        self.assert_count_equal('COMPONENTS/*', 4)
        self.assert_count_equal('COMPONENTS/GRID[@name="CSV"]/HEADER', 9)
        self.assert_count_equal('COMPONENTS/GRID[@name="CSV"]/RECORD', 6)
        self.assert_count_equal('COMPONENTS/GRID[@name="CSV"]/ACTIONS', 0)
        self.assert_count_equal('ACTIONS/ACTION', 3)
        self.assert_action_equal('ACTIONS/ACTION[2]', (six.text_type(
            'Ok'), 'images/ok.png', 'diacamma.invoice', 'articleImport', 0, 2, 1, {'step': '3'}))

        self.factory.xfer = ArticleImport()
        self.call('/diacamma.invoice/articleImport', {'step': 3, 'modelname': 'invoice.Article', 'quotechar': "'", 'delimiter': ',',
                                                      'encoding': 'utf-8', 'dateformat': '%d/%m/%Y', 'csvcontent0': csv_content,
                                                      "fld_reference": "num", "fld_designation": "comment", "fld_price": "prix",
                                                      "fld_unit": "unité", "fld_isdisabled": "", "fld_sell_account": "compte",
                                                      "fld_vat": "", "fld_stockable": "stock?", 'fld_categories': 'categorie',
                                                      'fld_provider.third.contact': 'fournisseur', 'fld_provider.reference': 'ref', }, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleImport')
        self.assert_count_equal('COMPONENTS/*', 2)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="result"]', "{[center]}{[i]}4 éléments ont été importés{[/i]}{[/center]}")
        self.assert_count_equal('ACTIONS/ACTION', 1)

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {'show_filter': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 4)
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="reference"]', "A123")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="designation"]', "article N°1")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="price_txt"]', "16.95€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="unit"]', 'Kg')
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="sell_account"]', "701")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="stockable"]', "stockable")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="categories"]', "cat 2{[br/]}cat 3")

        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="reference"]', "B234")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="designation"]', "article N°2")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="price_txt"]', "23.56€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="unit"]', 'L')
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="sell_account"]', "701")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="stockable"]', "stockable")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="categories"]', "cat 3")

        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="reference"]', "C345")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="designation"]', "article N°3")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="price_txt"]', "45.74€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="unit"]', None)
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="sell_account"]', "702")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="stockable"]', "non stockable")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="categories"]', "cat 1")

        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="reference"]', "D456")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="designation"]', "article N°4")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="price_txt"]', "56.89€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="unit"]', 'm')
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="sell_account"]', "701")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="stockable"]', "stockable & non vendable")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="categories"]', None)

        self.factory.xfer = ArticleShow()
        self.call('/diacamma.invoice/articleShow', {'article': '1'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleShow')
        self.assert_count_equal('COMPONENTS/*', 16)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="reference"]', "A123")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="categories"]', "cat 2{[br/]}cat 3")
        self.assert_count_equal('COMPONENTS/GRID[@name="provider"]/RECORD', 2)
        self.assert_xml_equal('COMPONENTS/GRID[@name="provider"]/RECORD[1]/VALUE[@name="third"]', "Dalton Avrel")
        self.assert_xml_equal('COMPONENTS/GRID[@name="provider"]/RECORD[1]/VALUE[@name="reference"]', "POIYT")
        self.assert_xml_equal('COMPONENTS/GRID[@name="provider"]/RECORD[2]/VALUE[@name="third"]', "Maximum")
        self.assert_xml_equal('COMPONENTS/GRID[@name="provider"]/RECORD[2]/VALUE[@name="reference"]', "654321")

        self.factory.xfer = ArticleImport()
        self.call('/diacamma.invoice/articleImport', {'step': 3, 'modelname': 'invoice.Article', 'quotechar': "'", 'delimiter': ',',
                                                      'encoding': 'utf-8', 'dateformat': '%d/%m/%Y', 'csvcontent0': csv_content,
                                                      "fld_reference": "num", "fld_designation": "comment", "fld_price": "prix",
                                                      "fld_unit": "unité", "fld_isdisabled": "", "fld_sell_account": "compte",
                                                      "fld_vat": "", "fld_stockable": "stock?", 'fld_categories': 'categorie',
                                                      'fld_provider.third.contact': 'fournisseur', 'fld_provider.reference': 'ref', }, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleImport')
        self.assert_count_equal('COMPONENTS/*', 2)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="result"]', "{[center]}{[i]}4 éléments ont été importés{[/i]}{[/center]}")
        self.assert_count_equal('ACTIONS/ACTION', 1)

        self.factory.xfer = ArticleShow()
        self.call('/diacamma.invoice/articleShow', {'article': '1'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleShow')
        self.assert_count_equal('COMPONENTS/*', 16)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="reference"]', "A123")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="categories"]', "cat 2{[br/]}cat 3")
        self.assert_count_equal('COMPONENTS/GRID[@name="provider"]/RECORD', 2)
        self.assert_xml_equal('COMPONENTS/GRID[@name="provider"]/RECORD[1]/VALUE[@name="third"]', "Dalton Avrel")
        self.assert_xml_equal('COMPONENTS/GRID[@name="provider"]/RECORD[1]/VALUE[@name="reference"]', "POIYT")
        self.assert_xml_equal('COMPONENTS/GRID[@name="provider"]/RECORD[2]/VALUE[@name="third"]', "Maximum")
        self.assert_xml_equal('COMPONENTS/GRID[@name="provider"]/RECORD[2]/VALUE[@name="reference"]', "654321")

    def test_article_import2(self):
        initial_thirds()
        default_categories()
        csv_content = """'num','comment','prix','unité','compte','stock?','categorie','fournisseur','ref'
'A123','article N°1','ssdqs','Kg','701','stockable','cat 2','Avrel','POIYT'
'B234','article N°2','23.56','L','701','stockable','cat 3','',''
'C345','article N°3','45.74','','702','non stockable','cat 1','Avrel','MLKJH'
'D456','article N°4','56.89','m','701','stockable & non vendable','','Maximum','987654'
'A123','article N°1','13.57','Kg','701','stockable','cat 3','',''
'A123','article N°1','16.95','Kg','701','stockable','','Maximum','654321'
"""

        self.factory.xfer = ArticleImport()
        self.call('/diacamma.invoice/articleImport', {'step': 3, 'modelname': 'invoice.Article', 'quotechar': "'", 'delimiter': ',',
                                                      'encoding': 'utf-8', 'dateformat': '%d/%m/%Y', 'csvcontent0': csv_content,
                                                      "fld_reference": "num", "fld_designation": "comment", "fld_price": "prix",
                                                      "fld_unit": "unité", "fld_isdisabled": "", "fld_sell_account": "compte",
                                                      "fld_vat": "", "fld_stockable": "stock?", 'fld_categories': '',
                                                      'fld_provider.third.contact': '', 'fld_provider.reference': '', }, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleImport')
        self.assert_count_equal('COMPONENTS/*', 2)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="result"]', "{[center]}{[i]}4 éléments ont été importés{[/i]}{[/center]}")
        self.assert_count_equal('ACTIONS/ACTION', 1)

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {'show_filter': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 4)
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="reference"]', "A123")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="designation"]', "article N°1")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="price_txt"]', "16.95€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="unit"]', 'Kg')
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="sell_account"]', "701")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="stockable"]', "stockable")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="categories"]', None)

        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="reference"]', "B234")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="designation"]', "article N°2")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="price_txt"]', "23.56€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="unit"]', 'L')
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="sell_account"]', "701")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="stockable"]', "stockable")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="categories"]', None)

        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="reference"]', "C345")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="designation"]', "article N°3")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="price_txt"]', "45.74€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="unit"]', None)
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="sell_account"]', "702")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="stockable"]', "non stockable")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="categories"]', None)

        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="reference"]', "D456")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="designation"]', "article N°4")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="price_txt"]', "56.89€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="unit"]', 'm')
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="sell_account"]', "701")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="stockable"]', "stockable & non vendable")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="categories"]', None)

        self.factory.xfer = ArticleShow()
        self.call('/diacamma.invoice/articleShow', {'article': '1'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleShow')
        self.assert_count_equal('COMPONENTS/*', 16)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="reference"]', "A123")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="categories"]', None)
        self.assert_count_equal('COMPONENTS/GRID[@name="provider"]/RECORD', 0)

    def test_article_import3(self):
        default_customize()
        csv_content = """'num','comment','prix','unité','compte','stock?','categorie','fournisseur','ref','color','size'
'A123','article N°1','12.45','Kg','701','stockable','cat 2','Avrel','POIYT','---','10'
'B234','article N°2','23.56','L','701','stockable','cat 3','','','noir','25'
'C345','article N°3','45.74','','702','non stockable','cat 1','Avrel','MLKJH','rouge','75'
'D456','article N°4','56.89','m','701','stockable & non vendable','','Maximum','987654','blanc','1'
'A123','article N°1','13.57','Kg','701','stockable','cat 3','','','bleu','10'
'A123','article N°1','16.95','Kg','701','stockable','','Maximum','654321','bleu','15'
"""

        self.factory.xfer = ArticleImport()
        self.call('/diacamma.invoice/articleImport', {'step': 3, 'modelname': 'invoice.Article', 'quotechar': "'", 'delimiter': ',',
                                                      'encoding': 'utf-8', 'dateformat': '%d/%m/%Y', 'csvcontent0': csv_content,
                                                      "fld_reference": "num", "fld_designation": "comment", "fld_price": "prix",
                                                      "fld_unit": "unité", "fld_isdisabled": "", "fld_sell_account": "compte",
                                                      "fld_vat": "", "fld_stockable": "stock?",
                                                      "fld_custom_1": "color", "fld_custom_2": "size", }, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleImport')
        self.assert_count_equal('COMPONENTS/*', 2)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="result"]', "{[center]}{[i]}4 éléments ont été importés{[/i]}{[/center]}")
        self.assert_count_equal('ACTIONS/ACTION', 1)

        self.factory.xfer = ArticleList()
        self.call('/diacamma.invoice/articleList', {'show_filter': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleList')
        self.assert_count_equal('COMPONENTS/GRID[@name="article"]/RECORD', 4)
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="reference"]', "A123")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="designation"]', "article N°1")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="price_txt"]', "16.95€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="unit"]', 'Kg')
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="sell_account"]', "701")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[1]/VALUE[@name="stockable"]', "stockable")

        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="reference"]', "B234")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="designation"]', "article N°2")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="price_txt"]', "23.56€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="unit"]', 'L')
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="sell_account"]', "701")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[2]/VALUE[@name="stockable"]', "stockable")

        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="reference"]', "C345")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="designation"]', "article N°3")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="price_txt"]', "45.74€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="unit"]', None)
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="sell_account"]', "702")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[3]/VALUE[@name="stockable"]', "non stockable")

        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="reference"]', "D456")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="designation"]', "article N°4")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="price_txt"]', "56.89€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="unit"]', 'm')
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="isdisabled"]', "0")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="sell_account"]', "701")
        self.assert_xml_equal('COMPONENTS/GRID[@name="article"]/RECORD[4]/VALUE[@name="stockable"]', "stockable & non vendable")

        self.factory.xfer = ArticleShow()
        self.call('/diacamma.invoice/articleShow', {'article': '1'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'articleShow')
        self.assert_count_equal('COMPONENTS/*', 15)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="reference"]', "A123")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="custom_1"]', "bleu")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="custom_2"]', "15")


class BillTest(InvoiceTest):

    def setUp(self):
        self.xfer_class = XferContainerAcknowledge
        initial_thirds()
        LucteriosTest.setUp(self)
        default_compta()
        default_bankaccount()
        rmtree(get_user_dir(), True)

    def test_add_bill(self):
        default_articles()
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 0)
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/HEADER', 7)
        self.assert_xml_equal('COMPONENTS/GRID[@name="bill"]/HEADER[@name="total"]', "total")

        self.factory.xfer = BillAddModify()
        self.call('/diacamma.invoice/billAddModify', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billAddModify')
        self.assert_count_equal('COMPONENTS/*', 5)
        self.assert_count_equal('COMPONENTS/SELECT[@name="bill_type"]/CASE', 4)

        self.factory.xfer = BillAddModify()
        self.call('/diacamma.invoice/billAddModify', {'bill_type': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billAddModify')
        self.assert_count_equal('COMPONENTS/*', 6)
        self.assert_count_equal('COMPONENTS/SELECT[@name="bill_type"]/CASE', 4)
        self.assert_count_equal('COMPONENTS/SELECT[@name="cost_accounting"]/CASE', 2)

        self.factory.xfer = BillAddModify()
        self.call('/diacamma.invoice/billAddModify',
                  {'bill_type': 1, 'date': '2014-04-01', 'SAVE': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billAddModify')
        self.assert_attrib_equal(
            "ACTION", "id", "diacamma.invoice/billShow")
        self.assert_count_equal("ACTION/PARAM", 1)
        self.assert_xml_equal("ACTION/PARAM[@name='bill']", "1")
        self.assert_count_equal("CONTEXT/*", 2)

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_count_equal('ACTIONS/ACTION', 2)
        self.assert_count_equal('COMPONENTS/*', 11)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="title"]', "{[br/]}{[center]}{[u]}{[b]}facture{[/b]}{[/u]}{[/center]}")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="num_txt"]', "---")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="status"]', "en création")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="date"]', "1 avril 2014")
        self.assert_xml_equal(
            'COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}aucun tiers sélectionné{[br/]}pas de détail{[br/]}la date n'est pas incluse dans l'exercice{[/font]}")

        self.factory.xfer = BillAddModify()
        self.call('/diacamma.invoice/billAddModify',
                  {'bill': 1, 'date': '2015-04-01', 'SAVE': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billAddModify')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}aucun tiers sélectionné{[br/]}pas de détail{[/font]}")

        self.factory.xfer = SupportingThird()
        self.call('/diacamma.payoff/supportingThird',
                  {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.payoff', 'supportingThird')
        self.assert_count_equal('COMPONENTS/GRID[@name="third"]/RECORD', 7)

        self.factory.xfer = SupportingThirdValid()
        self.call('/diacamma.payoff/supportingThirdValid',
                  {'supporting': 1, 'third': 6}, False)
        self.assert_observer('core.acknowledge', 'diacamma.payoff', 'supportingThirdValid')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}pas de détail{[/font]}")

        self.factory.xfer = DetailAddModify()
        self.call('/diacamma.invoice/detailAddModify', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'detailAddModify')
        self.assert_count_equal('COMPONENTS/*', 7)

        self.factory.xfer = DetailAddModify()
        self.call('/diacamma.invoice/detailAddModify',
                  {'SAVE': 'YES', 'bill': 1, 'article': 1, 'designation': 'My article', 'price': '43.72', 'quantity': 2}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'detailAddModify')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_count_equal('COMPONENTS/*', 12)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="date"]', "1 avril 2015")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="third"]', "Dalton Jack")
        self.assert_count_equal('COMPONENTS/GRID[@name="detail"]/HEADER', 8)
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/HEADER[@name="price_txt"]', 'prix')
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/HEADER[@name="total"]', 'total')
        self.assert_count_equal('COMPONENTS/GRID[@name="detail"]/RECORD', 1)
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/RECORD[1]/VALUE[@name="article"]', 'ABC1')
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/RECORD[1]/VALUE[@name="designation"]', 'My article')
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/RECORD[1]/VALUE[@name="price_txt"]', '43.72€')
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/RECORD[1]/VALUE[@name="unit"]', None)
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/RECORD[1]/VALUE[@name="quantity"]', '2.00')
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/RECORD[1]/VALUE[@name="reduce_txt"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/RECORD[1]/VALUE[@name="total"]', '87.44€')

        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "87.44€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}{[/font]}")
        self.assert_count_equal('ACTIONS/ACTION', 3)

        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)

        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'filter': 'Dalton Jack'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)

    def test_add_bill_with_filter(self):
        default_categories()
        default_articles(True)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 0)

        self.factory.xfer = BillAddModify()
        self.call('/diacamma.invoice/billAddModify',
                  {'bill_type': 1, 'date': '2014-04-01', 'SAVE': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billAddModify')

        self.factory.xfer = DetailAddModify()
        self.call('/diacamma.invoice/detailAddModify', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'detailAddModify')
        self.assert_count_equal('COMPONENTS/*', 12)
        self.assert_count_equal('COMPONENTS/SELECT[@name="article"]/CASE', 5)

        self.factory.xfer = DetailAddModify()
        self.call('/diacamma.invoice/detailAddModify', {'bill': 1, 'third': 2}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'detailAddModify')
        self.assert_count_equal('COMPONENTS/*', 12)
        self.assert_count_equal('COMPONENTS/SELECT[@name="article"]/CASE', 2)

        self.factory.xfer = DetailAddModify()
        self.call('/diacamma.invoice/detailAddModify', {'bill': 1, 'reference': '34'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'detailAddModify')
        self.assert_count_equal('COMPONENTS/*', 12)
        self.assert_count_equal('COMPONENTS/SELECT[@name="article"]/CASE', 2)

        self.factory.xfer = DetailAddModify()
        self.call('/diacamma.invoice/detailAddModify', {'bill': 1, 'cat_filter': '2;3'}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'detailAddModify')
        self.assert_count_equal('COMPONENTS/*', 12)
        self.assert_count_equal('COMPONENTS/SELECT[@name="article"]/CASE', 1)

    def test_add_bill_bad(self):
        default_articles()
        self.factory.xfer = BillAddModify()
        self.call('/diacamma.invoice/billAddModify',
                  {'bill_type': 1, 'date': '2015-04-01', 'SAVE': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billAddModify')
        self.factory.xfer = SupportingThirdValid()
        self.call('/diacamma.payoff/supportingThirdValid',
                  {'supporting': 1, 'third': 6}, False)
        self.assert_observer('core.acknowledge', 'diacamma.payoff', 'supportingThirdValid')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}pas de détail{[/font]}")

        self.factory.xfer = DetailAddModify()
        self.call('/diacamma.invoice/detailAddModify',
                  {'SAVE': 'YES', 'bill': 1, 'article': 4, 'designation': 'My article', 'price': '43.72', 'quantity': 2}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'detailAddModify')
        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_count_equal('COMPONENTS/GRID[@name="detail"]/RECORD', 1)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}au moins un article a un compte inconnu !{[/font]}")

        self.factory.xfer = DetailDel()
        self.call('/diacamma.invoice/detailDel',
                  {'CONFIRME': 'YES', 'bill': 1, 'detail': 1}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'detailDel')
        self.factory.xfer = DetailAddModify()
        self.call('/diacamma.invoice/detailAddModify',
                  {'SAVE': 'YES', 'bill': 1, 'article': 3, 'designation': 'My article', 'price': '43.72', 'quantity': 2}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'detailAddModify')
        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_count_equal('COMPONENTS/GRID[@name="detail"]/RECORD', 1)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}au moins un article a un compte inconnu !{[/font]}")

        self.factory.xfer = DetailDel()
        self.call('/diacamma.invoice/detailDel',
                  {'CONFIRME': 'YES', 'bill': 1, 'detail': 2}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'detailDel')
        self.factory.xfer = DetailAddModify()
        self.call('/diacamma.invoice/detailAddModify',
                  {'SAVE': 'YES', 'bill': 1, 'article': 2, 'designation': 'My article', 'price': '43.72', 'quantity': 2}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'detailAddModify')
        self.factory.xfer = SupportingThirdValid()
        self.call('/diacamma.payoff/supportingThirdValid',
                  {'supporting': 1, 'third': 1}, False)
        self.assert_observer('core.acknowledge', 'diacamma.payoff', 'supportingThirdValid')
        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_count_equal('COMPONENTS/GRID[@name="detail"]/RECORD', 1)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}Ce tiers n'a pas de compte correct !{[/font]}")

    def check_list_del_archive(self):
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': -1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/ACTIONS/ACTION', 3)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 0}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 0)
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/ACTIONS/ACTION', 4)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/ACTIONS/ACTION', 5)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 2}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 0)
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/ACTIONS/ACTION', 1)

        self.factory.xfer = BillDel()
        self.call(
            '/diacamma.invoice/billDel', {'CONFIRME': 'YES', 'bill': 1}, False)
        self.assert_observer('core.exception', 'diacamma.invoice', 'billDel')

        self.factory.xfer = BillTransition()
        self.call('/diacamma.invoice/billArchive',
                  {'CONFIRME': 'YES', 'bill': 1, 'TRANSITION': 'archive'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billArchive')

        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': -1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 0)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 3}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/ACTIONS/ACTION', 2)

    def test_compta_bill(self):
        default_articles()
        details = [{'article': 1, 'designation': 'article 1', 'price': '22.50', 'quantity': 3, 'reduce': '5.0'},
                   {'article': 2, 'designation': 'article 2',
                       'price': '3.25', 'quantity': 7},
                   {'article': 0, 'designation': 'article 3',
                       'price': '11.10', 'quantity': 2}]
        self._create_bill(details, 1, '2015-04-01', 6)

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_attrib_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', 'description', "total")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "107.45€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}{[/font]}")
        self.assert_count_equal('ACTIONS/ACTION', 3)

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 0)

        self.factory.xfer = BillTransition()
        self.call('/diacamma.invoice/billValid',
                  {'CONFIRME': 'YES', 'bill': 1, 'withpayoff': False, 'TRANSITION': 'valid'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billValid')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_count_equal('COMPONENTS/*', 14)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="num_txt"]', "A-1")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="status"]', "validé")
        self.assert_count_equal('ACTIONS/ACTION', 4)

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 1)

        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="num"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="date_entry"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="date_value"]', '1 avril 2015')
        description = self.get_first_xpath('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="description"]').text
        self.assertTrue('facture A-1 - 1 avril 2015' in description, description)
        self.assertTrue('[411 Dalton Jack]' in description, description)
        self.assertTrue('107.45€' in description, description)
        self.assertTrue('[709] 709' in description, description)
        self.assertTrue('5.00€' in description, description)
        self.assertTrue('[701] 701' in description, description)
        self.assertTrue('67.50€' in description, description)
        self.assertTrue('[706] 706' in description, description)
        self.assertTrue('22.20€' in description, description)
        self.assertTrue('[707] 707' in description, description)
        self.assertTrue('22.75€' in description, description)

        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': -1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 0}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 0)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)

        self.factory.xfer = BillTransition()
        self.call('/diacamma.invoice/billCancel',
                  {'CONFIRME': 'YES', 'bill': 1, 'TRANSITION': 'cancel'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billCancel')
        self.assert_attrib_equal(
            "ACTION", "id", "diacamma.invoice/billShow")
        self.assert_count_equal("ACTION/PARAM", 1)
        self.assert_xml_equal("ACTION/PARAM[@name='bill']", "2")

        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': -1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 0}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 0)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 2}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 2}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_count_equal('COMPONENTS/*', 13)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "107.45€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="num_txt"]', "---")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="status"]', "en création")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="title"]', "{[br/]}{[center]}{[u]}{[b]}avoir{[/b]}{[/u]}{[/center]}")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="date"]', formats.date_format(date.today(), "DATE_FORMAT"))
        self.factory.xfer = BillAddModify()
        self.call('/diacamma.invoice/billAddModify',
                  {'bill': 2, 'date': '2015-04-01', 'SAVE': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billAddModify')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 2}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="date"]', "1 avril 2015")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}{[/font]}")

        self.factory.xfer = BillTransition()
        self.call('/diacamma.invoice/billValid',
                  {'CONFIRME': 'YES', 'bill': 2, 'withpayoff': False, 'TRANSITION': 'valid'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billValid')

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 2)
        self.assert_xml_equal(
            "COMPONENTS/LABELFORM[@name='result']", '{[center]}{[b]}Produit :{[/b]} 0.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 0.00€{[br/]}{[b]}Trésorerie :{[/b]} 0.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

    def test_add_quotation(self):
        default_articles()
        self._create_bill([{'article': 1, 'designation': 'article 1',
                            'price': '22.50', 'quantity': 3, 'reduce': '5.0'}], 0, '2015-04-01', 6)

        self.factory.xfer = BillTransition()
        self.call('/diacamma.invoice/billValid',
                  {'CONFIRME': 'YES', 'bill': 1, 'withpayoff': False, 'TRANSITION': 'valid'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billValid')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_count_equal('COMPONENTS/*', 10)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="num_txt"]', "A-1")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="status"]', "validé")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="title"]', "{[br/]}{[center]}{[u]}{[b]}devis{[/b]}{[/u]}{[/center]}")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="date"]', "1 avril 2015")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "62.50€")
        self.assert_count_equal('ACTIONS/ACTION', 5)

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 0)

        self.factory.xfer = BillFromQuotation()
        self.call('/diacamma.invoice/billFromQuotation',
                  {'CONFIRME': 'YES', 'bill': 1}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billFromQuotation')
        self.assert_attrib_equal(
            "ACTION", "id", "diacamma.invoice/billShow")
        self.assert_count_equal("ACTION/PARAM", 1)
        self.assert_xml_equal("ACTION/PARAM[@name='bill']", "2")

        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': -1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 0}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 0)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 2}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 0)
        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {'status_filter': 3}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 2}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_count_equal('COMPONENTS/*', 13)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="cost_accounting"]', "open")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "62.50€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="num_txt"]', "---")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="status"]', "en création")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="title"]', "{[br/]}{[center]}{[u]}{[b]}facture{[/b]}{[/u]}{[/center]}")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="date"]', formats.date_format(date.today(), "DATE_FORMAT"))

    def test_compta_asset(self):
        default_articles()
        self._create_bill([{'article': 0, 'designation': 'article A', 'price': '22.20', 'quantity': 3},
                           {'article': 0, 'designation': 'article B', 'price': '11.10', 'quantity': 2}], 2, '2015-04-01', 6)

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 0)

        self.factory.xfer = BillTransition()
        self.call('/diacamma.invoice/billValid',
                  {'CONFIRME': 'YES', 'bill': 1, 'withpayoff': False, 'TRANSITION': 'valid'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billValid')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_count_equal('COMPONENTS/*', 14)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="title"]', "{[br/]}{[center]}{[u]}{[b]}avoir{[/b]}{[/u]}{[/center]}")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "88.80€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="num_txt"]', "A-1")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="status"]', "validé")
        self.assert_count_equal('ACTIONS/ACTION', 3)

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 1)

        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="num"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="date_entry"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="date_value"]', '1 avril 2015')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="link"]', '---')
        description = self.get_first_xpath('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="description"]').text
        self.assertTrue('avoir A-1 - 1 avril 2015' in description, description)
        self.assertTrue('[411 Dalton Jack]' in description, description)
        self.assertTrue('88.80€' in description, description)
        self.assertTrue('[706] 706' in description, description)

        self.check_list_del_archive()

    def test_compta_receive(self):
        default_articles()
        self._create_bill([{'article': 2, 'designation': 'article', 'price': '25.00', 'quantity': 1}],
                          3, '2015-04-01', 6)

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 0)

        self.factory.xfer = BillTransition()
        self.call('/diacamma.invoice/billValid',
                  {'CONFIRME': 'YES', 'bill': 1, 'withpayoff': False, 'TRANSITION': 'valid'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billValid')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_count_equal('COMPONENTS/*', 13)
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "25.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="num_txt"]', "A-1")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="status"]', "validé")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="title"]', "{[br/]}{[center]}{[u]}{[b]}reçu{[/b]}{[/u]}{[/center]}")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="date"]', "1 avril 2015")
        self.assert_count_equal('ACTIONS/ACTION', 4)

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 1)

        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="num"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="date_entry"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="date_value"]', '1 avril 2015')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="link"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="costaccounting"]', '---')
        description = self.get_first_xpath('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="description"]').text
        self.assertTrue('reçu A-1 - 1 avril 2015' in description, description)
        self.assertTrue('[411 Dalton Jack]' in description, description)
        self.assertTrue('25.00€' in description, description)
        self.assertTrue('[707] 707' in description, description)
        self.check_list_del_archive()

    def test_bill_price_with_vat(self):
        default_articles()
        Parameter.change_value('invoice-vat-mode', '2')
        Params.clear()
        details = [{'article': 1, 'designation': 'article 1', 'price': '22.50', 'quantity': 3, 'reduce': '5.0'},  # code 701
                   {'article': 2, 'designation': 'article 2',  # +5% vat => 1.08 - code 707
                       'price': '3.25', 'quantity': 7},
                   {'article': 0, 'designation': 'article 3',
                       'price': '11.10', 'quantity': 2},  # code 709
                   {'article': 5, 'designation': 'article 4', 'price': '6.33', 'quantity': 3.25}]  # +20% vat => 3.43  - code 701
        self._create_bill(details, 1, '2015-04-01', 6)

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)

        self.assert_count_equal('COMPONENTS/GRID[@name="detail"]/HEADER', 8)
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/HEADER[@name="price_txt"]', 'prix TTC')
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/HEADER[@name="total"]', 'total TTC')
        self.assert_count_equal('COMPONENTS/GRID[@name="detail"]/RECORD', 4)
        self.assert_attrib_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', 'description', "total HT")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}{[/font]}")
        self.assert_attrib_equal('COMPONENTS/LABELFORM[@name="total_incltax"]', 'description', "total TTC")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_incltax"]', "128.02€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="vta_sum"]', "4.51€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "123.51€")

        self.assert_count_equal('ACTIONS/ACTION', 3)

        self.factory.xfer = BillTransition()
        self.call('/diacamma.invoice/billValid',
                  {'CONFIRME': 'YES', 'bill': 1, 'withpayoff': False, 'TRANSITION': 'valid'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billValid')

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 1)
        description = self.get_first_xpath('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="description"]').text
        self.assertTrue('[411 Dalton Jack]' in description, description)
        self.assertTrue('[4455] 4455' in description, description)
        self.assertTrue('128.02€' in description, description)
        self.assertTrue('4.51€' in description, description)
        self.assert_xml_equal(
            "COMPONENTS/LABELFORM[@name='result']", '{[center]}{[b]}Produit :{[/b]} 123.51€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 123.51€{[br/]}{[b]}Trésorerie :{[/b]} 0.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/HEADER', 7)
        self.assert_xml_equal('COMPONENTS/GRID[@name="bill"]/HEADER[@name="total"]', "total TTC")

    def test_bill_price_without_vat(self):
        default_articles()
        Parameter.change_value('invoice-vat-mode', '1')
        Params.clear()
        details = [{'article': 1, 'designation': 'article 1', 'price': '22.50', 'quantity': 3, 'reduce': '5.0'},
                   {'article': 2, 'designation': 'article 2',  # +5% vat => 1.14
                       'price': '3.25', 'quantity': 7},
                   {'article': 0, 'designation': 'article 3',
                       'price': '11.10', 'quantity': 2},
                   {'article': 5, 'designation': 'article 4', 'price': '6.33', 'quantity': 3.25}]  # +20% vat => 4.11
        self._create_bill(details, 1, '2015-04-01', 6)

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': 1}, False)

        self.assert_count_equal('COMPONENTS/GRID[@name="detail"]/HEADER', 8)
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/HEADER[@name="price_txt"]', 'prix HT')
        self.assert_xml_equal('COMPONENTS/GRID[@name="detail"]/HEADER[@name="total"]', 'total HT')
        self.assert_count_equal('COMPONENTS/GRID[@name="detail"]/RECORD', 4)
        self.assert_attrib_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', 'description', "total HT")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="info"]', "{[font color=\"red\"]}{[/font]}")
        self.assert_attrib_equal('COMPONENTS/LABELFORM[@name="total_incltax"]', 'description', "total TTC")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_incltax"]', "133.27€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="vta_sum"]', "5.25€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "128.02€")

        self.assert_count_equal('ACTIONS/ACTION', 3)

        self.factory.xfer = BillTransition()
        self.call('/diacamma.invoice/billValid',
                  {'CONFIRME': 'YES', 'bill': 1, 'withpayoff': False, 'TRANSITION': 'valid'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billValid')

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 1)

        description = self.get_first_xpath('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="description"]').text
        self.assertTrue('[411 Dalton Jack]' in description, description)
        self.assertTrue('[4455] 4455' in description, description)
        self.assertTrue('133.27€' in description, description)
        self.assertTrue('5.25€' in description, description)
        self.assert_xml_equal(
            "COMPONENTS/LABELFORM[@name='result']", '{[center]}{[b]}Produit :{[/b]} 128.02€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 128.02€{[br/]}{[b]}Trésorerie :{[/b]} 0.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

        self.factory.xfer = BillList()
        self.call('/diacamma.invoice/billList', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billList')
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/RECORD', 1)
        self.assert_count_equal('COMPONENTS/GRID[@name="bill"]/HEADER', 7)
        self.assert_xml_equal('COMPONENTS/GRID[@name="bill"]/HEADER[@name="total"]', "total HT")

    def test_statistic(self):
        default_articles()
        details = [
            {'article': 0, 'designation': 'article 0', 'price': '20.00', 'quantity': 15}]
        self._create_bill(details, 0, '2015-04-01', 6, True)  # 59.50
        details = [{'article': 1, 'designation': 'article 1', 'price': '22.00', 'quantity': 3, 'reduce': '5.0'},
                   {'article': 2, 'designation': 'article 2', 'price': '3.25', 'quantity': 7}]
        self._create_bill(details, 1, '2015-04-01', 6, True)  # 83.75
        details = [{'article': 0, 'designation': 'article 0', 'price': '50.00', 'quantity': 2},
                   {'article': 5, 'designation': 'article 5', 'price': '6.33', 'quantity': 6.75}]
        self._create_bill(details, 3, '2015-04-01', 4, True)  # 142.73
        details = [{'article': 1, 'designation': 'article 1', 'price': '23.00', 'quantity': 3},
                   {'article': 5, 'designation': 'article 5', 'price': '6.33', 'quantity': 3.50}]
        self._create_bill(details, 1, '2015-04-01', 5, True)  # 91.16
        details = [{'article': 2, 'designation': 'article 2', 'price': '3.30', 'quantity': 5},
                   {'article': 5, 'designation': 'article 5', 'price': '6.35', 'quantity': 4.25, 'reduce': '2.0'}]
        self._create_bill(details, 1, '2015-04-01', 6, True)  # 41.49
        details = [
            {'article': 5, 'designation': 'article 5', 'price': '6.33', 'quantity': 1.25}]
        self._create_bill(details, 2, '2015-04-01', 4, True)  # 7.91

        self.factory.xfer = BillStatistic()
        self.call('/diacamma.invoice/billStatistic', {}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billStatistic')
        self.assert_count_equal('COMPONENTS/*', 7)

        self.assert_count_equal('COMPONENTS/GRID[@name="articles"]/HEADER', 5)
        self.assert_count_equal('COMPONENTS/GRID[@name="articles"]/RECORD', 5)
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[1]/VALUE[@name="article"]', "ABC1")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[1]/VALUE[@name="amount"]', "130.00€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[1]/VALUE[@name="number"]', "6.00")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[2]/VALUE[@name="article"]', "---")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[2]/VALUE[@name="amount"]', "100.00€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[2]/VALUE[@name="number"]', "2.00")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[2]/VALUE[@name="mean"]', "50.00€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[2]/VALUE[@name="ratio"]', "28.47 %")

        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[3]/VALUE[@name="article"]', "ABC5")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[3]/VALUE[@name="amount"]', "81.97€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[3]/VALUE[@name="number"]', "13.25")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[4]/VALUE[@name="article"]', "ABC2")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[4]/VALUE[@name="amount"]', "39.25€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[4]/VALUE[@name="number"]', "12.00")
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[5]/VALUE[@name="article"]', '{[b]}total{[/b]}')
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[5]/VALUE[@name="amount"]', '{[b]}351.22€{[/b]}')
        self.assert_xml_equal('COMPONENTS/GRID[@name="articles"]/RECORD[5]/VALUE[@name="number"]', '{[b]}---{[/b]}')

        self.assert_count_equal('COMPONENTS/GRID[@name="customers"]/HEADER', 3)
        self.assert_count_equal('COMPONENTS/GRID[@name="customers"]/RECORD', 4)
        self.assert_xml_equal('COMPONENTS/GRID[@name="customers"]/RECORD[1]/VALUE[@name="customer"]', "Minimum")
        self.assert_xml_equal('COMPONENTS/GRID[@name="customers"]/RECORD[1]/VALUE[@name="amount"]', "134.82€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="customers"]/RECORD[2]/VALUE[@name="customer"]', "Dalton Jack")
        self.assert_xml_equal('COMPONENTS/GRID[@name="customers"]/RECORD[2]/VALUE[@name="amount"]', "125.24€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="customers"]/RECORD[2]/VALUE[@name="ratio"]', "35.66 %")
        self.assert_xml_equal('COMPONENTS/GRID[@name="customers"]/RECORD[3]/VALUE[@name="customer"]', "Dalton William")
        self.assert_xml_equal('COMPONENTS/GRID[@name="customers"]/RECORD[3]/VALUE[@name="amount"]', "91.16€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="customers"]/RECORD[4]/VALUE[@name="customer"]', '{[b]}total{[/b]}')
        self.assert_xml_equal('COMPONENTS/GRID[@name="customers"]/RECORD[4]/VALUE[@name="amount"]', '{[b]}351.22€{[/b]}')

        self.factory.xfer = BillStatisticPrint()
        self.call(
            '/diacamma.invoice/billStatisticPrint', {'PRINT_MODE': '4'}, False)
        self.assert_observer('core.print', 'diacamma.invoice', 'billStatisticPrint')
        csv_value = b64decode(
            six.text_type(self.get_first_xpath('PRINT').text)).decode("utf-8")
        content_csv = csv_value.split('\n')
        self.assertEqual(len(content_csv), 24, str(content_csv))
        self.assertEqual(content_csv[1].strip(), '"Impression des statistiques"')
        self.assertEqual(
            content_csv[12].strip(), '"total";"351.22€";"100.00 %";')
        self.assertEqual(
            content_csv[20].strip(), '"total";"351.22€";"---";"---";"100.00 %";')

        self.factory.xfer = BillPrint()
        self.call(
            '/diacamma.invoice/billPrint', {'bill': '1;2;3;4;5', 'PRINT_MODE': 3, 'MODEL': 8}, False)
        self.assert_observer('core.print', 'diacamma.invoice', 'billPrint')

    def test_payoff_bill(self):
        default_articles()
        details = [{'article': 0, 'designation': 'article 0', 'price': '100.00', 'quantity': 1}]
        bill_id = self._create_bill(details, 1, '2015-04-01', 6, True)  # 59.50

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList', {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 1)
        self.assert_xml_equal("COMPONENTS/LABELFORM[@name='result']", '{[center]}{[b]}Produit :{[/b]} 100.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 100.00€{[br/]}{[b]}Trésorerie :{[/b]} 0.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': bill_id}, False)
        self.assert_xml_equal('CONTEXT/PARAM[@name="supporting"]', bill_id)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "100.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_payed"]', "0.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_rest_topay"]', "100.00€")
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/HEADER', 6)
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/RECORD', 0)
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/ACTIONS/ACTION', 3)

        self.factory.xfer = PayoffAddModify()
        self.call('/diacamma.payoff/payoffAddModify', {'supporting': bill_id}, False)
        self.assert_observer('core.custom', 'diacamma.payoff', 'payoffAddModify')
        self.assert_count_equal('COMPONENTS/*', 7)
        self.assert_xml_equal('COMPONENTS/FLOAT[@name="amount"]', "100.00")
        self.assert_attrib_equal('COMPONENTS/FLOAT[@name="amount"]', 'max', "100.0")
        self.assert_xml_equal('COMPONENTS/EDIT[@name="payer"]', "Dalton Jack")

        self.factory.xfer = PayoffAddModify()
        self.call('/diacamma.payoff/payoffAddModify', {'SAVE': 'YES', 'supporting': bill_id, 'amount': '60.0', 'payer': "Ma'a Dalton", 'date': '2015-04-03', 'mode': 0, 'reference': 'abc', 'bank_account': 0}, False)
        self.assert_observer('core.acknowledge', 'diacamma.payoff', 'payoffAddModify')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': bill_id}, False)
        self.assert_xml_equal('CONTEXT/PARAM[@name="supporting"]', bill_id)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "100.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_payed"]', "60.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_rest_topay"]', "40.00€")
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/HEADER', 6)
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/RECORD', 1)
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/ACTIONS/ACTION', 3)
        self.assert_xml_equal('COMPONENTS/GRID[@name="payoff"]/RECORD[1]/VALUE[@name="date"]', "3 avril 2015")
        self.assert_xml_equal('COMPONENTS/GRID[@name="payoff"]/RECORD[1]/VALUE[@name="mode"]', "espèce")
        self.assert_xml_equal('COMPONENTS/GRID[@name="payoff"]/RECORD[1]/VALUE[@name="value"]', "60.00€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="payoff"]/RECORD[1]/VALUE[@name="payer"]', "Ma'a Dalton")
        self.assert_xml_equal('COMPONENTS/GRID[@name="payoff"]/RECORD[1]/VALUE[@name="reference"]', "abc")
        self.assert_xml_equal('COMPONENTS/GRID[@name="payoff"]/RECORD[1]/VALUE[@name="bank_account"]', "---")

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 2)
        description = self.get_first_xpath('COMPONENTS/GRID[@name="entryaccount"]/RECORD[2]/VALUE[@name="description"]').text
        self.assertTrue('[531] 531' in description, description)
        self.assert_xml_equal("COMPONENTS/LABELFORM[@name='result']", '{[center]}{[b]}Produit :{[/b]} 100.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 100.00€{[br/]}{[b]}Trésorerie :{[/b]} 60.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

        self.factory.xfer = PayoffAddModify()
        self.call('/diacamma.payoff/payoffAddModify', {'supporting': bill_id}, False)
        self.assert_observer('core.custom', 'diacamma.payoff', 'payoffAddModify')
        self.assert_xml_equal('COMPONENTS/FLOAT[@name="amount"]', "40.00")
        self.assert_attrib_equal('COMPONENTS/FLOAT[@name="amount"]', 'max', "40.0")

        self.factory.xfer = PayoffAddModify()
        self.call('/diacamma.payoff/payoffAddModify', {'SAVE': 'YES', 'supporting': bill_id, 'amount': '40.0', 'payer': "Dalton Jack", 'date': '2015-04-04', 'mode': 2, 'reference': 'efg', 'bank_account': 2}, False)
        self.assert_observer('core.acknowledge', 'diacamma.payoff', 'payoffAddModify')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': bill_id}, False)
        self.assert_xml_equal('CONTEXT/PARAM[@name="supporting"]', bill_id)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "100.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_payed"]', "100.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_rest_topay"]', "0.00€")
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/HEADER', 6)
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/RECORD', 2)
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/ACTIONS/ACTION', 2)

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList', {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 3)
        description = self.get_first_xpath('COMPONENTS/GRID[@name="entryaccount"]/RECORD[3]/VALUE[@name="description"]').text
        self.assertTrue('[581] 581' in description, description)
        self.assert_xml_equal("COMPONENTS/LABELFORM[@name='result']", '{[center]}{[b]}Produit :{[/b]} 100.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 100.00€{[br/]}{[b]}Trésorerie :{[/b]} 100.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

    def test_payoff_avoid(self):
        default_articles()
        details = [
            {'article': 0, 'designation': 'article 0', 'price': '50.00', 'quantity': 1}]
        bill_id = self._create_bill(details, 2, '2015-04-01', 6, True)  # 59.50

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 1)
        self.assert_xml_equal(
            "COMPONENTS/LABELFORM[@name='result']", '{[center]}{[b]}Produit :{[/b]} -50.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} -50.00€{[br/]}{[b]}Trésorerie :{[/b]} 0.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

        self.factory.xfer = PayoffAddModify()
        self.call(
            '/diacamma.payoff/payoffAddModify', {'supporting': bill_id, 'mode': 3}, False)
        self.assert_observer('core.custom', 'diacamma.payoff', 'payoffAddModify')
        self.assert_count_equal('COMPONENTS/*', 7)
        self.assert_count_equal('COMPONENTS/SELECT[@name="bank_account"]/CASE', 2)

        self.factory.xfer = PayoffAddModify()
        self.call(
            '/diacamma.payoff/payoffAddModify', {'SAVE': 'YES', 'supporting': bill_id, 'amount': '50.0', 'date': '2015-04-04', 'mode': 3, 'reference': 'ijk', 'bank_account': 1}, False)
        self.assert_observer('core.acknowledge', 'diacamma.payoff', 'payoffAddModify')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': bill_id}, False)
        self.assert_xml_equal('CONTEXT/PARAM[@name="supporting"]', bill_id)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "50.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_payed"]', "50.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_rest_topay"]', "0.00€")
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/HEADER', 5)
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/RECORD', 1)
        self.assert_count_equal('COMPONENTS/GRID[@name="payoff"]/ACTIONS/ACTION', 2)
        self.assert_xml_equal('COMPONENTS/GRID[@name="payoff"]/RECORD[1]/VALUE[@name="date"]', "4 avril 2015")
        self.assert_xml_equal('COMPONENTS/GRID[@name="payoff"]/RECORD[1]/VALUE[@name="mode"]', "carte de crédit")
        self.assert_xml_equal('COMPONENTS/GRID[@name="payoff"]/RECORD[1]/VALUE[@name="value"]', "50.00€")
        self.assert_xml_equal('COMPONENTS/GRID[@name="payoff"]/RECORD[1]/VALUE[@name="reference"]', "ijk")
        self.assert_xml_equal('COMPONENTS/GRID[@name="payoff"]/RECORD[1]/VALUE[@name="bank_account"]', "My bank")

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 2)
        description = self.get_first_xpath('COMPONENTS/GRID[@name="entryaccount"]/RECORD[2]/VALUE[@name="description"]').text
        self.assertTrue('[512] 512' in description, description)
        self.assert_xml_equal(
            "COMPONENTS/LABELFORM[@name='result']", '{[center]}{[b]}Produit :{[/b]} -50.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} -50.00€{[br/]}{[b]}Trésorerie :{[/b]} -50.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

        self.factory.xfer = PayoffDel()
        self.call(
            '/diacamma.payoff/payoffDel', {'CONFIRME': 'YES', 'payoff': 1}, False)
        self.assert_observer('core.acknowledge', 'diacamma.payoff', 'payoffDel')

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 1)
        self.assert_xml_equal(
            "COMPONENTS/LABELFORM[@name='result']", '{[center]}{[b]}Produit :{[/b]} -50.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} -50.00€{[br/]}{[b]}Trésorerie :{[/b]} 0.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

        self.factory.xfer = BillPrint()
        self.call(
            '/diacamma.invoice/billPrint', {'bill': '1', 'PRINT_MODE': 3, 'MODEL': 9}, False)
        self.assert_observer('core.print', 'diacamma.invoice', 'billPrint')

    def test_payoff_multi(self):
        default_articles()
        details = [{'article': 0, 'designation': 'article 0', 'price': '100.00', 'quantity': 1}]
        bill_id1 = self._create_bill(details, 1, '2015-04-01', 6, True)
        details = [{'article': 0, 'designation': 'article 0', 'price': '50.00', 'quantity': 1}]
        bill_id2 = self._create_bill(details, 1, '2015-04-01', 4, True)

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList', {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 2)
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="link"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[2]/VALUE[@name="link"]', '---')
        self.assert_xml_equal("COMPONENTS/LABELFORM[@name='result']",
                              '{[center]}{[b]}Produit :{[/b]} 150.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 150.00€{[br/]}{[b]}Trésorerie :{[/b]} 0.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

        self.factory.xfer = BillMultiPay()
        self.call('/diacamma.invoice/billMultiPay', {'bill': '%s;%s' % (bill_id1, bill_id2)}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billMultiPay')
        self.assert_attrib_equal("ACTION", "id", "diacamma.payoff/payoffAddModify")
        self.assert_count_equal("ACTION/PARAM", 1)
        self.assert_xml_equal("ACTION/PARAM[@name='supportings']", '%s;%s' % (bill_id1, bill_id2))

        self.factory.xfer = PayoffAddModify()
        self.call('/diacamma.payoff/payoffAddModify', {'supportings': '%s;%s' % (bill_id1, bill_id2)}, False)
        self.assert_observer('core.custom', 'diacamma.payoff', 'payoffAddModify')
        self.assert_xml_equal('COMPONENTS/FLOAT[@name="amount"]', "150.00")
        self.assert_attrib_equal('COMPONENTS/FLOAT[@name="amount"]', 'max', "150.0")
        self.assert_xml_equal('COMPONENTS/EDIT[@name="payer"]', "Dalton Jack")
        self.assert_count_equal('COMPONENTS/SELECT[@name="repartition"]/CASE', 2)
        self.assert_xml_equal('COMPONENTS/SELECT[@name="repartition"]', "0")

        self.factory.xfer = PayoffAddModify()
        self.call('/diacamma.payoff/payoffAddModify', {'SAVE': 'YES', 'supportings': '%s;%s' % (bill_id1, bill_id2),
                                                       'amount': '100.0', 'date': '2015-04-04', 'mode': 0, 'reference': '', 'bank_account': 0, 'payer': "Ma'a Dalton"}, False)
        self.assert_observer('core.acknowledge', 'diacamma.payoff', 'payoffAddModify')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': bill_id1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "100.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_payed"]', "66.67€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_rest_topay"]', "33.33€")

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': bill_id2}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "50.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_payed"]', "33.33€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_rest_topay"]', "16.67€")

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 3)
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="link"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[2]/VALUE[@name="link"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[3]/VALUE[@name="link"]', '---')
        self.assert_xml_equal("COMPONENTS/LABELFORM[@name='result']",
                              '{[center]}{[b]}Produit :{[/b]} 150.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 150.00€{[br/]}{[b]}Trésorerie :{[/b]} 100.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

    def test_payoff_multi_samethird(self):
        default_articles()
        details = [{'article': 0, 'designation': 'article 0', 'price': '100.00', 'quantity': 1}]
        bill_id1 = self._create_bill(details, 1, '2015-04-01', 6, True)
        details = [{'article': 0, 'designation': 'article 0', 'price': '50.00', 'quantity': 1}]
        bill_id2 = self._create_bill(details, 1, '2015-04-01', 6, True)

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 2)
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="link"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[2]/VALUE[@name="link"]', '---')
        self.assert_xml_equal("COMPONENTS/LABELFORM[@name='result']",
                              '{[center]}{[b]}Produit :{[/b]} 150.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 150.00€{[br/]}{[b]}Trésorerie :{[/b]} 0.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

        self.factory.xfer = BillMultiPay()
        self.call('/diacamma.invoice/billMultiPay',
                  {'bill': '%s;%s' % (bill_id1, bill_id2)}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billMultiPay')
        self.assert_attrib_equal("ACTION", "id", "diacamma.payoff/payoffAddModify")
        self.assert_count_equal("ACTION/PARAM", 1)
        self.assert_xml_equal("ACTION/PARAM[@name='supportings']", '%s;%s' % (bill_id1, bill_id2))

        self.factory.xfer = PayoffAddModify()
        self.call('/diacamma.payoff/payoffAddModify', {'supportings': '%s;%s' % (bill_id1, bill_id2)}, False)
        self.assert_observer('core.custom', 'diacamma.payoff', 'payoffAddModify')
        self.assert_xml_equal('COMPONENTS/FLOAT[@name="amount"]', "150.00")
        self.assert_attrib_equal('COMPONENTS/FLOAT[@name="amount"]', 'max', "150.0")
        self.assert_xml_equal('COMPONENTS/EDIT[@name="payer"]', "Dalton Jack")
        self.assert_count_equal('COMPONENTS/SELECT[@name="repartition"]/CASE', 2)
        self.assert_xml_equal('COMPONENTS/SELECT[@name="repartition"]', "0")

        self.factory.xfer = PayoffAddModify()
        self.call('/diacamma.payoff/payoffAddModify', {'SAVE': 'YES', 'supportings': '%s;%s' % (bill_id1, bill_id2), 'amount': '150.0',
                                                       'date': '2015-04-04', 'mode': 0, 'reference': '', 'bank_account': 0, 'payer': "Ma'a Dalton", "repartition": 0}, False)
        self.assert_observer('core.acknowledge', 'diacamma.payoff', 'payoffAddModify')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': bill_id1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "100.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_payed"]', "100.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_rest_topay"]', "0.00€")

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': bill_id2}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "50.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_payed"]', "50.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_rest_topay"]', "0.00€")

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 3)
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[3]/VALUE[@name="link"]', 'A')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[2]/VALUE[@name="link"]', 'A')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="link"]', 'A')
        self.assert_xml_equal("COMPONENTS/LABELFORM[@name='result']",
                              '{[center]}{[b]}Produit :{[/b]} 150.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 150.00€{[br/]}{[b]}Trésorerie :{[/b]} 150.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

    def test_payoff_multi_bydate(self):
        default_articles()
        details = [{'article': 0, 'designation': 'article 0', 'price': '100.00', 'quantity': 1}]
        bill_id1 = self._create_bill(details, 1, '2015-04-01', 6, True)
        details = [{'article': 0, 'designation': 'article 0', 'price': '50.00', 'quantity': 1}]
        bill_id2 = self._create_bill(details, 1, '2015-04-03', 6, True)

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 2)
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="link"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[2]/VALUE[@name="link"]', '---')
        self.assert_xml_equal("COMPONENTS/LABELFORM[@name='result']",
                              '{[center]}{[b]}Produit :{[/b]} 150.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 150.00€{[br/]}{[b]}Trésorerie :{[/b]} 0.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

        self.factory.xfer = BillMultiPay()
        self.call('/diacamma.invoice/billMultiPay',
                  {'bill': '%s;%s' % (bill_id1, bill_id2)}, False)
        self.assert_observer('core.acknowledge', 'diacamma.invoice', 'billMultiPay')
        self.assert_attrib_equal("ACTION", "id", "diacamma.payoff/payoffAddModify")
        self.assert_count_equal("ACTION/PARAM", 1)
        self.assert_xml_equal("ACTION/PARAM[@name='supportings']", '%s;%s' % (bill_id1, bill_id2))

        self.factory.xfer = PayoffAddModify()
        self.call('/diacamma.payoff/payoffAddModify', {'supportings': '%s;%s' % (bill_id1, bill_id2)}, False)
        self.assert_observer('core.custom', 'diacamma.payoff', 'payoffAddModify')
        self.assert_xml_equal('COMPONENTS/FLOAT[@name="amount"]', "150.00")
        self.assert_attrib_equal('COMPONENTS/FLOAT[@name="amount"]', 'max', "150.0")
        self.assert_xml_equal('COMPONENTS/EDIT[@name="payer"]', "Dalton Jack")
        self.assert_count_equal('COMPONENTS/SELECT[@name="repartition"]/CASE', 2)
        self.assert_xml_equal('COMPONENTS/SELECT[@name="repartition"]', "0")

        self.factory.xfer = PayoffAddModify()
        self.call('/diacamma.payoff/payoffAddModify', {'SAVE': 'YES', 'supportings': '%s;%s' % (bill_id1, bill_id2), 'amount': '120.0',
                                                       'date': '2015-04-07', 'mode': 0, 'reference': '', 'bank_account': 0, 'payer': "Ma'a Dalton", "repartition": 1}, False)
        self.assert_observer('core.acknowledge', 'diacamma.payoff', 'payoffAddModify')

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': bill_id1}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "100.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_payed"]', "100.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_rest_topay"]', "0.00€")

        self.factory.xfer = BillShow()
        self.call('/diacamma.invoice/billShow', {'bill': bill_id2}, False)
        self.assert_observer('core.custom', 'diacamma.invoice', 'billShow')
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_excltax"]', "50.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_payed"]', "20.00€")
        self.assert_xml_equal('COMPONENTS/LABELFORM[@name="total_rest_topay"]', "30.00€")

        self.factory.xfer = EntryAccountList()
        self.call('/diacamma.accounting/entryAccountList',
                  {'year': '1', 'journal': '-1', 'filter': '0'}, False)
        self.assert_observer('core.custom', 'diacamma.accounting', 'entryAccountList')
        self.assert_count_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD', 3)
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[3]/VALUE[@name="link"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[2]/VALUE[@name="link"]', '---')
        self.assert_xml_equal('COMPONENTS/GRID[@name="entryaccount"]/RECORD[1]/VALUE[@name="link"]', '---')
        self.assert_xml_equal("COMPONENTS/LABELFORM[@name='result']",
                              '{[center]}{[b]}Produit :{[/b]} 150.00€ - {[b]}Charge :{[/b]} 0.00€ = {[b]}Résultat :{[/b]} 150.00€{[br/]}{[b]}Trésorerie :{[/b]} 120.00€ - {[b]}Validé :{[/b]} 0.00€{[/center]}')

    def test_send_bill(self):
        default_articles()
        configSMTP('localhost', 1025)
        server = TestReceiver()
        server.start(1025)
        try:
            self.assertEqual(0, server.count())
            details = [
                {'article': 0, 'designation': 'article 0', 'price': '100.00', 'quantity': 1}]
            bill_id = self._create_bill(
                details, 1, '2015-04-01', 6, True)  # 59.50
            self.factory.xfer = PayableEmail()
            self.call('/diacamma.payoff/payableEmail',
                      {'item_name': 'bill', 'bill': bill_id}, False)
            self.assert_observer('core.custom', 'diacamma.payoff', 'payableEmail')
            self.assert_count_equal('COMPONENTS/*', 4)
            self.assert_xml_equal('COMPONENTS/EDIT[@name="subject"]', 'facture A-1 - 1 avril 2015')
            self.assert_xml_equal(
                'COMPONENTS/MEMO[@name="message"]', 'Jack Dalton\n\nVeuillez trouver ci-Joint à ce courriel facture A-1 - 1 avril 2015.\n\nSincères salutations')

            self.factory.xfer = PayableEmail()
            self.call('/diacamma.payoff/payableEmail',
                      {'bill': bill_id, 'OK': 'YES', 'item_name': 'bill', 'subject': 'my bill', 'message': 'this is a bill.', 'model': 8}, False)
            self.assert_observer('core.acknowledge', 'diacamma.payoff', 'payableEmail')
            self.assertEqual(1, server.count())
            self.assertEqual(
                'mr-sylvestre@worldcompany.com', server.get(0)[1])
            self.assertEqual(
                ['Jack.Dalton@worldcompany.com', 'mr-sylvestre@worldcompany.com'], server.get(0)[2])
            msg, msg_file = server.check_first_message('my bill', 2, {'To': 'Jack.Dalton@worldcompany.com'})
            self.assertEqual('text/html', msg.get_content_type())
            self.assertEqual(
                'base64', msg.get('Content-Transfer-Encoding', ''))
            self.assertEqual(
                '<html>this is a bill.</html>', decode_b64(msg.get_payload()))
            self.assertTrue(
                'facture_A-1_Dalton Jack.pdf' in msg_file.get('Content-Type', ''), msg_file.get('Content-Type', ''))
            self.assertEqual(
                "%PDF".encode('ascii', 'ignore'), b64decode(msg_file.get_payload())[:4])
        finally:
            server.stop()
