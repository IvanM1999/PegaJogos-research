# 🏗️ Arquitetura e Esqueleto do PegaJogo
**Status: Em Reconstrução (Fase de Análise Técnica)**

Abaixo está o levantamento técnico baseado nos artefatos encontrados até agora:

### 1. Front-end (Interface do Usuário)
- **Tecnologia:** Provavelmente **Visual Basic 6.0** (VB6).
- **Evidência:** Linker Version 6.0 e o uso intensivo de componentes COM/ActiveX (comum para integrar Flash na época).
- **Dependências Críticas:** 
    - `Flash.ocx` (ActiveX do Adobe Flash Player).
    - `MSVBVM60.DLL` (Runtime do Visual Basic).
    - `mscomctl.ocx` e `mswinsck.ocx`: Usados para a interface de árvore (categorias) e comunicação de rede.

### 2. Back-end (Banco de Dados)
- **Motor:** **Firebird SQL** (Provavelmente versão 1.5 ou 2.0).
- **Lógica Interna:** Dependência pesada de UDFs (`fbudf.dll`) para manipulação de strings e datas diretamente nas queries.
- **Conexão:** Utiliza **ODBC** ou conexão direta via `fbclient.dll` / `gds32.dll`.

### 3. Integração de Conteúdo
- **Jogos Flash (.swf):** Eram carregados dentro do binário principal através de um wrapper.
- **Executáveis (.exe):** O PegaJogo agia como um "Shell Execution", disparando processos externos para jogos que não eram em Flash.

### 4. Fluxo de Dados
1. **Boot:** O `PegaJogo.exe` carrega o runtime do VB6 e tenta registrar/carregar os componentes OCX na memória.
2. **Verificação de Integridade:** Checa se o Firebird está rodando e se as UDFs estão acessíveis. Se as UDFs falharem, o menu de categorias não aparece.
3. **Handshake de Rede:** Tenta uma conexão TCP (Socket) com `pegajogo.com.br`. O app fica "congelado" (Single-threaded) até o timeout do Windows (aprox. 20-40s) se o site estiver fora do ar.
4. **Sincronização:** O app busca arquivos `.php` remotos que retornam instruções SQL ou novos metadados.
5. **Renderização:** A interface VB6 preenche um controle `TreeView` com as categorias e um `ListView` com os títulos dos jogos.
6. **Lançamento:** Ao clicar, o caminho do arquivo (ex: `Games/acao/jogo.swf`) é passado para o componente ActiveX do Flash.

### 🔬 Desafio da Engenharia Reversa
O executável é um **Wrapper ActiveX**. Ele não contém o código dos jogos, apenas a lógica de "casca" para o banco de dados e o player de Flash. A compactação do binário visa ocultar as URLs de conexão e as queries SQL fixas.

---
*Orientação gerada para o projeto PegaJogos-research.*