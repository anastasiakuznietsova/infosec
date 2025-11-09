from config import WORD_LENGTH_RC5, ROUNDS_AMOUNT_RC5, KEY_LENGTH_RC5, MASK_RC5, P_RC5, Q_RC5, TO_BYTES_LENGTH_RC5

def nrm_bit_add(val):
    return val & MASK_RC5

def left_bit_rotation(x, rotate_by, w):
    rotate_by %= w
    return nrm_bit_add((x << rotate_by) | (x >> (w - rotate_by)))
def right_bit_rotation(x,rotate_by, w):
    rotate_by %= w
    return nrm_bit_add((x >> rotate_by) | (x << (w - rotate_by)))

def pad(bytes_line, w):
    bb = int(2 * w / 8)
    padding_len=bb-(len(bytes_line)%bb)
    padding = bytes([padding_len]) * padding_len
    return bytes_line+padding

def un_pad(padded):
    pad_len = padded[-1]
    return padded[:-pad_len]

def get_s(hex_key_string, w, key_len, r):
    k = bytes.fromhex(hex_key_string)

    p = P_RC5
    q = Q_RC5

    u = int(w / 8)
    c = int(key_len / u)

    l = [0] * c
    for i in range(0, c):
        l[i] = sum(2 ** (8 * j) * k[i * u + j] for j in range(u))
    s = [p] * (2 * r + 2)
    for i in range(1, 2 * r + 2):
        s[i] = nrm_bit_add(s[i - 1] + q)

    i, j = 0, 0
    a_1,b_1 = 0, 0
    t = max(c, 2 * r + 2)
    for _ in range(1, 3 * t):
        s[i] = left_bit_rotation(nrm_bit_add(s[i] + a_1 + b_1), 3, w)
        a_1 = s[i]
        i = (i + 1) % (2 * r + 2)

        l[j] = left_bit_rotation(nrm_bit_add(l[j] + a_1 + b_1), nrm_bit_add(a_1 + b_1), w)
        b_1 = l[j]
        j = (j + 1) % c
    return s

def rc5(b_bytes, s, w,r):
    a = (int.from_bytes(b_bytes[:TO_BYTES_LENGTH_RC5], byteorder='little'))
    b = (int.from_bytes(b_bytes[TO_BYTES_LENGTH_RC5:], byteorder='little'))

    a = nrm_bit_add(a + s[0])
    b = nrm_bit_add(b + s[1])

    for i in range(1, r + 1):
        a = nrm_bit_add(left_bit_rotation(a ^ b, b, w) + s[2 * i])
        b = nrm_bit_add(left_bit_rotation(b ^ a, a, w) + s[2 * i + 1])

    bytes_a = a.to_bytes(TO_BYTES_LENGTH_RC5, byteorder='little')
    bytes_b = b.to_bytes(TO_BYTES_LENGTH_RC5, byteorder='little')
    return bytes_a + bytes_b
def cbc(padded_bytes, iv, s, w,r):
    bb = int(2 * w / 8)
    c=b''
    c_prev = iv

    for i in range(0, len(padded_bytes), bb):
        plaintext_block = padded_bytes[i : i + bb]
        p_int = int.from_bytes(plaintext_block, 'little')
        c_prev_int = int.from_bytes(c_prev, 'little')

        xor_int = p_int ^ c_prev_int
        xor_bytes = xor_int.to_bytes(bb, 'little')

        new_c = rc5(xor_bytes, s, w,r)
        c += new_c
        c_prev = new_c
    return c

def rc5_decrypt(b_bytes, s, r,w):
    a = int.from_bytes(b_bytes[:TO_BYTES_LENGTH_RC5], 'little')
    b = int.from_bytes(b_bytes[TO_BYTES_LENGTH_RC5:], 'little')
    for i in range(r, 0, -1):
        b = right_bit_rotation(nrm_bit_add(b - s[2 * i + 1]), a, w) ^ a
        a = right_bit_rotation(nrm_bit_add(a - s[2 * i]), b, w) ^ b

    b = nrm_bit_add(b - s[1])
    a = nrm_bit_add(a - s[0])

    return a.to_bytes(TO_BYTES_LENGTH_RC5, 'little') + b.to_bytes(TO_BYTES_LENGTH_RC5, 'little')

def cbc_decrypt(c, iv, s, r, w):
    bb=int(2 * w / 8)
    plaintext = b''
    prev = iv
    for i in range(0, len(c), bb):
        block = c[i:i + bb]
        decrypted = rc5_decrypt(block, s, r,w)
        p_block = bytes(a ^ b for a, b in zip(decrypted, prev))
        plaintext += p_block
        prev = block
    return un_pad(plaintext)

def get_encoded_value(hex_key_string, rand_num, bytes_line):
    w = WORD_LENGTH_RC5
    r = ROUNDS_AMOUNT_RC5
    key_len = KEY_LENGTH_RC5
    bb = int(2 * w / 8)

    s = get_s(hex_key_string, w, key_len, r)
    iv = rc5(rand_num.to_bytes(bb, byteorder='little'), s, w,r)
    return cbc(pad(bytes_line, w), iv, s, w,r), iv

def get_decoded_value(hex_key_string, iv, encrypted_line):
    w = WORD_LENGTH_RC5
    r = ROUNDS_AMOUNT_RC5
    key_len = KEY_LENGTH_RC5

    s = get_s(hex_key_string, w, key_len, r)
    return cbc_decrypt(encrypted_line, iv, s, r, w)