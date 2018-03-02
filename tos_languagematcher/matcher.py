import pandas as pd
from pathlib import Path
from .exporter import ExporterFactory
from . import TSVS


class Matcher():
    def __init__(self, lang_en_path: Path, lang_tw_path: Path):
        self.tables = {}
        self.df_ens = {}
        self.df_tws = {}
        self.en_path = lang_en_path
        self.tw_path = lang_tw_path
        self.matchall()

    def readtsv(self, filepath, filename):
        def _change_encoding(df):
            for col in ['korean', 'name']:
                df[col] = df[col].str.encode('latin1')
                df[col] = df[col].str.decode('utf-8', errors='ignore')
            return df

        import csv
        df = pd.read_csv(filepath / filename, sep='\t',
                         names=['no', 'name', 'korean'],
                         usecols=[0, 1, 2],
                         encoding='latin1',
                         # engine='python',
                         quoting=csv.QUOTE_NONE,
                         error_bad_lines=False)
        df = _change_encoding(df)
        return df.iloc[:, :3]

    def matchall(self):
        for tsv in TSVS:
            self.tables[tsv] = self.match(tsv)

    def match(self, tsv):
        '''
            Match two table by korean

            Returns:
                Merged dataframe with df['en'] and df['tw'] available
        '''
        print("Matching.. " + tsv)
        df1 = self.readtsv(self.en_path, tsv)
        df2 = self.readtsv(self.tw_path, tsv)
        self.df_ens[tsv] = df1
        self.df_tws[tsv] = df2
        df = pd.merge(df1, df2, on='korean', how='outer')
        df = df.rename({'name_x': 'en', 'name_y': 'tw'}, axis='columns')
        return df

    def export(self, langfrom, langto, output_path):
        exporter = ExporterFactory(langfrom, langto, output_path)
        exporter.set_tables(self.tables, self.df_ens, self.df_tws)
        exporter.export()
