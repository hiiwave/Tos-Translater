from tos_languagematcher import Matcher
from pathlib import Path


lang_en_path = Path('data/lang-en')
lang_tw_path = Path('data/lang-tw')
output_path = Path('output/')


matcher = Matcher(lang_en_path, lang_tw_path)
# matcher.export('en', 'tw', output_path / 'itos-tw')
# matcher.export('tw', 'en-opt', output_path / 'twtos-en')
matcher.export('tw', 'en-opt', Path(r'C:\TreeOfSaviorTW\release\languageData\twtos-en'))
# matcher.export('tw', 'dual1', output_path / 'twtos-dual1')
# matcher.export('tw', 'dual2', output_path / 'twtos-dual2')
# matcher.export('tw', 'dual1', Path(r'C:\TreeOfSaviorTW\release\languageData\twtos-dual1'))
# matcher.export('tw', 'dual2', Path(r'C:\TreeOfSaviorTW\release\languageData\twtos-dual2'))