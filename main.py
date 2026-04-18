import ast
import json
import random
import base64
import secrets as s
from cloudpathlib.exceptions import MissingCredentialsError
from cryptography.fernet import Fernet

def SparkEnc(data , mode="encode",key=None):
    def chunkcipher(data, mode="encode"):
        def tbinary(text):
            return ''.join(format(ord(c), '08b') for c in text)
        def fbinary(binary_text):
            return ''.join(chr(int(binary_text[i:i + 8], 2)) for i in range(0, len(binary_text), 8))
        def obfbinary(data):
            def obfe(text):
                return ''.join(str(ord(c) << 1) + ' ' for c in text).strip()

            shits = []
            for x, shit in enumerate(data):
                num = str(shit)
                x = str(x + 1)
                obfdata = obfe(num)
                obforder = obfe(x)
                shits.append((obfdata, obforder))
            random.shuffle(shits)
            return shits

        def deobfbinary(data):
            final = []
            def obfd(encoded):
                nums = encoded.split()
                return ''.join(chr(int(n) >> 1) for n in nums)

            for x2 in range(len(data) + 1):
                for d in data:
                    e = d[0]
                    o = d[1]
                    num = obfd(e)
                    x = obfd(o)
                    if str(x) == str(x2):
                        final.append(num)
            return "".join(final)
        if mode == "decode":
            chunked = deobfbinary(data)
            text = fbinary(chunked)
            return text
        else:
            bdata = tbinary(data)
            chunks = obfbinary(bdata)
            return chunks
    def encoder(data):
        def encrypterXOR(data):
            def randomnumber():
                tok = s.token_hex(16)
                binary = ''.join(format(ord(c), '08b') for c in tok)
                data_bytes = int(binary, 2).to_bytes(len(binary) // 8, 'big')
                offset = data_bytes[-1] & 0x0F
                chunk = data_bytes[offset:offset + 4]
                num = int.from_bytes(chunk, 'big') & 0x7fffffff
                number = num % 1000000
                return str(number)
            def encode(text, key):
                encoded_chars = []
                for i, c in enumerate(text):
                    encoded_c = chr(ord(c) ^ ord(key[i % len(key)]))
                    encoded_chars.append(encoded_c)
                return ''.join(encoded_chars)

            dumped = json.dumps(data)
            key = randomnumber()
            encoded = encode(dumped, key)
            return encoded.encode("utf-8").hex(), key
        def encrypterAES(data):
            key = Fernet.generate_key()
            cipher = Fernet(key)
            dumped = json.dumps(data)
            encrypted = cipher.encrypt(dumped.encode("utf-8"))
            return encrypted, key
        xordata, xorkey = encrypterXOR(data)
        aesdata, aeskey = encrypterAES(xordata)
        keyf = {
            "x":xorkey,
            "a":aeskey.decode()
        }
        jskey = json.dumps(keyf)
        key = chunkcipher(jskey)
        base64key = base64.b64encode(str(key).encode())

        return aesdata , base64key
    def decoder(data, key):
        decoded = base64.b64decode(key).decode()
        key = ast.literal_eval(decoded)
        def decode(hex_string, key):
            data = bytes.fromhex(hex_string)
            decoded_chars = []
            for i, b in enumerate(data):
                decoded_c = chr(b ^ ord(key[i % len(key)]))
                decoded_chars.append(decoded_c)
            return ''.join(decoded_chars)
        keys = json.loads(chunkcipher(key,mode="decode"))
        xorkey = keys["x"]
        aeskey = keys["a"]
        cipher = Fernet(aeskey)
        decrypted = cipher.decrypt(data).decode("utf-8").replace('"',"")
        dec = decode(decrypted,str(xorkey))
        return dec
    if mode == "encode":
        e,k = encoder(data)
        return e, k
    else:
        if not key == None:
            d = decoder(data, key )
            return d
        else:
            raise MissingCredentialsError
