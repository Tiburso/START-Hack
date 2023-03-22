from bip32utils import BIP32Key
from bip85_master.bip85.app import bip39

# Generate xprv from mnemonic
""" Example Usage: 
    
    TEST_MNENONIC = "install scatter logic circle pencil average fall shoe quantum disease suspect usage"
    generate_mnemonic_from_seed(TEST_MNENONIC, 12, 0) 
    
    Returns -> "jelly zero knife tumble cliff original hawk submit cute raccoon present fringe"
    
"""
def generate_mnemonic_from_seed(mnemonic: str, num_words: int, index: int, language: str = 'english'):
    seed = BIP32Key.fromEntropy(mnemonic.encode('utf-8')).ExtendedKey()

    return bip39(seed, language, num_words, index)




