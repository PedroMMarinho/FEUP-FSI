# CTF Semana 3 (WordPress CVE)

## Reconhecimento

- **Versão do wordpress**: Pensamento inicial, verificar no código html da página web informação pertinente (ctrl+shift+i). Foi encontrado através da keyword "generator" as versões do WordPress e do plugin Woocommerce sendo elas 5.8.1 e 5.7.1, respectivamente.![htmlGenerator png](resources\CTF3\htmlGenerator.png)
 
- **Plugins instalados e versões dos mesmos**: Tal como foi referido no tópico acima foi encontrado o plugin Woocommerce através da inspeção do website. Sentimos que estavamos num bom caminho, no entanto, ainda nos faltava algo. Foi daí que ao explorar melhor as janelas da web encontramos na tab "Additional information" do item "WordPress Hosting" toda a informação acerca das versões!
![versions png](resources\CTF3\versions.png)
  
- **Possíveis utilizadores e nomes de utilizadores**: No que toca aos utilizadores deste sistema, deparamo-nos com dois comentários, o comentário do user "Orval Sanford" e o do "admin". Com base nesta informação, deduzimos que talvez seria possível infiltramo-nos na conta de um destes users.
![users png](resources\CTF3\users.png)


## Pesquisa por Vulnerabilidades

- **Procura de CVE's**: Após a recolha de informação passamos à fase de procura de CVE's. Primeiramente, focamo-nos em procurar nos sites recomendados do "Guião da Semana #2", onde fomos ao encontro de exploits que foram encontrados e ainda funcionam nas versões do WordPress, Woocommerce, Booster e MStore API referidas na imagem acima.

## Escolha da Vulnerabilidade

- **Identificação de CVE's**: Durante esta pesquisa estavamos indecisos entre dois CVE's, selecionamos o CVE-2022-21661, que resulta de uma gestão inadequada de consultas em WP_Query, o que pode permitir uma SQL injection através de plugins ou temas no WordPress. Para além deste, selecionamos o CVE-2023-2732, que permite a atacantes não autenticados fazer login como qualquer utilizador, inclusive administradores, devido à verificação insuficiente no pedido REST de adição de listagem no plugin MStore API.

<details>
  <summary><i>Spoiler<i></summary>
  O CVE-2023-2732 é o correto.
</details>


## Encontrar um exploit

- **Fonte de exploits**: Com os CVE's já identificados, só nos faltava encontrar os scripts desses exploits na internet. Optamos por escolher o github como ferramenta para a seleção de código previamente feito. Para cada um dos CVE's escolhidos encontramos os repositórios [CVE-2022-21661](https://github.com/sealldeveloper/CVE-2022-21661-PoC?tab=readme-ov-file) e [CVE-2023-2732](https://github.com/RandomRobbieBF/CVE-2023-2732).


## Explorar a vulnerabilidade

- **Execução de scripts**: Este passo foi relativamente simples. Após identificados os exploits, bastou seguir a documentação explicita sobre cada um e executar os passos indicados. Os resultados foram os seguintes:


**CVE-2022-21661**

![CVE-2022-21661 exploit](resources\CTF3\CVE-2022-21661_exploit.png)

**CVE-2023-2732**

<video controls src="resources\CTF3\CVE-2023-2732_exploit.mp4" title="Title"></video>

- Apenas o exploit da vulnerabilidade CVE-2023-2732 funcionou. Este permitiu identificar o admin como um utilizador válido e aceder indevidamente à sua conta. Assim conseguimos aceder a todas a funcionalidades previamente inacessiveis, nomeadamente às mensagens privadas, onde encontra-mos a flag final deste CTF.

## Referências

[^1]: (nome do website)[website]