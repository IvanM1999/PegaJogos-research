# 🚀 Roteiro para Reviver o PegaJogo

Para fazer o app voltar à vida, devemos seguir esta ordem de prioridade:

## Fase 1: Operação Offline (O Coração do App)
O objetivo aqui é fazer o binário abrir e listar jogos locais sem depender de servidores.

1. **Ambiente de Desenvolvimento:** 
   - Configure uma Máquina Virtual com **Windows XP SP3** ou **Windows 7 32-bits**.
   - Instale o **Firebird 2.0** (versão de 32 bits).
2. **Restauração do Banco de Dados:**
   - Coloque as DLLs presentes em `bin/udf/` dentro da pasta `UDF` da instalação do Firebird no Windows.
   - Tente conectar ao arquivo `.fdb` usando uma ferramenta como **IBExpert** ou **FlameRobin**.
3. **Correção de Dependências Flash:**
   - Como o Flash Player foi descontinuado, é necessário instalar um "Flash Player ActiveX" antigo ou usar um emulador como o **Ruffle** (embora integrar o Ruffle no binário VB6 original seja complexo).
4. **Mock de Arquivos:** 
   - O app espera encontrar os jogos em um caminho específico (ex: `C:\Arquivos de Programas\PegaJogo\Games`). Precisamos descobrir essa estrutura através dos logs ou strings do binário.

## Fase 2: Engenharia Reversa (Entendendo o Código)
1. **Extração de Strings:** Use ferramentas como `Strings.exe` ou `BinText` no `PegaJogo.exe` para encontrar URLs e comandos SQL fixos.
2. **Análise de Tráfego:** Use o **Wireshark** enquanto abre o app para ver para quais IPs ou Domínios ele tenta "discar".

## Fase 3: Operação Online (Reconstrução da Rede)
Assim que o app funcionar offline, faremos ele "acreditar" que o site oficial voltou.

1. **Redirecionamento de DNS:** Edite o arquivo `hosts` do Windows para apontar o domínio antigo do PegaJogo para o seu `localhost` (127.0.0.1).
2. **Criação do API Mock:** [CONCLUÍDO]
   - Implementado em **Node.js** no `NewServer/server.js` para responder a requisições de arquivos `.php` legados.
   - Geralmente eram arquivos `.php` ou `.xml` que retornavam a lista de novos jogos.
3. **Sincronização de Banco:** Descobrir como o app baixava atualizações do `.fdb` e replicar esse comportamento.
4. **Definição de Estratégia:** [NOVO] Escolher entre manter o binário original ou migrar para o Launcher Moderno (ver `Docs/reconstruction_strategies.md`).

## Fase 4: Modernização (O Novo PegaJogo)
Com o funcionamento entendido, o objetivo final é:
- Criar um novo Launcher em uma linguagem moderna (C#, Electron ou Rust).
- Usar o banco de dados recuperado para alimentar essa nova interface.
- Integrar o **Ruffle** para rodar os jogos Flash diretamente no navegador ou app moderno, sem depender do ActiveX do Windows.

---
*Instruções para os arqueólogos digitais do projeto.*