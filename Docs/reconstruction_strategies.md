# 🏗️ Estratégias de Reconstrução e Emulação

Este documento avalia as viabilidades técnicas de reaproveitar a estrutura original do PegaJogo ou migrar para uma arquitetura moderna.

## 1. Abordagem A: Revivificação Legada ("Patching")
*Objetivo: Fazer o `PegaJogo.exe` original rodar em ambientes modernos.*

### Viabilidade Técnica
- **Desafio de Runtime:** Exige a instalação de runtimes do VB6 e registro de OCXs legadas (`mscomctl.ocx`, `mswinsck.ocx`).
- **O Problema do Flash:** O ActiveX original está bloqueado. Soluções incluem o uso de versões "unpatched" (anteriores a 2021) ou o uso de ferramentas como o *FlashPatch*.
- **O Problema do Banco de Dados:** Requer uma instância ativa do Firebird 2.0 com a `fbudf.dll` configurada corretamente para que as queries de navegação funcionem.

### Prós e Contras
- ✅ **Prós:** Preserva a experiência exata, os sons, as animações de interface e o comportamento original do software.
- ❌ **Contras:** Extremamente instável em Windows 10/11; depende de muitas "gambiarras" de sistema; vulnerável a futuras atualizações do Windows.

---

## 2. Abordagem B: Estrutura Híbrida (Novo Launcher)
*Objetivo: Criar um novo executável (Electron, C# ou Rust) que consome os dados originais.*

### Viabilidade Técnica
- **Consumo de Dados:** O novo launcher pode ler diretamente o arquivo `.fdb` (Firebird) ou usar o `games.json` gerado pelo nosso servidor Node.js.
- **Emulação Interna:** Utiliza o **Ruffle** integrado para rodar os SWFs sem depender de componentes do sistema operacional.
- **Mock de Rede:** O launcher pode apontar internamente para o `localhost:3000` (NewServer) para buscar banners e atualizações, simulando o comportamento de rede original.

### Prós e Contras
- ✅ **Prós:** Portabilidade total; segurança moderna; não exige instalação de drivers ou bancos de dados pesados no cliente final.
- ❌ **Contras:** Exige esforço de design para replicar visualmente a interface clássica do PegaJogo.

---

## 3. Comparativo de Estrutura de Dados

| Componente | Estrutura Original | Estrutura Proposta (New Server) |
| :--- | :--- | :--- |
| **Catálogo** | Firebird SQL (`.fdb`) | JSON Estático (`games.json`) |
| **Lógica de UI** | VB6 Forms / ActiveX | HTML5 / CSS / JavaScript |
| **Motor Flash** | `Flash.ocx` (ActiveX) | Ruffle (WebAssembly) |
| **Atualização** | Scripts `.php` remotos | API REST em Node.js |
| **Armazenamento** | Pasta `Games/` local | Pasta `Reference-Flash/` |

## 4. Conclusão e Recomendação
Para fins de **pesquisa e arqueologia**, a Abordagem A é essencial para entender como o software se comunicava. 

Para fins de **preservação funcional e distribuição**, a Abordagem B (Reconstrução Moderna via NewServer) é a única sustentável a longo prazo, pois remove as dependências "mortas" (Flash Player e Firebird UDFs) que impedem o acesso de novos usuários ao acervo.

### Próximos Passos Sugeridos
1. **Extração Final:** Exportar todos os dados do Firebird para JSON de forma automatizada.
2. **Interface:** Criar um "Skin" CSS que mimetize o TreeView clássico do PegaJogo no `index.html`.
3. **Wrapper:** Empacotar o NewServer em um executável único (usando ferramentas como `pkg` para Node.js) para facilitar o uso.

---
*Documento de planejamento para o ecossistema PegaJogo.*