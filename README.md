# SparkEnc - A Secure Data Encryption Library

SparkEnc is a Python library designed for secure data encryption and decryption using a combination of XOR and AES encryption algorithms. The library provides a simple interface for encoding and decoding data, making it suitable for applications that require data confidentiality.

## Features

- **Data Encoding**: Convert plaintext data into an encrypted format.
- **Data Decoding**: Retrieve original data from the encrypted format.
- **Dual Encryption**: Uses both XOR and AES encryption for enhanced security.
- **Random Key Generation**: Generates unique keys for each encryption operation.
- **Chunk Ciphering**: Breaks down data into chunks to obfuscate the binary representation.

## Installation

To use SparkEnc, you'll need to have Python installed on your machine. You can install the required dependencies using pip:

```bash
pip install cryptography
```

## Usage

### Importing the Library

Start by importing the `SparkEnc` function from the module:

```python
from spark_enc import SparkEnc
```

### Encoding Data

To encode data, call the `SparkEnc` function with the data you want to encrypt and specify the mode as "encode". For example:

```python
data = {"username": "user", "password": "secure_password"}
encrypted_data, key = SparkEnc(data, mode="encode")

print("Encrypted Data:", encrypted_data)
print("Encryption Key:", key)
```

### Decoding Data

To decode data, call the `SparkEnc` function with the encrypted data and the key generated during encoding. Set the mode to "decode". For example:

```python
decoded_data = SparkEnc(encrypted_data, mode="decode", key=key)

print("Decoded Data:", decoded_data)
```

### Handling Missing Credentials

If you attempt to decode data without providing a key, a `MissingCredentialsError` will be raised. Ensure you store the key securely after encoding for future decoding.

## Example

Here is a complete example demonstrating encoding and decoding:

```python
from spark_enc import SparkEnc

# Sample data to be encrypted
data = {"username": "user123", "password": "my_secret_pass"}

# Encoding the data
encrypted_data, key = SparkEnc(data, mode="encode")
print("Encrypted Data:", encrypted_data)
print("Encryption Key:", key)

# Decoding the data
try:
    decoded_data = SparkEnc(encrypted_data, mode="decode", key=key)
    print("Decoded Data:", decoded_data)
except MissingCredentialsError as e:
    print("Error:", str(e))
```

## Security Considerations

- Always keep your encryption keys secure. Never hard-code them in your source code.
- Use strong passwords and unique keys for different encryption tasks.
- Regularly update and rotate your encryption keys to enhance security.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! If you have suggestions for improvements or would like to add new features, please open an issue or submit a pull request.

## Contact

For questions or feedback, please reach out via GitHub issues or contact the maintainer directly.
