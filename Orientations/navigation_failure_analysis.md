# 🕵️ Análise de Falhas nos Scripts de Navegação

Ao tentar executar o PegaJogo em ambientes modernos, a navegação costuma falhar (menus travados ou erro de script). Identificamos quatro causas principais para esse comportamento:

### 1. O "Time Bomb" do Adobe Flash Player
O PegaJogo utiliza o componente ActiveX do Flash para renderizar sua interface principal. 
- **Problema:** Versões do Flash Player fabricadas após 2020 possuem um "kill switch" que impede a execução de arquivos `.swf`.
- **Sintoma:** O app abre, mas a área de navegação fica branca ou exibe um ícone estático de "i" (informação), impedindo qualquer clique.
- **Solução:** É necessário utilizar um "Flash Player Standalone" antigo (versão 10 ou 11) ou instalar o emulador **Ruffle** configurado como um proxy para o componente ActiveX.

### 2. Dependência de UDFs no Firebird (fbudf)
A navegação é dinâmica e depende de queries SQL no banco de dados local.
- **Problema:** O arquivo `fbudf.txt` na pasta `bin/udf/` indica que o sistema usa funções como `NVL`, `DOW` e `STRING2BLOB`. 
- **Falha Crítica:** Se o servidor Firebird instalado não tiver a DLL `fbudf.dll` na sua pasta `/UDF`, as queries de busca de categorias vão falhar silenciosamente ou retornar erro de "Function Unknown". Sem o retorno da query, a navegação não é populada.
- **Solução:** Copiar as DLLs de UDF para a pasta de instalação do servidor Firebird (ex: `C:\Program Files (x86)\Firebird\Firebird_2_0\UDF`).

### 3. Falha de Handshake Online (Timeout)
O binário `PegaJogo.exe` tenta realizar uma verificação inicial com o domínio `pegajogo.com.br`.
- **Problema:** O código de navegação (provavelmente em VB6) aguarda uma resposta síncrona do servidor antes de liberar a interface local.
- **Sintoma:** O aplicativo parece "congelado" por 30 a 60 segundos antes de permitir qualquer interação, ou dispara um erro de script de Internet Explorer (MSHTML).
- **Solução:** Redirecionar o tráfego via arquivo `hosts` ou desativar o adaptador de rede para forçar o "Modo Offline" imediato.

### 4. Registro de Componentes ActiveX (OCX)
A interface do PegaJogo depende de bibliotecas legadas que não vêm mais pré-instaladas no Windows 10/11.
- **Componentes prováveis:** `mscomctl.ocx` (ListView/TreeView) e `shdocvw.dll` (WebBrowser).
- **Sintoma:** Erro de "Component not correctly registered" ou "Class not registered".
- **Solução:** Registrar manualmente os componentes via terminal (Admin):
  ```cmd
  regsvr32.exe C:\Caminho\Para\PegaJogo\bin\flash.ocx
  regsvr32.exe C:\Caminho\Para\PegaJogo\bin\mscomctl.ocx
  ```

### 🔬 Próximos Passos para o Desenvolvedor
1. **Monitoramento:** Utilize o **Process Monitor (ProcMon)** da Sysinternals e filtre por `PegaJogo.exe`. Verifique quais arquivos `.dll` ou `.ocx` retornam "NOT FOUND".
2. **Depuração de SQL:** Configure o Firebird para gerar logs de queries (`fbtrace.conf`) e observe se as instruções `SELECT` que montam o menu de navegação estão resultando em erro.
3. **Descompressão:** Como o executável está compactado (apenas 1 importação DLL), utilize um descompactador para analisar as strings internas e confirmar as URLs de navegação.

---
*Documento de suporte para a recuperação funcional do PegaJogo.*