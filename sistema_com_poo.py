from abc import ABC, abstractmethod 
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("\n Operação falhou! Você naõ tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("\n Saque realizado com sucesso!")
            return True
        else:
            print("\n Operação falhou! O valor informado não é válido.")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n Depósito realizado com sucesso!")
        else:
            print("\n Operação falhou! O valor informado é inválido.")
            return False
        
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes 
            if transacao["tipo"] == Saque.__name__]
        )
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques
        
        if excedeu_limite:
            print("\n Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("\n Operação falhou! Limite de saques diários excedido.")
        else:
            return super().sacar(valor) 
        
        return False
    
    def __str__(self):
        return f"""
            Agência: {self.agencia}
            C/C: {self.numero}
            Titular: {self.cliente.nome}
        """
        
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            { 
             "tipo": transacao.__class__.__name__,
             "valor": transacao.valor,
             "data": datetime.now().strtime("%d-%m-%Y %H:%M:%s")
            }
        )
        
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            
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
    return input(menu)

def main():
    clientes = []
    contas = []

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            deposito(clientes)

        elif opcao == "s":
            saque(clientes)

        elif opcao == "e":
            extrato(clientes)

        elif opcao == "nu":
            criar_usuario(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

def saque(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuario(cpf, clientes)     
    
       

def deposito(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuario(cpf, clientes)
    
    if not cliente:
        print("\n Cliente não encontrado!")
        return
    
    valor = float(input("\n Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def extrato(saldo, /, *, extrato):
        print(f"\n{' Extrato '.center(25, '-')}")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print(f"\n{''.center(25, '-')}")

def filtrar_usuario(cpf, usuarios):
    usuario_filtrado = [usuario for usuario in usuarios if usuario.cpf == cpf]
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
    
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Cliente não possui conta!")
        return
    return cliente.contas[0]