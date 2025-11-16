import zlib  # For CRC-32 calculation

def swap(S, i, j):
    S[i], S[j] = S[j], S[i]

def KSA(key):
    N = 256
    S = list(range(N))
    j = 0
    key_len = len(key)

    for i in range(N):
        j = (j + S[i] + key[i % key_len]) % N
        swap(S, i, j)

    return S

def PRGA(S, data):
    i = 0
    j = 0
    result = []


    

    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        swap(S, i, j)

        rnd = S[(S[i] + S[j]) % 256]
        result.append(rnd ^ byte)

    return result

def RC4(key, data):
    key = [ord(c) for c in key]
    S = KSA(key)
    result = PRGA(S, data)
    
    return result

# Custom checksum function
def calculate_custom_checksum(num1, num2):
    sum_result = num1 + num2
    if sum_result > 0xFFFFFFFF:
        sum_result = (sum_result & 0xFFFFFFFF) + (sum_result >> 32)
    checksum = ~sum_result & 0xFFFFFFFF
    return checksum

# Encrypt function with custom checksum
def encrypt_with_checksum(key, plaintext):
    # Generate two 32-bit numbers based on the plaintext
    num1 = int.from_bytes(plaintext.encode()[:4], byteorder='big') if len(plaintext) >= 4 else 0
    num2 = int.from_bytes(plaintext.encode()[4:8], byteorder='big') if len(plaintext) >= 8 else 0
    
    # Calculate checksum
    checksum = calculate_custom_checksum(num1, num2)
    checksum_bytes = checksum.to_bytes(4, byteorder='big')

    # Append checksum to the plaintext
    plaintext_with_checksum = plaintext.encode() + checksum_bytes

    # Encrypt the message + checksum using RC4
    encrypted_message = bytes(RC4(key, plaintext_with_checksum))

    return encrypted_message

# Decrypt function with custom checksum verification
def decrypt_with_checksum(key, encrypted_message):
    # Decrypt the message using RC4
    decrypted_message_with_checksum = bytes(RC4(key, list(encrypted_message)))

    # Separate the decrypted message and the checksum
    decrypted_message = decrypted_message_with_checksum[:-4].decode()
    received_checksum = int.from_bytes(decrypted_message_with_checksum[-4:], byteorder='big')

    # Generate two 32-bit numbers from the decrypted message
    num1 = int.from_bytes(decrypted_message.encode()[:4], byteorder='big') if len(decrypted_message) >= 4 else 0
    num2 = int.from_bytes(decrypted_message.encode()[4:8], byteorder='big') if len(decrypted_message) >= 8 else 0
    
    # Recalculate the checksum from the decrypted message
    calculated_checksum = calculate_custom_checksum(num1, num2)

    # Check if the checksum matches
    if received_checksum != calculated_checksum:
        raise ValueError("Integrity Check Failed: Checksum mismatch!")

    return decrypted_message
