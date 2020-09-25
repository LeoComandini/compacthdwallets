# HD wallets with 32 bytes public or private backups for master and subkeys

BIP32 [1] relies on extended keys to derive new keys.
Extended keys are 78 bytes long, but only key and chaincode (64 or 65 bytes) are
used to derive new keys.

It is possible to define HD wallets with the same features as BIP32 that does
not need the chaincode.

Let `G` be the secp256k1 generator.
Let `i` be the child index.
Let `(p, P=pG)` and `(p_i, P_i=p_iG)` be the parent and i-th child keypairs
respectively.
Let `h` be an adequately strong hash function which converts its output to
integer.
Define private and public child derivation as follow:

    p_i(p, i) = (i < 2^31)  p + h(pG, i)
                (i >= 2^31) h(p, i)

    P_i(P, i) = (i < 2^31)  P + h(P, i)G
                (i >= 2^31) not possible

Notes:
- The actual main difference with respect to BIP32 is that the chaincode is not
  included in the hash function inputs.
- The tweak to the parent key is also known as *pay-to-contract* [2] and is the
  same principle underlying taproot [3].
- The hash function input may include additional information, such as the script
  type.

## Advantages

### Shorter backups and descriptors
Multisig wallets need to backup the other parties extended public keys.
For instance, the backup can be an output descriptor with a xprv and multiple
xpub.
Using the above derivation scheme reduces the length of the descriptor that
should be backed up or passed around (e.g. to a hardware device).
With some additional work 32 bytes pubkeys can be used.

### Two-way mapping mnemonic to child private or public key
Most Bitcoin wallets allow restoring only from 12 or 24-words (BIP39 [4])
mnemonics, which map to 16 or 32 bytes sequences respectively.

From the mnemonic a tree of BIP32 exteneded keys is derived using a
non-reversable function.
However each BIP32 extended key needs at least 64 bytes to be represented,
making unfeasible the usage of standard such as BIP39.

This led to the arise of proposal such as BIP85 [5], which allows to derive
BIP39 mnemonics and other common backups from a BIP32 extended key.

The above derivation scheme allows intermediate user-friendly backups.
Suppose you have a master keypair, it's possible to harden derive child keys
and use them as a separate wallet with a common backup.
Each child key can be used as master key for another child wallet with the
master key still being able to spend such funds (same as BIP32). But contrary
to BIP32 each child wallet has a 32 bytes backup. Which optionally can be
mapped to a, for instance, 24 word BIP39 mnemonic. This allows to maintain the
same UX for child wallets.

Since pubkeys can have the same length, it is possible to backup or share
pubkeys with a similar technique.

A possible use case: Alice wants to teach to her unexperienced son Bob how to
use a Bitcoin wallet. She already has a wallet with master private key `a`,
let `i = 2^31` (i.e. `0_h`), she derives `b = a_i = h(a, i)`, maps `b` to the
backup expected by the wallet (e.g. mnemonic) and gives the backup to Bob.
Bob can use his wallet as a normal wallet, while Alice can monitor Bob's
transaction and eventually she can move coins in his place.

## Disadvantages
BIP32 is used by almost every existing wallets.

Suppose an attacker knows a child private key `p_i`, its index `i<2^31` and its
parent public key `P`. If the above derivation scheme is used, it can compute
the parent private key `p`. If using BIP32, it cannot, but it could if it knew
the chaincode.
However most wallets derive scriptpubkeys from keys from the same depth, so the
parent public key is never published on the blockchain. If the parent public
key is kept as secret as BIP32 extended keys are, then the situation is
analoguos to BIP32's.

## Examples
A simplified python example is provided.

Install package:

    pip install .

Run tests:

    python3 -m unittest discover -v

## TODOs
- More investigation on analogous proposals
- Add python examples
- Polish python code

## Copyright

`ecc.py` module was copied and adapted from BIP340's pure python reference
implementation [5].

[MIT](LICENSE)

## References
[1] https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki

[2] https://blockstream.com/sidechains.pdf Appendix A

[3] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2018-January/015614.html

[4] https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

[5] https://github.com/bitcoin/bips/blob/master/bip-0085.mediawiki

[6] https://github.com/bitcoin/bips/blob/master/bip-0340/reference.py
