from pathlib import Path
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
import functools
from tos_languagematcher import TSVS


class Exporter(ABC):
    def __init__(self, output_path: Path):
        self.output_path = output_path
        if not output_path.exists():
            output_path.mkdir()

    def set_tables(self, tables: pd.DataFrame, df_ens, df_tws):
        self.tables = tables
        self.df_ens = df_ens
        self.df_tws = df_tws

    def export(self):
        dfs = self._prepare_dfs()
        self._to_tsvs(dfs)

    def _to_tsvs(self, dfs):
        for tsv, df in dfs.items():
            path = self.output_path / tsv
            df.to_csv(path, sep='\t', index=False, header=False)
            print("Saved " + str(path))

    def _prepare_dfs(self):
        dfs = {}
        for tsv in TSVS:
            dfs[tsv] = self._prepare_df_tsv(tsv)
        return dfs

    def _prepare_df_tsv(self, tsv):
        ''' Prepare the dataframe of tsv
        '''
        df1 = self._get_df1(tsv)
        dfm = self.tables[tsv]
        df = pd.merge(df1, dfm, on='korean', how='left')
        df['result'] = self._make_df_result(df, tsv)
        self._custom_modify_result(df)
        df = df[['no', 'result']]
        return df

    def _custom_modify_result(self, df):
        pass

    @abstractmethod
    def _get_df1(self, tsv):
        pass

    @abstractmethod
    def _make_df_result(self, df, tsv):
        pass


class ExporterEnTw(Exporter):
    def _get_df1(self, tsv):
        return self.df_ens[tsv]
    
    def _make_df_result(self, df, tsv):
        return np.where(~df['tw'].isna(), df['tw'], df['en'])


class ExporterTwEn(Exporter):
    def _get_df1(self, tsv):
        return self.df_tws[tsv]
    
    def _make_df_result(self, df, tsv):
        return np.where(~df['en'].isna(), df['en'], df['tw'])


class ExporterTwEnopt(ExporterTwEn):
    ''' Add some UI optimization for ExporterTwEn
    '''
    def _custom_modify_result(self, df):
        mymap = {
            'Normal': '一般',
            'Party': '組隊',
            'Whisper': '密語',
            'Guild': '公會',
            'Shout': '大喊',
            'Groups': '群組'
        }
        df['result'] = df['result'].apply(lambda x: mymap[x] if x in mymap else x)
