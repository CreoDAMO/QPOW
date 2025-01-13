class PQCWrapper:
    def __init__(self, backend="quantcrypt"):
        self.backend = backend.lower()
        if self.backend == "quantcrypt":
            import quantcrypt
            self.lib = quantcrypt
        elif self.backend == "pqclean":
            import pqcrypto.sign.dilithium2 as pqclean
            self.lib = pqclean
        else:
            raise ValueError("Unsupported PQC backend. Choose 'quantcrypt' or 'pqclean'.")

    def generate_keypair(self):
        return self.lib.generate_keypair()

    def sign(self, message: bytes, private_key: bytes):
        return self.lib.sign(message, private_key)

    def verify(self, message: bytes, signature: bytes, public_key: bytes):
        return self.lib.verify(message, signature, public_key)