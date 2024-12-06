
# Trabalho realizado na Semana #11

## Tarefa 1

Nesta tarefa é nos indicado criar um CA (Certificate Authority) para emitir certificados digitais. Sendo assim, começamos por copiar o ficheiro OpenSSL para a nossa diretoria.

```bash
cp /usr/lib/ssl/openssl.cnf .
```
Neste novo ficheiro, teremos de modificar a linha referente a `unique_subject`, descomentando-la.

![uncomentSubject](resources/LOGBOOK11/uncomentSubject.png)

De seguida, criamos o ficheiro vazio `index.txt` e `serial` com um número em string.

```bash
touch index.txt
echo 1000 > serial
```

Agora executamos o seguinte comando para criar o nosso certificado, passando já a informação da _password_ e o _suject_.

```bash
openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 \
-keyout ca.key -out ca.crt \
-subj "/CN=www.modelCA.com/O=Model CA LTD./C=US" \
-passout pass:dees
```

![caCertificate](resources/LOGBOOK11/caCertificate.png)

Consequentemente, é nos pedido para correr os seguintes comandos e através do _output_
identificar o que é questionado em baixo:

```bash
# Comandos a ser executados
openssl x509 -in ca.crt -text -noout
openssl rsa -in ca.key -text -noout
```

**Qual parte do certificado indica que este é um certificado de uma Autoridade Certificadora (CA)?**

Nesta imagem, podemos verificar que no texto encontra-se `CA:TRUE`, o que indica que realmente é um Certificado de uma Autoridade Certificadora

![caConfirm](resources/LOGBOOK11/caConfirm.png)

**Qual parte do certificado indica que este é um certificado autoassinado?**

Nesta imagem, podemos verificar que como a `Subject Key Identifier` é igual à `Authority Key Identifier`, significa que fomos nós a criar o certificado.

![selfAssign](resources/LOGBOOK11/selfAssign.png)

**No algoritmo RSA, temos um expoente público e, um expoente privado d, um módulo n e dois números secretos p e q, de forma que n = pq. Por favor, identifique os valores desses elementos nos seus arquivos de certificado e chave.**

Módulo `n` do certificado:

![moduloNCertificado](resources/LOGBOOK11/moduloNCertificado.png)

Módulo `n` da chave:

![moduloNChave](resources/LOGBOOK11/moduloNChave.png)

Expoente público `e` do certificado:

![moduloExpCertificado](resources/LOGBOOK11/moduloExpCertificado.png)

Expoente público `e` da chave:

![moduloExp](resources/LOGBOOK11/moduloExp.png)

Expoente privado `d` da chave:

![moduloExpPriv](resources/LOGBOOK11/moduloExpPriv.png)

Número secreto `p` da chave: 

![prime1](resources/LOGBOOK11/prime1.png)

Número secreto `q` da chave: 

![prime2](resources/LOGBOOK11/prime2.png)


O valor do módulo `n` será equivalente a `p` * `q`.

## Tarefa 2

Esta tarefa tem o objetivo de criar um Request de Certificado para o nosso servidor.

Para tal executamos o comando para gerar CSR para `www.bank32.com`:

```bash
openssl req -newkey rsa:2048 -sha256 \
-keyout server.key -out server.csr \
-subj "/CN=www.bank32.com/O=Bank32 Inc./C=US" \
-passout pass:dees
```

![serverBank32](resources/LOGBOOK11/serverBank32.png)

Nós podemos utilizar os comandos já explorados na tarefa anterior para verificar o conteúdo descodificado.

```bash
openssl req -in server.csr -text -noout
openssl rsa -in server.key -text -noout
```

Seguidamente, vamos adicionar dois nomes alternativos para o login do request do certificado, para que o SAN esteja de ligado a esse mesmo.

```bash
openssl req -newkey rsa:2048 -sha256 \
-keyout server.key -out server.csr \
-subj "/CN=www.bank32.com/O=Bank32 Inc./C=US" \
-passout pass:dees -addext "subjectAltName = DNS:www.bank32.com, \
DNS:www.bank32A.com, \
DNS:www.bank32B.com"
```
![serverAlternateNames](resources/LOGBOOK11/serverAlternateNames.png)

## Tarefa 3

Nesta tarefa, teremos de gerar um certificado para o servidor.

Para tal vamos executar o seguinte comando:

```bash
openssl ca -config openssl.cnf -policy policy_anything \
-md sha256 -days 3650 \
-in server.csr -out server.crt -batch \
-cert ca.crt -keyfile ca.key
```

![databaseCSR](resources/LOGBOOK11/databaseCSR.png)

Seguidamente, temos de descomentar no nosso ficheiro `openssl.cnf` a linha `copy_extensions = copy`.

Agora corremos o seguinte comando para verificar se os nomes alternativos são incluídos:

```bash
openssl x509 -in server.crt -text -noout
```
Podemos ver que temos o que queriamos:

![alternativeNames](resources/LOGBOOK11/alternativeNames.png)

## Tarefa 4

Após sabermos as bases de como criar um Certificado de Autoridade, nesta tarefa iremos dar _setup_ do site `www.bank32.com` através de um server `Apache`.

