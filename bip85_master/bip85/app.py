from bip85 import BIP85

LANGUAGE_LOOKUP = {
    'english': 0,
    'japanese': 1,
    'korean': 2,
    'spanish': 3,
    'chinese_simplified': 4,
    'chinese_traditional': 5,
    'french': 6,
    'italian': 7,
    'czech': 8
}

def bip39(xprv_string, language, words, index):
    # 83696968'/39'/language'/words'/index'
    lang_code = LANGUAGE_LOOKUP[language]
    bip85 = BIP85()
    path = f"83696968p/39p/{lang_code}p/{words}p/{index}p"

    entropy = bip85.bip32_xprv_to_entropy(path, xprv_string)
    return bip85.entropy_to_bip39(entropy, words, language)


def wif(xprv_string, index):
    # m/83696968'/2'/index'
    bip85 = BIP85()
    path = f"83696968p/2p/{index}p"
    return bip85.entropy_to_wif(bip85.bip32_xprv_to_entropy(path, xprv_string))


def hex(xprv_string, index, width):
    # m/83696968'/128169p'/index'
    bip85 = BIP85()
    path = f"83696968p/128169p/{width}p/{index}p"
    return bip85.bip32_xprv_to_hex(path, width, xprv_string)


def xprv(xprv_string, index):
    # 83696968'/32'/index'
    bip85 = BIP85()
    path = f"83696968p/32p/{index}p"
    return bip85.bip32_xprv_to_xprv(path, xprv_string)
