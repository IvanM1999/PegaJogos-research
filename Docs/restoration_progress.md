# 🛠️ Registro de Restauração - PegaJogo "New Server"

Este documento descreve as decisões técnicas e etapas tomadas para a ressurreição funcional do ecossistema PegaJogo dentro do diretório `/new server`.

## 📋 Etapas Executadas

### 1. Preservação de Artefatos (Arquivamento)
- Os arquivos recuperados do WebArchive em `datashared/` foram mantidos em seu estado bruto. Nenhuma alteração de banner ou script foi feita neles para garantir a integridade da fonte original.

### 2. Engenharia Reversa e Dissecação (Novo)
- **Análise de Binário:** Confirmado que o `PegaJogo.exe` é um app VB6 compactado.
- **Identificação de Dependências:** Mapeado o uso de `fbudf.dll` no Firebird e componentes OCX para interface.

### 3. Criação do Ambiente "New Server"
- Localizado em `/new server`, este ambiente atua como o novo host para a experiência de jogo.
- Toda a lógica de carregamento foi centralizada no arquivo `index.html` dentro desta pasta.

### 3. Integração do Emulador Flash (Framework Ruffle)
- **Decisão:** Selecionado o **Ruffle** como framework de interpretação.
- **Motivo:** O Flash Player original possui uma "bomba-relógio" de software que impede a execução de SWFs desde 2021. O Ruffle permite a execução via WebAssembly com segurança e performance moderna.
- **Implementação:** O script é carregado localmente a partir dos recursos recuperados.

### 4. Importação e Mapeamento de Dados
- Os nomes de arquivos `.swf` e metadados (como títulos e categorias) foram extraídos visualmente dos bancos de dados recuperados (`recuperado.html` e `index.html` originais).
- A estrutura de diretórios de jogos (`datashared/Pega jogos/Games/`) foi mapeada via caminhos relativos para garantir que o "New Server" consiga carregar os binários sem modificar a pasta de origem.

### 5. Contorno de Scripts de Navegação Legados
- Substituímos a dependência do Internet Explorer/ActiveX (VB6) por uma interface HTML5/JavaScript responsiva que replica o "look and feel" do PegaJogo clássico.
- **Descoberta Crítica:** Identificamos que a falha de carregamento no executável original em VMs modernas deve-se à ausência da `fbudf.dll` no diretório `/UDF` do Firebird, impedindo a execução de funções como `NVL` e `DOW` nas queries de montagem do menu.

### 6. Automação e Servidor de Restauração (New Server)
- **Script de Inicialização:** Criado o `start_pega_jogo.bat` para verificar a presença do Node.js e instalar bibliotecas automaticamente.
- **Back-end Node.js:** Implementado `server.js` usando Express para servir o site e emular comportamentos de rede antigos (como interceptar chamadas `.php`).
- **Gerador de Catálogo:** Script Node.js `generate_games.js` para escanear a pasta de jogos original e atualizar o banco de dados JSON do site em tempo real.

## 🚀 Como usar o New Server
1. Execute o arquivo `start_pega_jogo.bat` na pasta `NewServer`.
2. Aguarde a instalação automática do Node e a geração do catálogo.
3. O servidor subirá em `http://localhost:3000`.
4. Selecione um jogo na interface e o Ruffle iniciará a emulação.

---
*Documentação gerada pelo Assistente de Código para PegaJogos-research.*