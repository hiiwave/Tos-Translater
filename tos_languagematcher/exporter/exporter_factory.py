from .exporter import ExporterEnTw, ExporterTwEn, ExporterTwEnopt
from .exporter_dual import ExporterTwDual1, ExporterTwDual2
from .exporter_full import ExporterTwFull, ExporterLanguageMap


def ExporterFactory(langfrom, langto, output_path):
    if (langfrom, langto) == ('en', 'tw'):
        return ExporterEnTw(output_path)
    elif (langfrom, langto) == ('tw', 'en'):
        return ExporterTwEn(output_path)
    elif (langfrom, langto) == ('tw', 'en-opt'):
        return ExporterTwEnopt(output_path)
    elif (langfrom, langto) == ('tw', 'dual1'):
        return ExporterTwDual1(output_path)
    elif (langfrom, langto) == ('tw', 'dual2'):
        return ExporterTwDual2(output_path)
    elif (langfrom, langto) == ('tw', 'full'):
        return ExporterTwFull(output_path)
    elif (langfrom, langto) == ('tw', 'map'):
        return ExporterLanguageMap(output_path)
    else:
        raise TypeError("Language Not support")
