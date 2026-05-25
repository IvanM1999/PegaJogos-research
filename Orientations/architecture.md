# 🏗️ Arquitetura e Esqueleto do PegaJogo

Abaixo está o levantamento técnico baseado nos artefatos encontrados até agora:

### 1. Front-end (Interface do Usuário)
- **Tecnologia:** Provavelmente **Visual Basic 6.0** (VB6).
- **Evidência:** Linker Version 6.0 e o uso intensivo de componentes COM/ActiveX (comum para integrar Flash na época).
- **Dependências Críticas:** 
    - `Flash.ocx` (ActiveX do Adobe Flash Player).
    - `MSVBVM60.DLL` (Runtime do Visual Basic).

### 2. Back-end (Banco de Dados)
- **Motor:** **Firebird SQL** (Provavelmente versão 1.5 ou 2.0).
- **Extensões (UDFs):** O arquivo `fbudf.txt` confirma que o sistema utiliza funções customizadas para manipular strings e datas (`NVL`, `DOW`, `STRING2BLOB`). Sem essas DLLs de UDF na pasta do servidor Firebird, o banco de dados pode não abrir ou disparar erros em queries.
- **Conexão:** Utiliza **ODBC** ou conexão direta via `fbclient.dll` / `gds32.dll`.

### 3. Integração de Conteúdo
- **Jogos Flash (.swf):** Eram carregados dentro do binário principal através de um wrapper.
- **Executáveis (.exe):** O PegaJogo agia como um "Shell Execution", disparando processos externos para jogos que não eram em Flash.

### 4. Fluxo de Dados
1. **Inicialização:** O binário verifica a presença do banco local (`.fdb` ou `.gdb`).
2. **Autenticação/Sync:** Se houver internet, tenta conexão com o servidor central (originalmente `pegajogo.com.br`).
3. **Exibição:** Lê a tabela de categorias e jogos do banco Firebird e renderiza a lista.
4. **Execução:** Copia o arquivo do jogo para uma pasta temporária e o executa.

### 🔬 Desafio da Engenharia Reversa
O `PegaJogo.exe` possui apenas **1 importação DLL** visível nos cabeçalhos PE, o que é um forte indício de que o executável está **compactado (Packed)**. 
- **Ação necessária:** Identificar se o packer é UPX ou um customizado (como MoleBox ou Aspack) para "descompactar" e ver as chamadas reais de API.

---
*Orientação gerada para o projeto PegaJogos-research.*