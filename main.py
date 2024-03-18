from collections import namedtuple
from math import gcd
import random

PublicKey = namedtuple("PublicKey", ["e", "n"])
PrivateKey = namedtuple("PrivateKey", ["d", "n"])

MIN_RANDOM = 2500
MAX_RANDOM = 12500


def count_primes_to(min_: int = 0, max_: int = None) -> list[int]:
    """Count prime numbers within a given range
    """
    primes: list[int] = list(range(max_))

    # Iterate over the list to mark non-prime numbers
    for dividerInd, divider in enumerate(primes):
        if divider < 2:
            continue

        # Mark multiples of the current divider as non-prime
        for ind in range(dividerInd + 1, len(primes)):
            if primes[ind] % divider == 0:
                primes[ind] = -1

    # Filter out non-prime numbers and numbers less than min_
    return list(filter(lambda x: x >= min_, primes))


def get_random_primes() -> list[int]:
    all_primes = count_primes_to(MIN_RANDOM, MAX_RANDOM)
    random.shuffle(all_primes)

    return all_primes


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
    p, q, *other_primes = get_random_primes()

    n = p * q
    m = (p - 1) * (q - 1)

    # Find a suitable value for the public exponent e
    d = next(number for number in other_primes if gcd(number, m) == 1)

    # Calculate the modular multiplicative inverse
    e = mod_inv(d, m)

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
    message = 563

    public, private = generate_key_pair()
    result = decrypt(encrypt(message, private), public)

    assert message == result, ("Message was", message, "but got", result)
