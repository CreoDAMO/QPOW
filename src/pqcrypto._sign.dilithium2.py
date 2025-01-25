from pqcrypto.sign import dilithium2
import os

# 1. Generate a Key Pair
public_key, private_key = dilithium2.generate_keypair()
print(f"Public Key (hex): {public_key.hex()}")
print(f"Private Key (hex): {private_key.hex()}")

# 2. Message to Sign
# Convert a string to bytes for signing
message = "This is a message to be signed".encode('utf-8')
print(f"Message (bytes): {message}")

# 3. Sign the Message
try:
    signature = dilithium2.sign(private_key, message)
    print(f"Signature (hex): {signature.hex()}")
except Exception as e:
    print(f"An error occurred while signing: {e}")

# 4. Verify the Signature
try:
    is_valid = dilithium2.verify(public_key, message, signature)
    print(f"Signature valid: {is_valid}")
except Exception as e:
    print(f"An error occurred during verification: {e}")

# 5. Tamper with the Message (Optional)
# Let's alter the message slightly
tampered_message = message + b" tampered"
try:
    is_valid_tampered = dilithium2.verify(public_key, tampered_message, signature)
    print(f"Signature valid for tampered message: {is_valid_tampered}")
except Exception as e:
    print(f"An error occurred during verification of tampered message: {e}")

# 6. Secure Key Storage
# Example of securely storing the private key
key_file = "private_key.bin"
with open(key_file, 'wb') as file:
    file.write(private_key)
    os.chmod(key_file, 0o600)  # Set file permissions to only allow owner read/write

# 7. Loading Keys from File
# When needed, load the private key securely
with open(key_file, 'rb') as file:
    stored_private_key = file.read()

# Verify if the loaded key matches the original
if stored_private_key == private_key:
    print("Private key loaded successfully.")
else:
    print("Warning: Private key does not match the original!")

# Clean up
os.remove(key_file)
