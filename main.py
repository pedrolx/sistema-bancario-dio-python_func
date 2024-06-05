def exibir_menu():
    nome = " PyBank "
    menu = f"""
    {nome.center(25, "-")}
    [d] - Depositar 
    [s] - Sacar
    [e] - Extrato
    [nc] - Nova Conta
    [nu] - Novo Usuario
    [q] - Sair
    {"".center(25, "-")}
    """
    return menu

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= limite_saques

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"Valor sacado. Você ainda pode fazer {limite_saques - numero_saques} saques hoje.")
        else:
            print("Operação falhou! O valor informado é inválido.")
        
        return saldo, extrato 

def deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def extrato(saldo, /, *, extrato):
        print(f"\n{' Extrato '.center(25, '-')}")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print(f"\n{''.center(25, '-')}")

def filtrar_usuario(cpf, usuarios):
    usuario_filtrado = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somenten número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe um usuário cadastrado com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(f"Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): ")

    usuarios.append({ "nome": nome, "data_nascimento": data_nascimento, 
                     "cpf": cpf, "endereco": endereco })
    
    print("Usuário registrado!".center("-", 20))

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso!")
        return { "agencia": agencia, "numero_conta": numero_conta, "usuario": usuario }
    
    print("Usuário não encontrado!")

def listar_contas(contas):
    for conta in contas:
        info = f"""
            Agência: { conta["agencia"] }
            Conta: { conta["numero_conta"] }
            Titular: { conta["usuario"]["nome"] }
            """
        
        print(" Lista de Contas ".center("-", 20))
        print(info)
        print("".center("-", 20))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = input(exibir_menu())

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = deposito(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque:"))
            saldo, extrato = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()