from pathlib import Path
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from . import TSVS


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

    @abstractmethod
    def _prepare_df_tsv(self, tsv):
        pass


class ExporterEnTw(Exporter):
    def _prepare_df_tsv(self, tsv):
        df1 = self.df_ens[tsv]
        dfm = self.tables[tsv]
        df = pd.merge(df1, dfm, on='korean', how='left')
        df['name'] = np.where(df['tw'].isna(), df['en'], df['tw'])
        df = df[['no', 'name']]
        return df


class ExporterTwEn(Exporter):
    def _prepare_df_tsv(self, tsv):
        df1 = self.df_tws[tsv]
        dfm = self.tables[tsv]
        df = pd.merge(df1, dfm, on='korean', how='left')
        df['name'] = np.where(df['en'].isna(), df['tw'], df['en'])
        df = df[['no', 'name']]
        return df


class ExporterTwDual1(Exporter):
    def _get_dual_condition(self, df):
        cond_short = df.tw.str.len() < 10
        cond_nocomma = df.tw.str.find('，') == -1
        cond_nosentence = df.tw.str.find('。') == -1
        return cond_short & cond_nocomma & cond_nosentence

    def _add_dual(self, df):
        cond = self._get_dual_condition(df)
        df['dual'] = df.tw
        df['dual'][cond] = np.where(
            ~df['en'].isna(), df.tw + r'\n(' + df.en + ')', df['tw'])

    def _prepare_df_tsv(self, tsv):
        df1 = self.df_tws[tsv]
        if tsv in ['UI.tsv'] or tsv[:5] == 'QUEST':
            return df1[['no', 'name']]
        dfm = self.tables[tsv]
        df = pd.merge(df1, dfm, on='korean', how='left')
        self._add_dual(df)
        df = df[['no', 'dual']]
        return df


class ExporterTwEn(Exporter):
    def export(self):
        dfs = {}
        for tsv in TSVS:
            df1 = self.df_tws[tsv]
            dfm = self.tables[tsv]
            df = pd.merge(df1, dfm, on='korean', how='left')
            df['name'] = np.where(
                df['name_x'].isna(), df['name_y'], df['name_x'])
            df = df[['no', 'name']]
            path = self.output_path / tsv
            df.to_csv(path, sep='\t', index=False, header=False)
            print("Saved " + str(path))
            dfs[tsv] = df
        return dfs

def ExporterFactory(langfrom, langto, output_path):
    if (langfrom, langto) == ('en', 'tw'):
        return ExporterEnTw(output_path / 'itos-tw')
    elif (langfrom, langto) == ('tw', 'en'):
        return ExporterTwEn(output_path / 'twtos-en')
    elif (langfrom, langto) == ('tw', 'dual1'):
        return ExporterTwDual1(output_path / 'twtos-dual1')
    else:
        raise TypeError("Language Not support")
