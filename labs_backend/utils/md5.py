from config import HASH_MD_BUFFER,HASH_SIN_TABLE,HASH_CYCLIC_SHIFT


def bits_padding(input_bytes):
    original_len = len(input_bytes) * 8
    padded = bytearray(input_bytes)
    padded.append(0x80)
    while len(padded) % 64 != 56:
        padded.append(0x00)

    length_bytes = original_len.to_bytes(8, byteorder='little')
    for byte in length_bytes:
        padded.append(byte)

    words = []
    for i in range(0, len(padded), 4):
        word = int.from_bytes(padded[i:i + 4], byteorder='little')
        words.append(word)

    return words



def f(b,c,d,i):
    if i<16:
        return (b&c) | ((~b) & d)
    elif i<32:
        return (d&b) | ((~d) & c)
    elif i<48:
        return b^c^d
    else:
        return c ^ (b|(~d))

def left_rotation(x,r):
    return ( (x<<r) | (x>>(32-r))) % (2**32)

def cls(a,f,inp_v,i):
    K = HASH_SIN_TABLE

    R = HASH_CYCLIC_SHIFT
    sum_k = (a+f+inp_v+K[i]) % (2**32)
    return left_rotation( sum_k, R[i]) % (2**32)

def find_idx(i):
    if i < 16:
        return i
    elif i < 32:
        return (5*i+1) % 16
    elif i < 48:
        return (3*i+5) % 16
    else:
        return (7*i) % 16


def md5(inp):
    A,B,C,D = HASH_MD_BUFFER
    for j in range(0, len(inp), 16):
        block = inp[j:j + 16]
        a, b, c, d = A, B, C, D
        for i in range(64):
            a_1, c_1, d_1 = d,b,c
            idx = find_idx(i)
            b_1 = (cls(a,f(b,c,d,i),block[idx],i)+b) %2**32
            a, b, c, d =a_1,b_1,c_1, d_1

        A= (A+a)%2**32
        B= (B+b)%2**32
        C= (C+c)%2**32
        D= (D+d)%2**32
    result = (A.to_bytes(4, byteorder='little') +
              B.to_bytes(4, byteorder='little') +
              C.to_bytes(4, byteorder='little') +
              D.to_bytes(4, byteorder='little'))
    return result.hex()


def start_hashing(input_val):
    if isinstance(input_val, str):
        input_bytes = input_val.encode('utf-8')
    else:
        input_bytes = input_val
    words = bits_padding(input_bytes)
    return md5(words)

def compare_hash(hashed_val, control_val):
    return hashed_val==control_val


