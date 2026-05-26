# LegacyClone

`LegacyClone` é um projeto NodeGUI que traz uma interface desktop JavaScript para os mesmos objetivos de restauração do `LegacyLabs`.

## Objetivo

- Criar uma alternativa desktop em NodeGUI para orquestrar as ferramentas de análise e mock já existentes em `LegacyLabs`.
- Permitir que quem prefere JavaScript e UI nativa use `LegacyLabs` sem depender de navegadores ou webviews.

## Estrutura inicial

- `app.js` — aplicação NodeGUI principal.
- `package.json` — dependência de `@nodegui/nodegui` e comando de inicialização.

## Como instalar

No diretório `LegacyClone`: 

```powershell
cd LegacyClone
npm install
```

## Como usar

```powershell
cd LegacyClone
npm start
```

## O que o app faz

- executa `LegacyLabs/scripts/string_triage.py` usando o Python instalado
- inicia e para `LegacyLabs/scripts/legacy_local_server.py`
- carrega o relatório JSON de `LegacyLabs/reports/legacy_strings_report.json`

## Observações

- O app espera que `LegacyLabs` esteja no mesmo nível de pasta de `LegacyClone`.
- Algumas funcionalidades dependem de um Python disponível no PATH.
- O servidor local usa a porta configurada na interface; por padrão, `80`.
