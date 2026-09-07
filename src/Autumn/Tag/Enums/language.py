import enum


class Language(enum.Enum):
    """
    A class holding many of the languages spoken worldwide.
    """
    ABKHAZIAN = "ab"
    AFAR = "aa"
    AFRIKAANS = "af"
    AKAN = "ak"
    ALBANIAN = "sq"
    AMHARIC = "am"
    ARABIC = "ar"
    ARAGONESE = "an"
    ARMENIAN = "hy"
    ASSAMESE = "as"
    AVARIC = "av"
    AVESTAN = "ae"
    AYMARA = "ay"
    AZERBAIJANI = "az"
    BAMBARA = "bm"
    BASHKIR = "ba"
    BASQUE = "eu"
    BELARUSIAN = "be"
    BENGALI = "bn"
    BISLAMA = "bi"
    BOSNIAN = "bs"
    BRETON = "br"
    BULGARIAN = "bg"
    BURMESE = "my"
    CATALAN = "ca"
    CHAMORRO = "ch"
    CHECHEN = "ce"
    CHICHEWA = "ny"
    CHINESE = "zh"
    CHURCH_SLAVONIC = "cu"
    CHUVASH = "cv"
    CORNISH = "kw"
    CORSICAN = "co"
    CREE = "cr"
    CROATIAN = "hr"
    CZECH = "cs"
    DANISH = "da"
    DIVEHI = "dv"
    DUTCH = "nl"
    DZONGKHA = "dz"
    ENGLISH = "en"
    ESPERANTO = "eo"
    ESTONIAN = "et"
    EWE = "ee"
    FAROESE = "fo"
    FIJIAN = "fj"
    FINNISH = "fi" # Finish?
    FRENCH = "fr"
    WESTERN_FRISIAN = "fy"
    FULAH = "ff"
    SCOTTISH_GAELIC = "gd"
    GALICIAN = "gl"
    GANDA = "lg"
    GEORGIAN = "ka"
    GERMAN = "de"
    GREEK = "el"
    KALAALLISUT = "kl"
    GUARANI = "gn"
    GUJARATI = "gu"
    HAITIAN_CREOLE = "ht"
    HAUSA = "ha"
    HEBREW = "he"
    HERERO = "hz"
    HINDI = "hi"
    HIRI_MOTU = "ho"
    HUNGARIAN = "hu"
    ICELANDIC = "is"
    IDO = "io"
    IGBO = "ig"
    INDONESIAN = "id"
    INTERLINGUA = "ia"
    INTERLINGUE = "ie"
    INUKTITUT = "iu"
    INUPIAQ = "ik"
    IRISH = "ga"
    ITALIAN = "it"
    JAPANESE = "ja"
    JAVANESE = "jv"
    KANNADA = "kn"
    KANURI = "kr"
    KASHMIRI = "ks"
    KAZAKH = "kk"
    CENTRAL_KHMER = "km"
    KIKUYU = "ki"
    KINYARWANDA = "rw"
    KIRGHIZ = "ky"
    KOMI = "kv"
    KONG = "kg"
    KOREAN = "ko"
    KUANYAMA = "kj"
    KURDISH = "ku"
    LAO = "lo"
    LATIN = "la"
    LATVIAN = "lv"
    LIMBURGAN = "li"
    LINGALA = "ln"
    LITHUANIAN = "lt"
    LUBA_KATANGA = "lu"
    LUXEMBOURGISH = "lb"
    MACEDONIAN = "mk"
    MALAGASY = "mg"
    MALAYALAM = "ml"
    MALTESE = "mt"
    MANX = "gv"

    # -------------------------------------

    # English
    ENGLISH_US = "en-US"
    ENGLISH_UK = "en-UK"
    ENGLISH_AUSTRALIA = "en-AU"
    ENGLISH_CANADA = "en-CA"
    ENGLISH_INDIA = "en-IN"
    ENGLISH_NZ = "en-NZ"
    ENGLISH_SA = "en-ZA"
    ENGLISH_IRELAND = "en-IE"
    ENGLISH_PHILIPPINES = "en-PH"
    ENGLISH_SINGAPORE = "en-SG"

    # Spanish

    SPANISH_SPAIN = "es-ES"
    SPANISH_MEXICO = "es-MX"
    SPANISH_ARGENTINA = "es-AR"
    SPANISH_COLOMBIA = "es-CO"
    SPANISH_CHILE = "es-CL"
    SPANISH_PERU = "es-PE"
    SPANISH_VENEZUELA = "es-VE"
    SPANISH_CUBA = "es-CU"
    SPANISH_DR = "es-DO"
    SPANISH_US = "es-US"

    # French

    FRENCH_FRANCE = "fr-FR"
    FRENCH_CANADA = "fr-CA"
    FRENCH_BELGIUM = "fr-BE"
    FRENCH_SWITZERLAND = "fr-CH"
    FRENCH_LUXEMBOURG = "fr-LU"
    FRENCH_MONACO = "fr-MC"

    # Portuguese

    PORTUGUESE_PORTUGAL = "pt-PT"
    PORTUGUESE_BRAZIL = "pt-BR"
    PORTUGUESE_ANGOLA = "pt-AO"
    PORTUGUESE_MOZAMBIQUE = "pt-MZ"

    # German

    GERMAN_GERMANY = "de-DE"
    GERMAN_AUSTRIA = "de-AT"
    GERMAN_SWITZERLAND = "de_CH"
    GERMAN_LIECHTENSTEIN = "de-LI"
    GERMAN_BELGIUM = "de-BE"

    # Dutch

    DUTCH_NETHERLANDS = "nl-NL"
    DUTCH_BELGIUM = "nl-BE"

    # Chinese

    CHINESE_SIMPLIFIED = "zh-Hans"
    CHINESE_TRADITIONAL = "zh-Hant"
    CHINESE_MAINLAND = "zh-CN"
    CHINESE_TAIWAN = "zh-TW"
    CHINESE_HK = "zh-HK"
    CHINESE_SINGAPORE = "zh-SG"
    CHINESE_MACAU = "zh-MO"

    # Arabic

    ARABIC_SAUDI ="ar-SA"
    ARABIC_EGYPT = "ar-EG"
    ARABIC_ALGERIA = "ar-DZ"
    ARABIC_MOROCCO = "ar-MA"
    ARABIC_IRAQ = "ar-IQ"
    ARABIC_SYRIA = "ar-SY"
    ARABIC_JORDAN = "ar-JO"
    ARABIC_LEBANON = "ar-LB"
    ARABIC_KUWAIT = "ar-KW"
    ARABIC_UAE = "ar-AE"
    ARABIC_YEMEN = "ar-YE"
    ARABIC_PALESTINE = "ar-PS"

    # Serbian

    SERBIAN_CYRILLIC = "sr-Cyrl"
    SERBIAN_LATIN = "sr-Latn"
    SERBIAN_SERBIA = "sr-SR"
    SERBIAN_BOSNIA = "sr-BA"

    # Croatian

    AFRIKAANS_SOUTH_AFRICA = "af-ZA"
    AFRIKAANS_NAMIBIA = "af-NA"

    # Norwegian

    NORWEGIAN_BOKMAL = "nb-NO"
    NORWEGIAN_NYNORSK = "nn-NO"

    # Swedish

    SWEDISH_SWEDEN = "sv-SE"
    SWEDISH_FINLAND = "sv-FI"

    # Russian

    RUSSIAN_RUSSIA = "ru-RU"
    RUSSIAN_BELARUS = "ru-BY"
    RUSSIAN_KAZAKHSTAN = "ru-KZ"
    RUSSIAN_UKRAINE = "ru-UA"


    # Persian

    PERSIAN_IRAN = "fa-IR"
    PERSIAN_AFGHANISTAN = "fa-AF"

    # Urdu

    URDU_PAKISTAN = "ur-PK"
    URDU_INDIA = "ur-IN"

    # Punjabi

    PUNJABI_GURMUKHI = "pa-Guru"
    PUNJABI_SHAHMUKHI = "pa-Arab"

    # Bengali

    BENGALI_BANGLADESH = "bn-BD"
    BENGALI_INDIA = "bn-IN"

    # Kurdish

    KURDISH_LATIN = "ku-Latn"
    KURDISH_ARABIC = "ku-Arab"

    # Azerbaijani

    AZERBAIJANI_LATIN = "az-Latn"
    AZERBAIJANI_CYRILLIC = "az-Cyrl"

    # Uzbek

    UZBEK_LATIN = "uz-Latn"
    UZBEK_CYRILLIC = "uz-Cyrl"

    # Kazakh

    KAZAKH_CYRILLIC = "ka-Cyrl"
    KAZAKH_LATIN = "ka-Latn"

    # Mongolian

    MONGOLIAN_CYRILLIC = "mon-Cyrl"
    MONGOLIAN_MONGOL ="mon-Mong"

    # Tamil

    TAMIL_INDIA = "ta-IN"
    TAMIL_SRI_LANKA = "ta-LK"
    TAMIL_SINGAPORE = "ta-SG"

    # Malay

    MALAY_MALAYSIA = "ms-MY"
    MALAY_BRUNEI = "ms-BN"
    MALAY_SINGAPORE = "ms-SG"

    # Swahili

    SWAHILI_KENYA = "sw-KE"
    SWAHILI_TANZANIA = "sw-TZ"
    SWAHILI_UGANDA = "sw-UG"

    # Greek

    GREEK_GREECE = "el-GR"
    GREEK_CYPRUS = "el-CY"

    # Yiddish

    YIDDISH_HEBREW = "yi-Hebr"
    YIDDISH_LATIN = "yi-Latn"