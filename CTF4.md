
# CTF Semana 4 (Environment Variables)


## Reconhecimento

### Dependências

O primeiro passo que optamos por tomar foi a procura de caracteristicas do sistema, para tal, analisamos a informação resultante de `apt list --installed` que se encontrava presente.

![Software instalado](resources/CTF4/softwareInstalado.png)

Conseguimos destacar as seguintes caracteristicas:

- bash 4.3-7
- apache2 2.4.7-1
- dhcp 4.2.4-7

### Funcionalidades

Também procuramos entender o funcionamento da plataforma, e o modo de funcionamento da caixa de input.
Percebemos que o nosso input era adicionado ao comando `ls -al`, o que utilizamos inicialmente a nosso favor de modo a encontrar a localização da `flag` dentro do sistema:

![Localização da flag](resources/CTF4/flagLocation.png)

## Pesquisa de vulnerabilidades

Após indentificadas as dependências do sistema, decidimos procurar por vulnerabilidades já conhecidas. Para tal introduzimos os dados recolhidos em [CVE Mitre](https://cve.mitre.org/) da seguinte forma:


![Input em CVE Mitra](resources/CTF4/cveInputList.png)

Obtendo:

![CVEs encontrados](resources/CTF4/cveResult.png)

Com base nos CVEs encontrados, optamos por analisar o **CVE-2014-6278**, uma vez que foi a tentativa falhada/incompleta mais recente para a vulnerabilidade descrita.

Esta consiste num parse mal executado nas definições das funções dos valores das variáveis de ambiente, o que permite atacar remotamente, através de um ambiente alterado/construído, permitindo a execução de qualquer comando malicioso.

## Procura pela Flag

Com base nos conhecimentos adquiridos com a resolução do **LOGBOOK4** apercebemo-nos que, como o input do utilizador é imediatamente adicionado ao comando `ls` seria possível encadear outro comando com a utilização de `&&` ou `;`.

Como já sabiamos a localização da flag, foi simples ver o seu conteúdo:

![metodo 1](resources/CTF4/getflag1.png)
![metodo 2](resources/CTF4/getflag2.png)

![resultado](resources/CTF4/flagResult.png)

Concluímos assim que o valor da flag: `flag{C0aVBzSKTzm7UDwLLLvLxz04TMMSj1}`


