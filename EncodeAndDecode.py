import numpy as np

def encode_message(message, G):
    codeword = np.dot(message, G) % 2
    return codeword
