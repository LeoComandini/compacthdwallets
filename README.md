# HD wallets with 32 bytes public or private backups for master and subkeys

**TL;DR**: using *pay-to-contract* to derive a HD wallet allows shorter
backups.

BIP32 relies on extended keys to derive new keys.
Extended keys are 78 bytes long, but only key and chaincode (64 or 65 bytes) are
used to derive new keys.

It is possible to define HD wallets with the same features as BIP32 that does
not need the chaincode.

Let `G` be the secp256k1 generator.
Let `i` be the child index.
Let `(p, P=pG)` and `(p_i, P_i=p_iG)` be the parent and i-th child keypairs
respectively.
Let `h` be an adequately strong hash function which converts its outputs to
integers.
Define private and public child derivation as follow:

    p_i(p, i) = (i < 2^31)  p + h(pG, i)
                (i >= 2^31) h(p, i)

    P_i(P, i) = (i < 2^31)  P + h(P, i)G
                (i >= 2^31) not possible

Notes:
- The tweak to the parent key is also known as *pay-to-contract* and is the same
  principle underlying taproot. 
- The above formulae suggest to a tree structure similar to bip32, however that
  implies an EC scalar multiplication and addition for each public derivation
  level (parent to child). It is possible to reduce the number of EC operations
  needed by including the full (unhardened) path in the hash function input.
- The hash function input may include additional information, such as the script
  type.

## Advantages

### Shorter backups and descriptors
Multisig wallets needs to backup the other parties extended public keys.
For instance the backup can be an output descriptor with a xprv and multiple
xpub.
Using the above derivation scheme reduces the length of the descriptor that
should be backed up or passed around (e.g. to a hardware device).
With some additional work 32 bytes pubkeys can be used.

### 1 to 1 conversion mnemonic-child private or public key
Existing standards can be used to backup child private keys. Suppose you have a
master keypair it's possible to hardened derive child keys and use them as
separate wallet with a common backup (similar scope of BIP85).
Each child key can be used as master key for another "sub" wallet with the
master key still being able to spend such funds (same as BIP32). But contrary
to BIP32 each "sub" wallet has a 32 bytes backup. Which optionally can be mapped
to a, for instance, 24 word BIP39 mnemonic.

Since pubkeys can have the same length, it is possible to backup or share
pubkeys with a similar technique.

## Disadvantages
BIP32 is used by almost every existing wallets.

## TODOs
- More investigation on analogous proposal
- Add python example
- Add references

## Copyright

[MIT](LICENSE)
