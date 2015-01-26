# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   Author: Christophe Combelles                                              #
#   Copyright 2015 Anybox                                                     #
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU Affero General Public License as            #
#   published by the Free Software Foundation, either version 3 of the        #
#   License, or (at your option) any later version.                           #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU Affero General Public License for more details.                       #
#                                                                             #
#   You should have received a copy of the GNU Affero General Public License  #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

from openerp.osv import orm
import json
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer


class AccountStatementCompletionRule(orm.Model):

    _inherit = "account.statement.completion.rule"

    def _get_functions(self, cr, uid, context=None):
        res = super(AccountStatementCompletionRule, self)._get_functions(
            cr, uid, context=context)
        res.append(
            ('get_from_prediction', 'From matching data of the last 1000 statement lines')
        )
        return res

    def get_from_prediction(self, cr, uid, st_line, context=None):
        """
        Match the partner based on the last N partner matchings and the partner database

        :param int/long st_line: read of the concerned
        account.bank.statement.line

        :return:
            A dict of value that can be passed directly to the write method of
            the statement line or {}
           {'partner_id': value,
            'account_id': value,

            ...}
        """
        res = {}
        if not st_line:
            return res
        cr.execute('select date, name, ref, additionnal_bank_fields, partner_id, account_id '
                   'from account_bank_statement_line where partner_id is not NULL '
                   'order by date desc, id limit 1000;')

        # construct the dataset from existing statements
        st_line['additionnal_bank_fields'] = json.dumps(st_line['additionnal_bank_fields'])
        dataset = [(r['name'].upper() or '',
                   r['partner_id'])
                   for r in cr.dictfetchall()]
        # add existing partner names in the dataset to improve prediction bootstrapping
        cr.execute('select id, name from res_partner where is_company=true')
        dataset += [(r['name'].upper() or '',
                    r['id'])
                    for r in cr.dictfetchall()]
        if len(dataset) <= 3:
            return {}
        vectorizer = CountVectorizer(min_df=0, analyzer='char', ngram_range=(3, 3))
        # fit and transform the dataset into a training vector
        training_vector = vectorizer.fit_transform([d[0] for d in dataset]
                                                   + [st_line['name'].upper()])
        classifier = svm.LinearSVC()
        categories = [d[1] for d in dataset]
        classifier.fit(training_vector[:-1], categories)
        partner_id = classifier.predict(training_vector[-1])[0]
        return {'partner_id': partner_id}
