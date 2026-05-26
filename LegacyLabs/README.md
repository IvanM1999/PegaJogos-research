# LegacyLabs

Esta pasta contém os artefatos, scripts e documentação necessários para restaurar e rodar localmente a versão legacy do PegaJogo.

## Estrutura

- `bin/`
  - `PegaJogo.exe` — executável legacy original.

- `scripts/`
  - `legacy_local_server.py` — servidor local de mock para rotas legadas.
  - `string_triage.py` — script de triagem de strings e descoberta de endpoints.

- `reports/`
  - `legacy_strings_report.json` — relatório gerado pelo `string_triage.py` com URLs, hosts, scripts e outros artefatos identificados no binário.

- `docs/`
  - `binary_analysis_pega_jogo.md`
  - `installer_extraction_analysis.md`
  - `legacy_restoration_blueprint.md`
  - `local_run_instructions.md`
  - `modern_installer_strategy.md`
  - `unpacking_guide.md`

## Como usar

No `LegacyLabs`, execute o servidor local a partir de `scripts`:

```powershell
cd LegacyLabs\scripts
python legacy_local_server.py --port 80
```

Se precisar recarregar o relatório JSON, gere-o novamente com `string_triage.py`:

```powershell
cd LegacyLabs\scripts
python string_triage.py ..\bin\PegaJogo.exe --json ..\reports\legacy_strings_report.json
```

## Configuração de hosts local

Adicione estas linhas ao arquivo de hosts do Windows (`C:\Windows\System32\drivers\etc\hosts`):

```text
127.0.0.1 pegajogo.com
127.0.0.1 www.pegajogo.com
127.0.0.1 desktop.meusjogosonline.com
127.0.0.1 www.meusjogosonline.com
127.0.0.1 ads.xpg.com.br
127.0.0.1 promote.orkut.com
127.0.0.1 twitter.com
```

## Nota

O `legacy_local_server.py` agora procura o relatório em `LegacyLabs/reports/legacy_strings_report.json`.
