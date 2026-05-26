# 📑 Resumo Executivo: PegaJogos-research

## 1. Visão Geral
Este projeto visa a preservação e restauração do ecossistema **PegaJogo**, uma plataforma brasileira de distribuição de jogos dos anos 2000. O objetivo é permitir que o acervo de jogos Flash e a experiência do usuário original sejam acessíveis em hardware e sistemas operacionais modernos.

## 2. O Aplicativo Original (Legacy)
A análise técnica revelou que o `PegaJogo.exe` original é um cliente **Visual Basic 6.0** que opera sob as seguintes condições:
- **Banco de Dados:** Utiliza **Firebird SQL (v1.5/2.0)** com dependência de funções customizadas (**UDFs**) como `fbudf.dll`.
- **Motor de Renderização:** Depende do componente ActiveX **Adobe Flash Player**, que possui um bloqueio de execução (Kill-Switch) desde 2021.
- **Rede:** Realiza chamadas síncronas para `pegajogo.com.br` via scripts `.php`, o que causa travamentos (freezes) em ambientes onde o domínio original não responde.

## 3. Infraestrutura de Restauração (New Server)
Para contornar as limitações do software legado, desenvolvemos o ambiente **NewServer**, focado em **Node.js**:

### Componentes Principais:
- **Servidor (server.js):** Um back-end Express que serve os arquivos do site, configura tipos MIME específicos para WebAssembly (`.wasm`) e emula as rotas `.php` antigas para suporte a modo legado.
- **Gerador de Catálogo (generate_games.js):** Script Node.js que escaneia a pasta de jogos original (`Reference-Flash`) e reconstrói automaticamente o banco de dados em formato JSON.
- **Automação (start_pega_jogo.bat):** Script de inicialização que verifica dependências, instala pacotes via `npm` e sobe o servidor com auto-recuperação.
- **Emulação (Ruffle):** Integração do emulador Ruffle para rodar os arquivos `.swf` sem necessidade do Flash Player original instalado no sistema.

## 4. Estratégias de Preservação
Identificamos duas rotas distintas para o projeto:

| Estratégia | Método | Estágio |
| :--- | :--- | :--- |
| **Revivificação** | Patching do `.exe` original em VMs (Windows XP/7). | Documentado |
| **Reconstrução** | Criação de um novo Launcher moderno usando Node.js/HTML5. | Em desenvolvimento |

## 5. Progresso Atual
- [x] Mapeamento de dependências OCX/DLL do binário original.
- [x] Identificação da lógica de UDFs do Firebird.
- [x] Implementação do servidor de arquivos e mock de API em Node.js.
- [x] Automação completa do ambiente de desenvolvimento local.
- [x] Migração de scripts de suporte de Python para Node.js (unificação de stack).

## 6. Próximos Passos
1. **Interface Visual:** Desenvolver um front-end que replique a estética clássica do PegaJogo.
2. **Migração de Dados:** Finalizar a extração de metadados dos arquivos `.fdb` remanescentes para o catálogo JSON.
3. **Portabilidade:** Empacotar o `NewServer` como um executável único para facilitar o acesso de usuários leigos.

---
*Documento atualizado em: 2024*
*PegaJogos-research - Preservando a história do software nacional.*