Para tal, precisamos de garantir que o ficheiro `Dockerfile` está corretamente configurado, assim como, `bank32_apache_ssl.conf` e, a informação do certificado está na diretoria correta.

![diretoriaKey&Crt](resources/LOGBOOK11/diretoriaKey&Crt.png)

![dockerfile](resources/LOGBOOK11/dockerfile.png)

![bankConfig](resources/LOGBOOK11/bankConfig.png)

Como podemos observar, neste lab, todas as configurações já veem corretamente configuradas.

Sendo assim, agora vamos abrir o container com o comando `dcup` e ,seguidamente, acedemos à shell do container aberto através dos comandos `dockps e docksh <id>`, e por fim corremos o comando `service apache2 start`, para abrir o servidor:

![apacheStart](resources/LOGBOOK11/apacheStart.png)

Podemos verificar que quando abrimos o servidor com o link http://www.bank32.com, temos uma tela vermelha.

![httpBank](resources/LOGBOOK11/httpBank.png)

E quando abrimos o servidor com o link https://www.bank32.com, temos uma tela verde.

![httpsBank](resources/LOGBOOK11/httpsBank.png)

Este comportamento é normal, uma vez que foi designado no ficheiro de configuração do servidor. No entanto, ao navegar pelo site via HTTPS, o navegador alerta-nos de que a ligação ao site não é segura.

![notSecure](resources/LOGBOOK11/notSecure.png)

Para resolver este problema, temos de ir às `preferences` do firefox e ir à secção dos certificados. Aí, iremos adicionar o ficheiro `modelCA.crt` visto que é a chave pública que "assinou" o `bank32.crt`.

![modelCA](resources/LOGBOOK11/modelCA.png)

Após dar refresh ao firefox, a nossa conexão será totalmente segura:

![bank32CA](resources/LOGBOOK11/bank32CA.png)


## Tarefa 5

Nesta tarefa, vamos fazer utilizar o nosso servidor a partir do acesso do site `www.example.com`. Quando um utilizador visitar o site `www.example.com`, ele será redirecionado para o nosso `www.example.com`, que está alojado num IP diferente do original. 

Sendo assim, o primeiro passo será adicionar uma nova entrada no VirtualHost ao ficheiro /etc/apache2/sites-available/bank32_apache_ssl.conf:

```
<VirtualHost *:443>
    DocumentRoot /var/www/bank32
    ServerName www.example.com
    DirectoryIndex index.html
    SSLEngine On
    SSLCertificateFile /certs/server.crt
    SSLCertificateKeyFile /certs/server.key
</VirtualHost>
```

De seguida adicionamos o DNS do servidor no ficheiro `/etc/hosts`:
`10.9.0.80    www.example.com`

Ao acedermos ao site `www.example.com`, como estamos a usar o mesmo certificado que em `www.bank32.com`, o navegador avisa-nos de que este certificado não é para `www.example.com`, comparando o URL visitado com o Common Name apresentado no certificado. Podemos ver esse aviso na imagem seguinte:

![exampleSite](resources/LOGBOOK11/exampleSite.png)

## Tarefa 6

Após termos criado o nosso _fake website_ `www.example.com`, vamos tentar fazer com que o aviso, de o site ser de risco, seja omitido através de um CA fabricado por nós, no sentido de o utilizador não suspeite que está a aceder um website de outra origem.
Sendo assim, vamos criar um novo certificado para o nosso website malicioso.

Para tal corremos o comando para criar o _request_ do certificado:
```bash
openssl req -newkey rsa:2048 -sha256 \
-keyout malicious.key -out malicious.csr \
-subj "/CN=www.example.com/O=Example Inc./C=US" \
-passout pass:dees
```

E geramo-lo:

```bash
openssl ca -config openssl.cnf -policy policy_anything \
-md sha256 -days 3650 \
-in malicious.csr -out malicious.crt -batch \
-cert ca.crt -keyfile ca.key
```

Após gerarmos os ficheiros `malicious.csr` e `malicious.key` para o `www.example.com`, guardamo-los na diretoria `certs`.


Seguidamente, mudamos a entrada do `www.example.com` no _VirtualHost_, no ficheiro `/etc/apache2/sites-available/bank32_apache_ssl.conf` para:


![newExampleEntry](resources/LOGBOOK11/newExampleEntry.png)

Como podemos ver conseguimos com que o nosso servidor `www.example.com`, fica-se seguro.

![certificateHelloWorld](resources/LOGBOOK11/certificateHelloWorld.png)

**Apesar de assumirmos que estas autoridades de certificação são resistentes a ataques, realisticamente, devemos considerar sempre a possibilidade de serem comprometidas. Indique um mecanismo que permita reagir a essa ocorrência e impedir ataques, e que medidas um adversário pode tomar para evitar que esse mecanismo o impeça de tirar partido de uma autoridade de certificação comprometida.**:

Para mitigar os riscos de uma `autoridade de certificação` (CA) comprometida, utilizam-se mecanismos como listas de revogação de certificados (CRLs), o protocolo `OCSP` para verificar a validade deste em tempo real, certificados de transparência para registar publicamente todos os certificados emitidos e `pinning` de certificados para restringir quais são aceites em cituações críticas. Contudo, adversários podem bloquear servidores `OCSP`, explorar listas desatualizadas e manipular logs de transparência.