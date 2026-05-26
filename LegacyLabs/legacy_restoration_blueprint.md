# 🧪 LegacyLabs: Blueprint para Restauração do Binário Original

Este documento detalha o plano técnico para estabilizar o aplicativo original (`PegaJogo.exe`) e modernizar sua distribuição através de um novo instalador.

## 1. Reaproveitamento da Infraestrutura Legada
Para manter a fidelidade e evitar a reescrita total da lógica de negócio, aproveitaremos:
- **Database Engine:** O arquivo `.fdb` (Firebird) continuará sendo o repositório central de metadados.
- **Hierarquia de Assets:** Manteremos a estrutura de pastas `Games/[Categoria]/[Jogo].swf` para garantir que as queries SQL internas do binário não precisem ser alteradas.
- **Componentes COM:** Utilizaremos as OCXs originais, mas com um processo de registro automatizado e resiliente.

## 2. Destrinchando a Arquitetura para o "Conserto"
Para "consertar" o app sem o código-fonte original, focaremos em três frentes de intercepção:

### A. Otimização do Banco de Dados (Zero-Config)
- **Firebird Embedded:** A meta é substituir o servidor Firebird instalado pelo `fbembed.dll` (renomeado para `fbclient.dll`). Isso permite que o app acesse os dados localmente sem que o usuário precise instalar um serviço de banco de dados.
- **UDF Deployment:** O novo instalador garantirá que a `fbudf.dll` esteja na subpasta correta, resolvendo o erro de "Function Unknown" que trava o menu.

### B. Bypass de Rede e DNS
- **Fake Internet:** O `NewServer` (Node.js) será configurado para responder como `pegajogo.com.br`. 
- **Descongelamento da UI:** Ao interceptar as chamadas `.php` e retornar um status 200 (ou o conteúdo esperado), o binário VB6 sairá do estado de "congelado" imediatamente após o boot.

### C. Patch de Compatibilidade Flash
- **ActiveX Wrapper:** Testar o uso do `Ruffle` como um substituto direto para a `Flash.ocx` via redirecionamento de chamadas COM, ou distribuir o ActiveX "unlocked" (versão 11.7 ou inferior) para contornar o Kill-Switch.

## 3. O Novo Instalador (Tecnologia Moderna)
O instalador original será substituído por um script de implantação robusto, possivelmente usando **Inno Setup** ou **NSIS**.

### Funcionalidades do Novo Pacote:
1. **Bootstrap de Runtimes:** Instalação automática do Runtime do VB6 (`MSVBVM60.DLL`).
2. **Registro Silencioso:** Execução de `regsvr32 /s` para todos os componentes na pasta `bin/`.
3. **Ajuste de Hosts:** Automação (com elevação de privilégio) para adicionar o redirecionamento de DNS local durante a instalação.
4. **Portabilidade:** Criação de um ambiente "Sandboxed" onde o app encontra todas as suas DLLs na própria pasta raiz, evitando conflitos com o `System32`.

Próximos Experimentos (Laboratório)
- [x] **Análise de Binário:** Confirmado que o `PegaJogo.exe` é um binário VB6 nativo e não está compactado. (Ver binary_analysis_pega_jogo.md)
- [ ] **Extração de Strings:** Localizar URLs e caminhos de banco de dados fixos no binário.
- [ ] **Embedded Firebird Proof-of-Concept:** Tentar rodar o binário apontando para um cliente Firebird embutido.
- [ ] **Mock de XML de Sincronização:** Capturar o formato exato que o app espera para atualizar a lista de jogos via rede.

---
*Este documento é uma peça de trabalho viva do LegacyLabs.*