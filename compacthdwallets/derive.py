import hashlib

from compacthdwallets.ecc import (
    bytes_from_point,
    G,
    int_from_bytes,
    n,
    point_add,
    point_mul,
    Point,
)


def h(P: Point, i: int) -> bytes:
    """h(P, i) = sha256(P || i)

    The choice of using sha256 is arbitrary and questionable."""

    return int_from_bytes(hashlib.sha256(bytes_from_point(P) + i.to_bytes(4, byteorder="big")).digest())

def CKDprv(p: int, i: int) -> int:
    """Private Child Key Derivation"""

    P = point_mul(G, p)
    if 2**31 <= i < 2**32:
        return h(P, i)
    elif 0 <= i < 2**31:
        return (p + h(P, i)) % n
    else:
        raise ValueError("Invalid index")

def CKDpub(P: Point, i: int) -> Point:
    """Public Child Key Derivation"""

    if 2**31 <= i < 2**32:
        raise ValueError("Not possible")
    elif 0 <= i < 2**31:
        return point_add(P, point_mul(G, h(P, i)))
    else:
        raise ValueError("Invalid index")
