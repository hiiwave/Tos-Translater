from pathlib import Path
import pandas as pd
import numpy as np
from . import TSVS


class Exporter():
    def __init__(self, output_path: Path):
        self.output_path = output_path
        if not output_path.exists():
            output_path.mkdir()

    def set_tables(self, tables: pd.DataFrame, df_ens, df_tws):
        self.tables = tables
        self.df_ens = df_ens
        self.df_tws = df_tws

    def export(self):
        pass


class ExporterEnTw(Exporter):
    def export(self):
        dfs = {}
        for tsv in TSVS:
            df1 = self.df_ens[tsv]
            dfm = self.tables[tsv]
            df = pd.merge(df1, dfm, on='korean', how='left')
            df['name'] = np.where(
                df['name_y'].isna(), df['name_x'], df['name_y'])
            df = df[['no', 'name']]
            path = self.output_path / tsv
            df.to_csv(path, sep='\t', index=False, header=False)
            print("Saved " + str(path))
            dfs[tsv] = df
        return dfs


def ExporterFactory(langfrom, langto, output_path):
    if langfrom == 'en' and langto == 'tw':
        return ExporterEnTw(output_path / 'itos-tw')
    elif langfrom == 'tw' and langto == 'en':
        return ExporterEnTw(output_path / 'itos-tw')
        # return ExporterTwEn(output_path / 'twtos-en')
    else:
        raise TypeError("Language Not support")
