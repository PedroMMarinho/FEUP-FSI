import random

# Algoritmo de Miller-Rabin
def miller_rabin(n, k=40):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Encontrar primo próximo
def find_prime_near(n, offset, range_limit=1000000000):
    t = 500 + offset
    p_guess = 2 ** t
    
    for dp in range(0, range_limit):
        p = p_guess + dp
        if miller_rabin(p):
            q = n // p
            if n % p == 0 and miller_rabin(q):
                return p, q
    raise ValueError("Primes not found in range.")

# Algoritmo estendido de Euclides
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

# Função para decifrar
def decrypt_rsa(ciphertext, e, n):
    t = 2
    g = 2
    offset = ((t-1)*10+g) // 2
    p, q = find_prime_near(n,offset)

    phi = (p - 1) * (q - 1)
    _, d, _ = extended_gcd(e, phi)
    d = d % phi
    if d < 0:
        d += phi

    # Decifrar o texto
    int_ciphertext = int.from_bytes(ciphertext, "little")
    int_plaintext = pow(int_ciphertext, d, n)
    plaintext = int_plaintext.to_bytes((int_plaintext.bit_length() + 7) // 8, 'little')
    return plaintext

# Dados fornecidos
ciphertext_hex = "cd23cc233f7a5b9adb51e5616da489ab56c793d6fda7e4461c7780c3c060bced506b33a29ae9529baa157c8f8e4b4025b335fd930a26c9e387e9ce364be5ef8f9901ae9072e26cebb59ce0c682b49d3d1858bf15bfc886df6505e5a84ff541763b90c7a8a09ba863d499e994613dd1e44be0df788ee281455ecf06f936ee1e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
ciphertext = bytes.fromhex(ciphertext_hex)
e = 65537
n = 87777985100699018932094980018995348321190282174917313121792031815299158108154767154642811192581804697812555605405953787919330941803914366451585659492418224310284735827777424547738583851212264460897302213165924339933324276893486075954339784316175553712334493638957419692734948763763918793616499789655592951

# Decifrar
plaintext = decrypt_rsa(ciphertext, e, n)
print(plaintext.decode("utf-8", errors="ignore"))


