# Trabalho realizado na Semana #7

## Questão 1
### Configuração básica

- De forma a tornar este lab possível, temos de adicionar as entradas indicadas pelo guião, no ficheiro `/etc/hosts/`, utilizando o comando `nano`, por exemplo, a partir da root.

![xss lab websites](resources/LOGBOOK7/xss_websites.png)   

- Seguidamente, após o download do _zip_ deste lab, corremos os comandos `dcbuild` e `dcup` de forma a executarmos os containers de docker.

Desta forma, conseguimos ter acesso à pagina `www.seed-server.com`:

![Elgg webpage](resources/LOGBOOK7/elgg_webpage.png)

De forma a testarmos os ataques, também nos é fornecido os utilizadores e as suas respectivas _passwords_ desta webpage.

| UserName | Password    |
|----------|-------------|
| admin    | seedelgg    |
| alice    | seedalice   |
| boby     | seedboby    |
| charlie  | seedcharlie |
| samy     | seedsamy    |


### Tarefa 1 : Posting a Malicious Message to Display an Alert Window

- Como referido no título desta tarefa, o nosso objectivo é conseguirmos executar um script a mostrar uma mensagem maliciosa. Para isso, podemos inserir o seguinte código malicoso, `<script>alert('XSS');</script>`, num dos `forms` do nosso utilizador.

![message script gif](resources/LOGBOOK7/message_script.gif)

Neste caso inserimos o **script malicioso** no perfil da **alice**, na secção _brief description_, e realmente verificamos que para qualquer utilizador, esta mensagem será mostrada.


### Tarefa 2 :  Posting a Malicious Message to Display Cookies

- Tal como na task anterior,o nosso objectivo é mostrar uma mensagem, mas neste caso com as cookies do utilizador. Para tal, inserimos o script malicioso `<script>alert(document.cookie);</script>`, num dos `forms` do nosso utilizador.

![cookie message gif](resources/LOGBOOK7/cookie_message.gif)


Da mesmo maneira que demos _display_ da mensagem `XSS`, agora aparecem as cookies do utilizador _logado_ ao aceder ao perfil da alice.


### Tarefa 3: Stealing Cookies from the Victim’s Machine

