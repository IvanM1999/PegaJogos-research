# 🔍 Análise de Binário: PegaJogo.exe (Core App)

Este documento detalha as especificações técnicas do executável principal após a extração do instalador.

## 1. Perfil Técnico
- **Linguagem:** Visual Basic 6.0 (VB6).
- **Arquitetura:** x86 (32-bit) PE32.
- **Tipo de Compilação:** **Native Code** (Código Nativo). 
    - *Evidência:* Presença de funções de ponto flutuante como `_adj_fdiv_m64` e `_adj_fpatan`.
- **Estado de Empacotamento:** **Unpacked** (Não compactado).
    - *Observação:* Diferente do instalador, o executável principal possui seções padrão (`.text`, `.data`, `.rsrc`) e a tabela de importação está totalmente visível.

## 2. Dependências de Runtime
- **Core:** `MSVBVM60.DLL` (Runtime do Visual Basic).
- **Indirect Dependencies:** O binário utiliza chamadas COM/ActiveX para carregar os componentes de interface e banco de dados que devem estar presentes na pasta `bin` ou registrados no sistema:
    - `flash.ocx` (Renderização de jogos).
    - `mscomctl.ocx` (Interface de árvore/lista).
    - `mswinsck.ocx` (Comunicação de rede).

## 3. Pontos de Intervenção para "Conserto"
Como o binário não está compactado, as seguintes strings podem ser localizadas via editor hexadecimal ou ferramenta de `strings`:

- **Banco de Dados:** Procurar por caminhos de arquivo `.fdb` ou strings de conexão Firebird. 
- **URLs de Rede:** Mapear os endereços de `pegajogo.com.br` para redirecionamento via `hosts` ou interceptação no `NewServer`.
- **Lógica SQL:** Identificar as queries enviadas ao Firebird para verificar a compatibilidade com as UDFs (`fbudf.dll`).

## 4. Conclusão do Experimento
O fato de o executável ser VB6 Nativo e não estar compactado é uma excelente notícia. Isso significa que podemos realizar patches binários (Hex Editing) diretamente para alterar URLs de servidor ou caminhos de banco de dados, se necessário, sem lidar com algoritmos complexos de descompressão.

---
*Laboratório de Arqueologia Digital - LegacyLabs*