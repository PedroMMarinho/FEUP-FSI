
# Trabalho realizado na Semana #4

## Task 1: Manipulating Environment Variables

- **Use printenv/env**: Como podemos verificar ao utilizar o comando printenv ou env, de facto, mostra-nos no terminal todas as variáveis de ambiente.

- **Use export/unset**: Como indicado, utilizamos os dois comandos e conseguimos definir novas variáveis de ambiente com um valor específico,assim como remover variáveis já existentes:

```bash
seed@VM:~$ printenv test
seed@VM:~$ export test=testValue
seed@VM:~$ printenv test
testValue
seed@VM:~$ unset test
seed@VM:~$ printenv test
seed@VM:~$ 
```

## Task 2: Passing Environment Variables from Parent Process to Child Process

- Após correr o código indicado verificamos que de facto não existia nenhuma diferença entre as variáveis de ambiente do processo filho e do processo pai. Desta forma podemos concluir que o processo filho, criado a partir da função `fork`, herda todas as variáveis de ambiente.

## Task 3: Environment Variables and `execve()`

Answering the question "are environment variables automatically inherited by the new program?"

- Não. Quando corremos o programa com o terceiro parâmetro de `execve` (`envp`) como `NULL` o ambiente do novo programa vai ser vazio.

- Como foi esclarecido no `man execve`: envp é um array de strings, com o formato convencional **key=value**, que são passadas como um ambiente para o novo programa. The argv and envp arrays must each include a null pointer at the end of the array.

- So, the new program environment variables need to be passed in the `envp` argument of `execve`. To achieve that, the use of `environ` is convinient since it points to an array of pointers to strings called the "environment", which stores the value of each environmental variables. 

- One of this variables changes, the `_` variable. This is normal because this variable holds the last argument of the previous command.  

## Task 4: Environment Variables and `system()`

- Depois de corrermos o código fornecido verificamos, através da comparação com as variáveis de ambiente antes da execução do mesmo, que de facto estas se mantêm (apesar de não necessáriamente com a mesma ordem)

## Task 5: Environment Variable and Set-UID Programs

- Com a execução passos referidos conseguimos perceber que nem todas a variáveis de ambiente no processo pai são transferidas para o processo `SET-UID` filho.

- De facto, este é um processo natural. As variáveis de ambiente mais cruciais, como `LD_LIBRARY_PATH` (aquelas que se maliciosamente alteradas teriam facilmente um impacto negativo) são filtradas ou alteradas de formas a proteger o sistema.

- Estranhamente `PATH` não apresenta o mesmo tipo de cuidado que `LD_LIBRARY_PATH` o que pode se mostrar uma vulnerabilidade

