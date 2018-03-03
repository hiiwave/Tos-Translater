from .exporter import *


class ExporterTwDualBase(Exporter):
    def _get_df1(self, tsv):
        return self.df_tws[tsv]

    def _get_dual_condition(self, df):
        cond_short = df.tw.str.len() < 15
        cond_short &= df.en.str.len() < 35
        special_chars = [',', '.', '!', ':', '%', '{', '}']
        cond_nospecialchars = functools.reduce(
            lambda x, y: x & y, [df.en.str.find(c) == -1 for c in special_chars])
        return cond_short & cond_nospecialchars

    def _make_df_result(self, df, tsv):
        if tsv in ['UI.tsv'] or tsv[:5] == 'QUEST':
            return self._make_df_initial(df)
        else:
            cond = self._get_dual_condition(df)
            res = self._make_df_initial(df).copy()
            res[cond] = self._make_df_dual(df)
            return res

    def _custom_modify_result(self, df):
        mymap = {
            'Normal': '一般',
            'Party': '組隊',
            'Whisper': '密語',
            'Guild': '公會',
            'Shout': '呼喊',
            'Groups': '群組'
        }
        rows = df['en'].isin(mymap.keys())
        df['result'][rows] = df['en'][rows].apply(lambda x: mymap[x])

    @abstractmethod
    def _make_df_initial(self, df):
        pass

    @abstractmethod
    def _make_df_dual(self, df):
        pass


class ExporterTwDual1(ExporterTwDualBase):
    def _make_df_initial(self, df):
        return df['tw']

    def _make_df_dual(self, df):
        return np.where(~df['en'].isna(), df.tw + ' (' + df.en + ')', df['tw'])


class ExporterTwDual2(ExporterTwDualBase):
    def _make_df_initial(self, df):
        return df['en']

    def _make_df_dual(self, df):
        res = pd.Series(np.where(~df['tw'].isna(), df.en + ' (' + df.tw + ')', df['en']))
        return res