# CTF Semana 10 (Classical Encryption)

## Contextualização

O desafio de CTF desta semana consiste em aplicar os conceitos sobre esquemas de cifração clássicos. O foco será explorar a previsibilidade das frequências de letras, considerando o conhecimento prévio da linguagem em que o texto original foi escrito.

## Tarefas

**Como é que a cifra em questão pode estar a cifrar os dados?**: Como nos é dito no enunciado foi utilizada o método de cifração clássica, que consiste na transformação de todas as letras para minúscula, a remoção de todos os tipos de pontuação e espaços entre palavras. Por fim, mapeam para cada uma das letras um símbolo correspondente.


**Qual metodologia será utilizada para a decifração**: De modo a termos sucesso na decifração do conteúdo escondido, vamos avaliar a frequência de cada símbolo e os seus `n-gramas` correspondentes. Além disso, para utilizarmos corretamente a informação previemente referida temos de procurar pela frequência de cada um das letras, encriptadas, e a sua respectiva língua, sendo neste caso português. Utilizamos também a [wikipédia frequência letras português](https://pt.wikipedia.org/wiki/Frequ%C3%AAncia_de_letras), para nos ajudar na decisão de cada componente. 


## Execução da decifração

Passando agora para a parte prática, primeiramente vamos executar o script, [freq.py](resources/CTF10/freq.py) , que vai revelar as frequências dos símbolos, de modo a tentar perceber a letra por de trás do símbolo.

_N-grams_ obtidos: [frequência 1 letra](resources/CTF10/1-gram-(top-20).txt), [frequência 2 letra](resources/CTF10/2-gram-(top-20).txt), [frequência 3 letra](resources/CTF10/3-gram-(top-20).txt).

Agora a ideia será procurar por sequências que se repetem de forma a objetivar e solidificar a certeza da escolha da letra correspondente ao símbolo.

Sendo assim, decidimos pegar na sequência de símbolos `-=~;~%#)*#->|*%;+=`, visto que era a maior sequência que ocorria duas vezes no texto. Como tal, fomos testando com base na ocurrência de cada símbolo. A partir da frequência das letras em português, fomos fazendo palpites até, eventualmente, chegarmos à frase `dosistemaeducativo`. Havendo agora algo com que nós nos conseguissemos segurar, facilmente descobrimos o resto da encriptação.

Símbolos únicos: `[~(*&.!,;=-)]%|#:+?@>_`

Chave de mapeamento: `zsparnbxiodmltcegvhjuf`

Comando para desencriptação: `sed 'y/[~(*&.!,;=-)]%|#:+?@>_/zsparnbxiodmltcegvhjuf/' L02G02.cph > output.txt`

Resultado final: [output.txt](resources/CTF10/output.txt) 

Como tal conseguimos com sucesso obter a `flag{amxgvrmremgszthb}`.

