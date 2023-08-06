# -*- coding:utf-8 -*-
from sklearn import tree

__author__ = 'denishuang'

STATIC_FIELDS = ['member_id', 'reg_date', 'pay_date', 'pay_amount', 'gid', 'paid', 'reg_count']

import pandas as pd
import numpy as np


class BaseForcaster(object):
    def __init__(self, data, dimensions=None, train_rate=5, field_map={}):
        self.data = data
        self.mid_field = field_map.get('member_id', 'member_id')
        self.payment_field = field_map.get('pay_amount', 'pay_amount')
        self.predict_field = field_map.get('predict_pay_amount', 'predict_pay_amount')
        self.dimensions = dimensions or [c for c in data.columns
                                         if c not in field_map.values()
                                         and data[c].dtype != np.dtype('<M8[ns]')
                                         ]

        self.normalize()
        self.train_rate = train_rate
        self.train_set, self.test_set = self.split_train_test()

    def split_train_test(self):
        df = self.data
        df['set'] = df['group'] < self.train_rate and 'train' or 'test'
        return df[df['set']=='train'], df[df['set']=='test']

    def normalize(self):
        df = self.data
        df.fillna(0, inplace=True)
        df['group'] = df[self.mid_field] % 10

    def train(self):
        raise Exception("unimplemented!")

    def predict(self, df):
        raise Exception("unimplemented!")

    def performance(self, df):
        return df[['set','group',self.payment_field, self.predict_field]].groupby(['set','group']).sum()

    def run(self):
        self.train()
        return self.performance(self.predict(self.data))



class DecisionTreeForcaster(BaseForcaster):
    def __init__(self, data, dimensions=None, train_rate=5, field_map={}):
        super(DecisionTreeForcaster, self).__init__(data, dimensions, train_rate, field_map)
        self.tree = tree.DecisionTreeRegressor()

    def normalize(self):
        super(DecisionTreeForcaster, self).normalize()
        df = self.data
        cats = {}
        for d in self.dimensions:
            if df[d].dtype == 'object':
                cc = pd.Categorical(df[d])
                cats[d] = cc.categories
                df[d] = cc.codes
        self.categories = cats

    def train(self):
        Y = self.train_set[self.payment_field]
        X = self.train_set[self.dimensions]
        self.tree.fit(X, Y)

    def predict(self, df):
        df[self.predict_field] = self.tree.predict(df[self.dimensions])
        return df


class Forcaster(object):
    def __init__(self, data, dimensions=None, train_rate=5, field_map={}):
        self.data = data
        self.data.rename(columns=field_map, inplace=True)
        self.dimensions = dimensions or [c for c in data.columns if c not in STATIC_FIELDS]
        self.train_rate = train_rate
        self.normalize()
        self.dimension_values = {}
        self.train_set, self.test_set = self.split_train_test()
        self.base_corr = 0
        self.base_value = 0

    def split_train_test(self):
        df = self.data
        return df[df['gid'] < 5], df[df['gid'] >= 5]

    def normalize(self):
        df = self.data
        df['pay_amount'].fillna(0, inplace=True)
        df['reg_count'] = 1
        df['gid'] = df['member_id'] % 10
        df['paid'] = df['pay_amount'].apply(lambda x: x > 0 and 1 or 0)
        for d in self.dimensions:
            df[d] = df[d].astype(object)

    def cal_reg_pament(self, df):
        return (df['pay_amount'] / df['reg_count']).agg('average')

    def cal_corr(self, df):
        return df.corr().iloc[0, 1]

    def train(self):
        df = self.train_set
        dimensions = self.dimensions
        m = self.dimension_values
        gsum = df[['gid', 'reg_count', 'pay_amount']].groupby('gid').sum()
        self.base_corr = self.cal_corr(gsum)
        if self.base_corr < 0:
            self.base_corr = 0
        self.base_value = self.cal_reg_pament(gsum)
        for d in dimensions:
            r = df[[d, 'gid', 'reg_count', 'pay_amount', 'paid']].groupby([d, 'gid']).sum()
            for a in r.index.levels[0]:
                b = r.loc[a]
                corr = self.cal_corr(b)
                if corr <= 0 or np.isnan(corr):
                    continue
                m["%s:%s" % (d, a)] = dict(
                    reg_payment=self.cal_reg_pament(b),
                    corr=corr,
                    groups=len(b),
                    reg_count=b['reg_count'].sum(),
                    pay_count=b['paid'].sum()
                )
                # print d, a
        return m

    def predict_object(self, obj):
        tc = self.base_corr
        a = 0
        facts = []
        fs = [('base', self.base_value, self.base_corr)]
        for d in self.dimensions:
            k = '%s:%s' % (d, obj[d])
            vs = self.dimension_values.get(k)
            if vs:
                corr = vs.get('corr')
                val = vs.get('reg_payment')
                fs.append((k, val, corr))
                tc += corr
        if tc == 0:
            tc = 1
            fs = [('base', self.base_value, 1)]
        for d, v, c in fs:
            w = c / tc
            f = v * w
            a += f
            facts.append("%s %.2f*%.2f=%.2f" % (d, v, w, f))
        return a, obj.member_id, ' | '.join(facts)

    def predict(self, df):
        return pd.DataFrame([(row.gid, self.predict_object(row)[0], row.pay_amount) for index, row in df.iterrows()],
                            columns=['gid', 'predict', 'actual'])

    def score(self, result):
        d1 = result.sum()
        d2 = result.groupby('gid').sum()
        return d1['predict'] / d1['actual'], d2['predict'] / d2['actual']

    def fit(self):
        self.train()
        print 'train:', self.score(self.predict(self.train_set))
        print 'test:', self.score(self.predict(self.test_set))

    def sample(self, size=10):
        ds = [self.predict_object(row) for index, row in self.test_set.iterrows()]
        ds.sort(reverse=True)
        l = len(ds)

        def output(start):
            print "\n##############", start, "###########\n"
            for p, id, s in ds[start:start + size]:
                print "%.2f" % p, id, s

        output(0)
        output(l / 2)
        output(l - size)


def tree_fit(data, rate=2, exclude=[]):
    a = len(data) / 2
    dt = data  # data[dims]
    for d in exclude:
        dt = dt.drop(d, 1)
    dt = dt.fillna(0)
    cats = {}
    for d in dt.columns:
        if dt[d].dtype == 'object':
            cc = pd.Categorical(dt[d])
            cats[d] = cc.categories
            dt[d] = cc.codes
    train = dt[dt[u'资源编号'] % rate != 0]
    test = dt[dt[u'资源编号'] % rate == 0]
    Y = train[u'成单金额'].fillna(0)
    YT = test[u'成单金额'].fillna(0)
    X = train
    X = X.drop(u'资源编号', 1).drop(u'成单金额', 1)
    test = test.drop(u'资源编号', 1).drop(u'成单金额', 1)
    mode = tree.DecisionTreeRegressor()
    mode.fit(X, Y)
    r = mode.predict(test)
    return r, YT, test, cats


def csv_correlation(fname):
    return pd.read_csv(fname).corr().iloc[0, 1]
