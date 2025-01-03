
# Trabalho realizado nas Semanas #2 e #3

## Identificação

- **Vulnerabilidade**: CVE-2019-14287 é uma falha no comando sudo que dá acesso priveligiado a utilizadores indevidos.[^1]

- **Sistemas Afetados**: Sistemas baseados em Linux/Unix com versões anteriores à 1.8.28.[^2]

## Catalogação 

- **Reporting**: Falha reportada em 2019, por Joe Vennix, um investigador de segurança da empresa Apple, durante uma análise de segurança.[^4]

- **Gravidade**: Alto nível de gravidade, com pontuação CVSS de 9.0 e 8.8, segundo cvedetails.[^3]

- **Bug Bounty**: Não há registos públicos de pagamento por bug bounty.

## Exploit

- **Tipo de Exploit**: Elevação de privilégios, o atacante consegue utilizar um valor de UID inválido para ganhar privilégios de administrador.

- **Bypass da Especificação Runas**: Utilizando os IDs de utilizador -1 ou 4294967295, as restrições configuradas com a palavra-chave ALL seriam ignoradas.

- **Alteração de Registos**: Os logs do sudo mostram o ID 4294967295 em vez de root, dificultando a deteção de atividades maliciosas.

- **Automação**: Existem várias automações que exploram a execução de comandos manipulados com UIDs, no entanto desta vulnerabilidade em específico não há nenhuma.

## Ataques

- **Utilização da vulnerabilidade**: Não existem registos da utilização desta vulnerabilidade, pelo menos publicamente.

- **Potencial de Danos**: Esta é uma vulnerabilidade que apresenta um elevado risco para qualquer sistema afetado.

- **Possíveis Danos**: Alguns possíveis danos são o comprometimento de dados confidenciais, integridade do sistema e manipulação de registos dificultando a deteção de atividades maliciosas. 

## Referências

[^1]:[CVE-2019-14287 - CVEdetails](https://www.cvedetails.com/cve/CVE-2019-14287/)

[^2]:[Sudo Advisory: -1 UID Vulnerability](https://www.sudo.ws/security/advisories/minus_1_uid/#:~:text=This%20vulnerability%20has%20been%20assigned%20CVE-2019-14287%20in%20the%20Common)

[^3]:[NVD Impact Score for CVE-2019-14287](https://nvd.nist.gov/vuln/detail/CVE-2019-14287)

[^4]:[ Apple Researcher Finds Huge Flaw in Linux Sudo Command - Tom's Hardware](https://www.tomshardware.com/news/apple-researcher-finds-huge-flaw-in-linux-sudo-command)