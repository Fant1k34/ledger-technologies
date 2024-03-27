from collections import namedtuple
from math import gcd
import random

PublicKey = namedtuple("PublicKey", ["e", "n"])
PrivateKey = namedtuple("PrivateKey", ["d", "n"])

MIN_RANDOM = 250000000000000
MAX_RANDOM = 25000000000000000000000
DEFAULT_NUMBER_OF_ITERATIONS = 5


def miller_test(d: int, n: int) -> bool:
    """Miller Test implementation
    """
    a = 2 + random.randint(1, n - 4)
    x = pow(a, d, n)
 
    if x == 1 or x == n - 1:
        return True
 
    while d != n - 1:
        x = (x * x) % n
        d = d * 2
 
        if x == 1:
            return False
        
        if x == n - 1:
            return True
 
    return False


def is_prime(n: int, k: int) -> bool:
    """Checks if the number is prime with Miller Test
    """
    if n <= 1:
        return False
    
    if n in [2, 3, 5, 7, 11]:
        return True
 
    d = n - 1
    while d % 2 == 0:
        d //= 2
 
    for _ in range(k):
        if not miller_test(d, n):
            return False
 
    return True


def get_random_prime(value: int) -> int:
    """Compute random number starting with value
    """
    if value & 1 == 0:
        value += 1

    while not is_prime(value, DEFAULT_NUMBER_OF_ITERATIONS):
        value += 2

    return value


def mod_inv(a: int, m: int) -> int:
    """Compute the modular multiplicative inverse of a with module m
    """
    m0, x0, x1 = m, 0, 1

    # Extended Euclidean Algorithm to find the modular inverse
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0

    # Ensure the result is positive
    return x1 + m0 if x1 < 0 else x1


def process_evaluation() -> tuple[int, int, int]:
    # Generate random prime numbers p and q, and other primes
    while True:
        start_value_p = random.randint(MIN_RANDOM, MAX_RANDOM)
        start_value_q = random.randint(MIN_RANDOM, MAX_RANDOM)

        p = get_random_prime(start_value_p)
        q = get_random_prime(start_value_q)
        
        if p != q:
            break

    n = p * q
    m = (p - 1) * (q - 1)

    e = 65537
    d = mod_inv(e, m)

    return e, d, n


def generate_key_pair() -> tuple[PublicKey, PrivateKey]:
    """Generate a pair of public and private keys for RSA
    """
    e, d, n = process_evaluation()

    public_key = PublicKey(e, n)
    private_key = PrivateKey(d, n)

    return public_key, private_key


def encrypt(message: int, public_key: PublicKey) -> int:
    """Provide encryption of message with public_key
    """
    return pow(message, public_key.d, public_key.n)


def decrypt(cipher: int, private_key: PrivateKey) -> int:
    """Provide decryption of message with private_key
    """
    return pow(cipher, private_key.e, private_key.n)


if __name__ == '__main__':
    message = 563000

    public, private = generate_key_pair()

    encrypted = encrypt(message, private)
    decrypted = decrypt(encrypted, public)

    assert message == decrypted, ("Message was", message, "but got", decrypted)

    print(f"Message: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
