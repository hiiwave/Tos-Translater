from tos_languagematcher import Matcher
from pathlib import Path


lang_en_path = Path('data/lang-en')
lang_tw_path = Path('data/lang-tw')
# lang_entw_path = Path('data/lang-en-tw-20180222')
output_path = Path('output/')


matcher = Matcher(lang_en_path, lang_tw_path)
matcher.export('en', 'tw', output_path)
matcher.export('tw', 'en', output_path)
# exporter.export('tw', 'tw-en')
