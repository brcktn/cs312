import random
from sympy import isprime


# Extended Euclidean Algorithm to find x, y, and gcd
def ext_euclid(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = ext_euclid(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


# Function to generate a large prime number
def generate_large_prime(bits=512):
    while True:
        p = random.getrandbits(bits)
        if isprime(p):
            return p


# Function to generate RSA keys
def generate_rsa_keys(bits=512):
    # Generate two distinct prime numbers p and q
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)

    while p == q:
        q = generate_large_prime(bits)

    # Compute N = p * q
    N = p * q

    # Compute the totient of N, phi(N) = (p-1)(q-1)
    phi_n = (p - 1) * (q - 1)

    # Choose an integer e such that 1 < e < phi(N) and gcd(e, phi(N)) = 1
    e = random.randrange(2, phi_n)
    while True:
        gcd, x, y = ext_euclid(e, phi_n)
        if gcd == 1:  # e is coprime with phi(N)
            break
        e = random.randrange(2, phi_n)

    # Compute d, the modular multiplicative inverse of e mod phi(N)
    _, d, _ = ext_euclid(e, phi_n)
    d = d % phi_n  # Ensure d is positive

    return N, e, d


# Function for modular exponentiation (for testing)
def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result


# Test the RSA key generation and modular exponentiation
def test_rsa():
    N, e, d = generate_rsa_keys(8)  # Smaller key size for testing
    print(f"Public Key: (N={N}, e={e})")
    print(f"Private Key: (N={N}, d={d})")

    # Test encryption and decryption
    message = random.getrandbits(int(8 / 4))  # Example message
    print(f"Original message: {message}")

    # Encrypt the message: cipher = (message^e) % N
    cipher = mod_exp(message, e, N)
    print(f"Encrypted message: {cipher}")

    # Decrypt the message: decrypted = (cipher^d) % N
    decrypted = mod_exp(cipher, d, N)
    print(f"Decrypted message: {decrypted}")

    # Check if the decrypted message matches the original message
    assert message == decrypted, "Decryption failed!"
    print("Test passed: Decryption successful!")


# Run the test
test_rsa()
