# Bank

## Saque

    - [x] Keyword only, apenas por nome
    - Saldo, valor, extrato, limite, numero_saques, limite_saquyes... retorno, saldo e extrato

## Depósito

    - [x] Positional only, apenas por posição
    - Saldo, valor, extrato > retorno saldo e extrato

## Extrato

    - [x] position only e keyword only
        - Saldo, argumentos nomeados: extrato

## Novas funções

    - [x] Criar usuário
        - [x] Usuários em lista: nome, data de nascimento, cpf e endereço
        - [x] Endereço: cep, logradouro, complemento, bairro, localidade, uf
            - Formato: CEP, logradouro, nro - bairro - cidade/uf
        - [x] Deve ser armazenado somente os números do CPF
        - [x] Não pode criar um usuário com o mesmo CPF

    - [x] Criar conta corrente
        - [x] Conta é composta por: agência, número da conta, usuário
        - [x] O número da conta é sequencial, começa em 1
        - [x] A agência é fixa, "0001"
        - [x] O usuário pode ter mais de uma conta, mas uma conta pertence a somente um usuário

> Para vincular um usuário, filtre a lista de usuários buscando o número do CPF informado para cada usuário na lista
