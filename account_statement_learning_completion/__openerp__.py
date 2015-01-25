###############################################################################
#
#    account_statement_learning_completion module for Odoo
#    Copyright (C) 2015 Anybox (<http://anybox.fr>)
#
#    account_statement_learning_completion is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License v3 or later
#    as published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    account_statement_learning_completion is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License v3 or later for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    v3 or later along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': 'Bank statement completion using Machine Learning',
    'version': '0.1',
    'description': """This module uses a Machine Learning algorithm (Support Vector Classification) to
automatically recognize partners in bank statements, based on the last 1000
matchings
    """,
    'summary': "",
    'icon': '/account_statement_learning_completion/static/description/icon.png',
    'author': 'Christophe Combelles',
    'website': 'http://anybox.fr',
    'license': 'AGPL-3',
    'category': 'Finance',
    'depends': ['account_statement_base_completion'],
    'data': [
        #'security/ir.model.access.csv',
        'statement.xml',
        'data.xml',
    ],
    'demo': [ ],
    'auto_install': False,
    'web': False,
    'post_load': None,
    'application': False,
    'installable': True,
    'sequence': 150,
}
