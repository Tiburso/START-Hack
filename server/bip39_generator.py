from bip32utils import BIP32Key
from bip85_master.bip85.app import bip39

from config import HGS_KEY_PHRASE

# Generate xprv from mnemonic
""" Example Usage: 
    
    TEST_MNENONIC = "install scatter logic circle pencil average fall shoe quantum disease suspect usage"
    generate_mnemonic_from_seed(TEST_MNENONIC, 12, 0) 
    
    Returns -> "jelly zero knife tumble cliff original hawk submit cute raccoon present fringe"
    
"""

def generate_mnemonic_from_seed(index: int, mnemonic: str = HGS_KEY_PHRASE, language: str = 'english'):
    seed = BIP32Key.fromEntropy(mnemonic.encode('utf-8')).ExtendedKey()

    num_words = len(mnemonic.split(' '))

    return bip39(seed, language, num_words, index)