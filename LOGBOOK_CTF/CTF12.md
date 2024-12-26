# CTF Semana 12 (RSA)

## Reconhecimento do Ambiente

Neste desafio, vamos explorar o método de cifração `RSA`, de modo a perceber como este funciona e como podemos decifrar uma mensagem sabendo os primos a que foram utilizados.

Sendo assim, para resolvermos o seguinte problema, são disponilizados os seguintes dados:

- O expoente público `e = 65537`

- O módulo `n = 87777985100699018932094980018995348321190282174917313121792031815299158108154767154642811192581804697812555605405953787919330941803914366451585659492418224310284735827777424547738583851212264460897302213165924339933324276893486075954339784316175553712334493638957419692734948763763918793616499789655592951`

- O criptograma, em hexadecimal `"cd23cc233f7a5b9adb51e5616da489ab56c793d6fda7e4461c7780c3c060bced506b33a29ae9529baa157c8f8e4b4025b335fd930a26c9e387e9ce364be5ef8f9901ae9072e26cebb59ce0c682b49d3d1858bf15bfc886df6505e5a84ff541763b90c7a8a09ba863d499e994613dd1e44be0df788ee281455ecf06f936ee1e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"`
  
- Turno 2, Grupo 2
- `p` é um primo próximo de `2^500+(((t-1)*10 + g) // 2)` = 2^506
- `q` é um primo próximo de `2^501+(((t-1)*10 + g) // 2)` = 2^507

## Tarefas

Primeiramente, temos de descobrir os números primos exatos de `p` e `q`, para tal vamos utilizar o algoritmo `Miller-Rabin` para testar a primalidade enquanto testamos os números.


```python
# Algoritmo de Miller-Rabin
def miller_rabin(n, k=40):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Encontrar primo próximo
def find_prime_near(n, offset, range_limit=1000000000):
    t = 500 + offset
    p_guess = 2 ** t
    
    for dp in range(0, range_limit):
        p = p_guess + dp
        if miller_rabin(p):
            q = n // p
            if n % p == 0 and miller_rabin(q):
                return p, q
    raise ValueError("Primes not found in range.")
```


Após obtermos os números primos, temos de implementar o `RSA`. Neste caso, vamos ter de calcular os valores de `e` e de `d`, sendo `e` a chave pública e o `d` a chave secreta, tal que o valor destes terá de equivaler: `ed % (p-1)(q-1) = 1`.


Sendo assim, criamos as seguintes funções para executar este cálculo, que por sua vez, decifra a mensagem secreta com a chave `d` descoberta.

```python
# Algoritmo estendido de Euclides
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

# Função para decifrar
def decrypt_rsa(ciphertext, e, n):
    t = 2
    g = 2
    offset = ((t-1)*10+g) // 2
    p, q = find_prime_near(n,offset)

    phi = (p - 1) * (q - 1)
    _, d, _ = extended_gcd(e, phi)
    d = d % phi
    if d < 0:
        d += phi

    # Decifrar o texto
    int_ciphertext = int.from_bytes(ciphertext, "little")
    int_plaintext = pow(int_ciphertext, d, n)
    plaintext = int_plaintext.to_bytes((int_plaintext.bit_length() + 7) // 8, 'little')
    return plaintext
```

Por fim, temos de responder às seguintes questões:

- **Como consigo usar a informação que tenho para inferir os valores usados no RSA que cifrou a flag?**: O código implementa a decriptação de uma mensagem cifrada com RSA. Começamos por estimar os números primos 𝑝 e 𝑞 próximos de 2^506 e 2^507, respetivamente, ajustados pelo _offset_ do nosso grupo. Para verificar a primalidade, utilizamos a função `Miller-Rabin`. Depois, de calcularmos os valores de 𝑝 e 𝑞, fizemos o ϕ(n)=(p−1)⋅(q−1) e, com isso, utilizamos o `algoritmo estendido de Euclides` para determinar a chave privada 𝑑. Com a chave privada, foi possível finalmente desencriptar a mensagem cifrada.

- **Como consigo descobrir se a minha inferência está correta?**: Como já referido anteriormente, utilizamos o calcúlo ϕ(n)=(p−1)⋅(q−1), para confirmarmos a validade do `RSA`.

- **Finalmente, como posso extrair a minha chave do criptograma que recebi?**: Para extrair a chave privada e decriptar o criptograma RSA, é necessário calcular ϕ(n)=(p−1)⋅(q−1), onde 𝑝 e q são os primos usados para gerar o módulo 𝑛. Após calcular ϕ(n), encontra-se o valor de 𝑑, que é o inverso de 𝑒 módulo ϕ(n), usando o Algoritmo de Euclides Estendido. Com 𝑑, podemos decriptar o criptograma c usando a fórmula m=c^d(mod n), onde 𝑚 é a mensagem original.

Sendo assim, ao correr o [script.py](resources/CTF12/script.py) obtemos a `flag{pvuokifusjxpagsy}`.
