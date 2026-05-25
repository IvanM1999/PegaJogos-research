# 🛠️ Manual de Recuperação: Fazendo o PegaJogo.exe Voltar à Vida

Este manual descreve os passos necessários para contornar as falhas de scripts e dependências, permitindo a execução do PegaJogo em ambientes modernos ou controlados.

---

## 1. Preparação do Ambiente
Para evitar conflitos com o Windows 10/11, é altamente recomendável o uso de uma **Máquina Virtual (VM)**:
- **SO:** Windows XP SP3 ou Windows 7 32-bits.
- **Rede:** Desativada inicialmente (Modo Host-only).

## 2. Configuração do Banco de Dados (Firebird)
O PegaJogo não abrirá se não conseguir consultar o banco de dados.
1. Instale o **Firebird 2.0 (32-bit)**.
2. Localize o arquivo de banco de dados (geralmente `.fdb` ou `.gdb`) e coloque-o na pasta esperada pelo app.
3. **Vital:** Copie a biblioteca de funções customizadas:
   - Origem: `bin/udf/fbudf.dll`
   - Destino: `C:\Arquivos de Programas\Firebird\Firebird_2_0\UDF\`

## 3. Contornando o Bloqueio do Flash Player
Sem o Flash, a interface de navegação ficará em branco.
1. Desinstale qualquer versão moderna do Flash Player.
2. Instale o **Adobe Flash Player ActiveX 10.3 ou 11.7** (versões anteriores ao "Kill Switch" de 2021).
3. Se o Windows bloquear a instalação, utilize o **BlueMaxima's Flashpatch** ou altere a data do sistema para antes de 2020 (apenas para teste rápido).

## 4. Registro de Componentes (OCX/DLL)
O PegaJogo utiliza bibliotecas de interface que precisam ser registradas no registro do Windows. Abra o Prompt de Comando como **Administrador** e execute:

```cmd
cd C:\Caminho\Para\PegaJogo\bin
regsvr32.exe flash.ocx
regsvr32.exe mscomctl.ocx
regsvr32.exe mswinsck.ocx
```
*Nota: Se faltar a `MSVBVM60.DLL`, você precisará instalar o Runtime do Visual Basic 6.*

## 5. Simulação de Rede (DNS Mock)
Para evitar que o app trave tentando conectar ao servidor original que não existe mais:
1. Abra o arquivo de hosts: `C:\Windows\System32\drivers\etc\hosts`.
2. Adicione a seguinte linha para redirecionar o tráfego para sua própria máquina:
   ```text
   127.0.0.1  pegajogo.com.br
   127.0.0.1  www.pegajogo.com.br
   ```
3. (Opcional) Suba um servidor local (Python ou Node) na porta 80 para observar as requisições que o app tenta fazer.

## 6. Verificação de Execução
Após seguir os passos, execute o `PegaJogo.exe`. Se a navegação ainda falhar:
1. Use o **Process Monitor (ProcMon)** para ver se o executável está tentando ler um arquivo em um caminho que não existe (ex: `D:\` ou `C:\Games`).
2. Verifique se o processo `fbserver.exe` (Firebird) está ativo e consumindo o arquivo de banco.

---

## Resumo de Comandos Rápidos
| Problema | Solução |
| :--- | :--- |
| Tela Branca | Instalar Flash ActiveX antigo |
| Erro de DLL | `regsvr32` nos arquivos da pasta `bin` |
| App Congelado | Configurar o arquivo `hosts` |