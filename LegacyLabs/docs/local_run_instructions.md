# LegacyLabs - Execução Local do PegaJogo

Este documento descreve como usar os scripts dentro de `LegacyLabs` para analisar o binário `PegaJogo.exe` e montar um servidor local que substitui o antigo backend.

## 1. Análise do Binário
Use o script `scripts/string_triage.py` para extrair strings, URLs e domínios embutidos em `bin/PegaJogo.exe`.

```bash
cd LegacyLabs
cd scripts
python string_triage.py ..\bin\PegaJogo.exe --json ..\reports\legacy_strings_report.json
```

Isso produz um relatório contendo:
- URLs e hosts encontrados no binário
- endpoints de rede remotos
- nomes de scripts e arquivos esperados
- configuração recomendada de hosts local

## 2. Rodando o servidor local de mock
O `scripts/legacy_local_server.py` embarca um servidor HTTP que responde a caminhos legados como `/jogar` e arquivos `.php`/`.asp`.

```bash
cd LegacyLabs
cd scripts
python legacy_local_server.py --port 80
```

O script usa por padrão `../DataOriginal/executavel` como root, então ele serve diretamente os arquivos antigos do executável e a pasta `Games`.

Se você não puder usar a porta 80, use outra porta de teste:

```bash
python legacy_local_server.py --port 8080
```

## 3. Mapeamento de domínios antigos para local
Adicione as seguintes linhas ao arquivo de hosts do Windows (`C:\Windows\System32\drivers\etc\hosts`):

```text
127.0.0.1 pegajogo.com
127.0.0.1 www.pegajogo.com
127.0.0.1 desktop.meusjogosonline.com
127.0.0.1 www.meusjogosonline.com
127.0.0.1 ads.xpg.com.br
127.0.0.1 promote.orkut.com
127.0.0.1 twitter.com
```

Isso garante que as chamadas de rede do binário não saiam para a Internet.

## 4. O que ainda precisa ser ajustado
- O servidor local atualmente responde com páginas de stub para caminhos legados.
- O próximo passo é ajustar as respostas para replicar o formato exato que o binário espera em cada endpoint.
- O relatório JSON gerado pelo `string_triage.py` ajuda a identificar os endpoints que precisam ser construídos.

## 5. Localização dos arquivos
- `LegacyLabs/scripts/string_triage.py`: extrai strings e padrões do binário.
- `LegacyLabs/scripts/legacy_local_server.py`: servidor local de mock para endpoints legados.
- `LegacyLabs/reports/legacy_strings_report.json`: relatório JSON gerado pelo `string_triage.py`.
- `LegacyLabs/bin/PegaJogo.exe`: binário legacy usado para triagem.
- `LegacyLabs/docs/local_run_instructions.md`: instruções para executar tudo localmente.

## 6. Observação importante
Estas ferramentas foram criadas para trabalhar exclusivamente dentro de `LegacyLabs`. O binário original permanece em `DataOriginal/executavel/PegaJogo.exe`, mas todos os scripts de análise e mock ficam aqui.
