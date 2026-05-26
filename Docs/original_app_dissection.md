# 🕵️ Dissecação Técnica: PegaJogo Original (Legacy)

Este documento detalha o funcionamento interno do aplicativo PegaJogo original, servindo como base para a engenharia reversa e para o desenvolvimento do "New Server".

## 1. Anatomia do Binário (`PegaJogo.exe`)
- **Linguagem:** Visual Basic 6.0 (VB6).
- **Estado do Executável:** **Packed (Compactado)**. O binário apresenta apenas uma importação de DLL (`KERNEL32.dll`), o que indica o uso de um compressor/proteção como UPX, MoleBox ou Aspack.
- **Runtime:** Depende estritamente da `MSVBVM60.DLL`.
- **Comportamento de Interface:** Utiliza controles ActiveX para renderizar a árvore de categorias (`mscomctl.ocx`) e a comunicação de rede (`mswinsck.ocx`).

## 2. O Motor de Dados (Firebird SQL)
O aplicativo não é autônomo; ele é um cliente que consome um banco de dados **Firebird (v1.5/2.0)**.

### Dependência Crítica: UDF (User Defined Functions)
Diferente de bancos de dados simples, o PegaJogo delegava lógica de tratamento de dados para o motor SQL através da `fbudf.dll`.
- **Funções Identificadas:**
    - `NVL(valor, substituto)`: Usado para evitar erros de interface quando campos de descrição de jogos estavam vazios.
    - `DOW(data)`: Extrai o dia da semana, possivelmente para rotinas de "Jogo do Dia".
    - `STRING2BLOB`: Usada no processo de sincronização de rede para converter dados recebidos em objetos de armazenamento.
**Falha Comum:** Se essas UDFs não estiverem na pasta `/UDF` do servidor Firebird, o menu de categorias nunca será carregado.

## 3. Fluxo de Execução e Gargalos

### A. Sequência de Boot
1. O app carrega as OCXs de interface.
2. Tenta abrir uma conexão via socket com `pegajogo.com.br`.
3. **Problema de Concorrência:** Por ser VB6 (single-threaded), o app "congela" enquanto aguarda o timeout do Windows (até 45 segundos) se o domínio não responder.

### B. Sincronização de Conteúdo
O app verificava atualizações via scripts PHP remotos:
- Chamava arquivos como `get_news.php` ou `sync_db.php`.
- O retorno desses scripts era processado e injetado no banco `.fdb` local via comandos `INSERT/UPDATE`.

### C. Lançamento de Jogos
1. O app consulta o caminho do arquivo no banco de dados (Ex: `Games\Acao\jogo.swf`).
2. O arquivo é carregado no componente ActiveX `Flash.ocx`.
3. **O Bloqueio (Kill-Switch):** Versões modernas do componente Flash impedem a execução após 2021. O app original não tem tratamento para o fim do suporte ao Flash.

## 4. Estrutura de Diretórios Esperada
Para o app funcionar sem erros de "Arquivo não encontrado", ele espera:
```text
/PegaJogo
  ├── PegaJogo.exe
  ├── /bin (DLLs e OCXs)
  ├── /Games (Arquivos .swf categorizados)
  └── /DB (O arquivo .fdb ou .gdb)
```

---
*Documentação técnica de referência para o projeto PegaJogos-research.*