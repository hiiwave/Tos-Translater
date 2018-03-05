from .exporter import Exporter
import functools
import numpy as np
import pandas as pd


class ExporterTwFull(Exporter):
    ''' Similar to ExporterTwEn but remaining zh-tw and korean
    '''
    def _get_df1(self, tsv):
        return self.df_tws[tsv]

    def _make_df_result(self, df, tsv):
        return np.where(~df['en'].isna(), df['en'], df['tw'])

    # Overwrite
    def _prepare_df_tsv(self, tsv):
        ''' Prepare the dataframe of tsv
        '''
        df1 = self._get_df1(tsv)
        dfm = self.tables[tsv]
        df = pd.merge(df1, dfm, on='korean', how='left')
        df['result'] = self._make_df_result(df, tsv)
        self._custom_modify_result(df)
        df = df[['no', 'tw', 'en', 'korean']]
        return df


class ExporterLanguageMap(ExporterTwFull):
    ''' Export language mapping tables
    '''
    def _prepare_df_tsv(self, tsv):
        df = super()._prepare_df_tsv(tsv)
        cond = self._get_nospecialchars_condition(df)
        df = df[cond]
        df = df[['tw', 'en', 'korean']]
        return df

    def _get_nospecialchars_condition(self, df):
        cond_short = df.tw.str.len() < 15
        cond_short &= df.en.str.len() < 35
        special_chars = [',', '.', '!', ':', '%', '{', '}']
        cond_nospecialchars = functools.reduce(
            lambda x, y: x & y, [df.en.str.find(c) == -1 for c in special_chars])
        return cond_nospecialchars
