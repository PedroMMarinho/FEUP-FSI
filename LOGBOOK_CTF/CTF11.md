# CTF Semana 11 (Weak Encryption)

## Tarefa 1

**Ao investigar o cipherspec.py o que é que está de errado na forma como estes algoritmos estão a cifrar?**

- **Erro Principal**: A criação da chave está mal implementada visto que, devido ao hotfix para tornar o a função mais rápida, apenas os últimos 3 bytes são randomizados, tornando o resto dos 13 bytes fáceis de prever, sendo neste caso `\x00`.

- **Impacto**: A cifra AES-CTR, que é considerada segura, perde a sua eficácia porque a chave, que se torna previsível, reduz drasticamente o tempo de pesquisa, o que facilita a utilização de ataques de **brute force**.

**Como consigo usar esta ciphersuite para cifrar e decifrar dados?**

É possível cifrar e decifrar dados, utilizando as funções providenciadas, através dos seguintes comandos:

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from binascii import unhexlify
import itertools

# Criação da chave
key = gen()

# Criação de um nonce aleatório (16 bytes)
nonce = urandom(16)

# Mensagem a cifrar
mensagem = b"flag{mensagem_secreta}"

# Cifração
criptograma = enc(key, mensagem, nonce)

# Decifração
mensagem_decifrada = dec(key, criptograma, nonce)
```

**Como consigo fazer uso da vulnerabilidade que observei para quebrar o código?**:

Para tal, podemos criar um programa que vai tentar descobrir a flag através de um ataque de brute force, visto que apenas precisamos de acertar os últimos **três bytes**.

**Como consigo automatizar este processo, para que o meu ataque saiba que encontrou a flag?**

De forma a automatizar este processo, criamos um script de python que faz a pesquisa de todas as combinações possíveis da chave, apenas alterando a parte dinâmica ao longo do programa.

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from binascii import unhexlify
import itertools

# Dados iníciais
nonce_hex = "4e7c118824f0c9ef7d6c24bbc884a638"
ciphertext_hex = "80fcebd25ae41cfc96a045bf1a943239879270f2d0e8"

nonce = unhexlify(nonce_hex)
ciphertext = unhexlify(ciphertext_hex)

# AES tamanho do bloco
KEYLEN = 16

def decrypt_with_key(key, ciphertext, nonce):
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce)) # utilizar o nonce e a chave gerada
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# Brute-force os últimos 3 bytes da chave
def brute_force_aes_ctr():
    fixed_part = b'\x00' * (KEYLEN - 3)  # Primeiros 13 bytes fixos
    for suffix in itertools.product(range(256), repeat=3):  # 256^3 possibilidades
        key = fixed_part + bytes(suffix)
        try:
            decrypted_message = decrypt_with_key(key, ciphertext, nonce)
            if decrypted_message.startswith(b"flag{") and decrypted_message.endswith(b"}"):
                return decrypted_message.decode(), key
        except Exception:
            continue
    return None, None

# Chamar a função de brute-force
flag, key = brute_force_aes_ctr()

if flag:
    print(f"Found flag: {flag}")
    print(f"Key: {key.hex()}")
else:
    print("Failed to decrypt the ciphertext.")
```

No final o nosso _output_ será: 

`Found flag: flag{gawlydjvcdazqkar} Key: 00000000000000000000000000ed841d`

## Tarefa 2

**O quão grande teria que ser o offset em cipherspec.py para que fosse inviável que as máquinas pessoais usadas no ataque conseguissem descobrir a chave no pior caso, durante um período de 10 anos?**

Para descobrir o offset criamos um script que vai verificar o tempo de execução que demora a descobrir a flag, e fazemos a devida conversão para 10 anos, obtendo assim o offset necessário para impossibilitar um ataque de 10 anos.

```python
import time
import itertools
from os import urandom
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import itertools

def dec(k, c, nonce):
	cipher = Cipher(algorithms.AES(k), modes.CTR(nonce))
	decryptor = cipher.decryptor()
	msg = b""
	msg += decryptor.update(c)
	msg += decryptor.finalize()
	return msg

# Configuração para o teste
FIXED_PART = b'\x00' * 13  # Parte fixa da chave
ciphertext = urandom(32)  # Texto cifrado fictício
nonce = urandom(16)  # Nonce aleatório
test_key = FIXED_PART + b'\x00\x00\x00'  # Chave base para testar

def test_key_speed(duration=5):
    """Calcula quantas chaves podem ser testadas em um intervalo de tempo."""
    count = 0
    start_time = time.time()
    while time.time() - start_time < duration:
        for suffix in itertools.product(range(256), repeat=3):  # Espaço para offset 3
            key = FIXED_PART + bytes(suffix)
            try:
                dec(key, ciphertext, nonce)  # Tentativa de decifrar
            except Exception:
                pass  # Ignorar exceções para focar apenas no desempenho
            count += 1
    return count / duration  # Retorna chaves por segundo

# Testar a performance
keys_per_second = test_key_speed()
print(f"Chaves testadas por segundo: {keys_per_second:.2f}")

# Calcular combinações possíveis em 10 anos
seconds_in_10_years = 10 * 365 * 24 * 60 * 60
total_keys_10_years = keys_per_second * seconds_in_10_years

# Determinar o offset mínimo
offset = 3  # Inicializar com offset pequeno
while (2 ** (8 * offset)) < total_keys_10_years:
    offset += 1

print(f"Offset necessário para inviabilizar ataque em 10 anos: {offset}")
```

Neste caso, obtemos um **offset de 7**.


## Tarefa 3

**O autor desta otimização teve outra ideia "brilhante". Usar o nonce com 1 byte de tamanho e não o enviar na rede! Isso obrigaria o adversário a testar todas as 2^8 possibilidades para cada chave possível, de modo a conseguir conduzir o ataque. Explique de que forma esta não é uma contra-medida eficaz para fortalecer a segurança destes esquemas de cifra.**

Reduzir o tamanho do nonce para **1 byte** é realmente uma péssima ideia, visto que o número de possibilidades é um incremento desprezível no esforço total no que toca em encontrar a chave correta. Para além disso, caso fosse necessário decifrar mais que 256 mensagens diferentes, usar um nonce com apenas 1 byte, iria causar colisões inevitáveis, o que comprometeria a robustez da segurança do sistema.

