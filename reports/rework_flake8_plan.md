# Flake8 Fix Plan (foco por código)

## E501 (389 ocorrências)
- Ajustar linhas > 88 colunas (ou quebrar em múltiplas linhas).

- src/dashboard/Class/main.py:99:89 line too long (135 > 88 characters)
- src/dashboard/Class/run.py:82:89 line too long (95 > 88 characters)
- src/dashboard/Class/run.py:84:89 line too long (92 > 88 characters)
- src/dashboard/Class/src/dashboard/ssa_dashboard.py:242:89 line too long (123 > 88 characters)
- src/dashboard/Class/src/dashboard/ssa_dashboard.py:526:89 line too long (173 > 88 characters)
- src/dashboard/Class/src/dashboard/ssa_dashboard.py:1040:89 line too long (106 > 88 characters)
- src/dashboard/Class/src/dashboard/ssa_dashboard.py:1325:89 line too long (96 > 88 characters)
- src/dashboard/Class/src/dashboard/ssa_dashboard.py:1350:89 line too long (96 > 88 characters)
- src/dashboard/Class/src/dashboard/ssa_dashboard.py:1385:89 line too long (97 > 88 characters)
- src/dashboard/Class/src/dashboard/ssa_dashboard.py:1465:89 line too long (111 > 88 characters)

## W293 (339 ocorrências)

- src/dashboard/Class/run.py:14:1 blank line contains whitespace
- src/dashboard/Class/run.py:44:1 blank line contains whitespace
- src/dashboard/Class/run.py:70:1 blank line contains whitespace
- src/dashboard/Class/run.py:74:1 blank line contains whitespace
- src/dashboard/Class/run.py:76:1 blank line contains whitespace
- src/dashboard/Class/run.py:100:1 blank line contains whitespace
- src/dashboard/Class/run.py:103:1 blank line contains whitespace
- src/dashboard/Class/run.py:105:1 blank line contains whitespace
- src/dashboard/Class/run.py:112:1 blank line contains whitespace
- src/dashboard/Class/run.py:114:1 blank line contains whitespace

## F401 (60 ocorrências)
- Remover imports não utilizados.

- src/dashboard/Class/main.py:10:1 'dataclasses.dataclass' imported but unused
- src/dashboard/Class/main.py:11:1 'datetime.datetime' imported but unused
- src/dashboard/Class/main.py:11:1 'datetime.date' imported but unused
- src/dashboard/Class/main.py:13:1 'numpy as np' imported but unused
- src/dashboard/Class/main.py:14:1 'plotly.express as px' imported but unused
- src/dashboard/Class/main.py:15:1 'plotly.graph_objects as go' imported but unused
- src/dashboard/Class/main.py:16:1 'dash.Dash' imported but unused
- src/dashboard/Class/main.py:16:1 'dash.dcc' imported but unused
- src/dashboard/Class/main.py:16:1 'dash.html' imported but unused
- src/dashboard/Class/main.py:16:1 'dash.Input' imported but unused

## W291 (50 ocorrências)

- src/dashboard/Class/run.py:88:60 trailing whitespace
- src/dashboard/Class/src/utils/data_validator.py:80:50 trailing whitespace
- src/dashboard/Class/src/utils/data_validator.py:90:50 trailing whitespace
- src/dashboard/Class/src/utils/data_validator.py:120:71 trailing whitespace
- src/dashboard/Class/src/utils/file_manager.py:56:48 trailing whitespace
- src/dashboard/Class/src/utils/log_manager.py:176:76 trailing whitespace
- src/dashboard/Class/src/utils/log_manager.py:186:57 trailing whitespace
- src/dashboard/Class/src/utils/log_manager.py:191:57 trailing whitespace
- src/dashboard/Report_from_excel.py:7:78 trailing whitespace
- src/dashboard/Report_from_excel.py:1369:31 trailing whitespace

## F811 (34 ocorrências)
- Atenção: redefinição de nomes; revisar imports e ordem de código.

- src/dashboard/Class/main.py:11:1 redefinition of unused 'datetime' from line 6
- src/dashboard/Class/main.py:12:1 redefinition of unused 'pd' from line 4
- src/dashboard/Class/main.py:18:1 redefinition of unused 'logging' from line 3
- src/dashboard/Class/main.py:19:1 redefinition of unused 'dash_table' from line 16
- src/dashboard/Class/main.py:23:1 redefinition of unused 'warnings' from line 5
- src/dashboard/Class/main.py:29:1 redefinition of unused 'os' from line 1
- src/dashboard/Class/main.py:30:1 redefinition of unused 'sys' from line 2
- src/dashboard/Class/main.py:31:1 redefinition of unused 'logging' from line 18
- src/dashboard/Class/main.py:32:1 redefinition of unused 'Path' from line 7
- src/dashboard/Class/main.py:193:1 redefinition of unused 'LogManager' from line 43

## E302 (30 ocorrências)

- src/dashboard/Class/run.py:11:1 expected 2 blank lines, found 1
- src/dashboard/Class/run.py:40:1 expected 2 blank lines, found 1
- src/dashboard/Class/run.py:55:1 expected 2 blank lines, found 1
- src/dashboard/Class/run.py:67:1 expected 2 blank lines, found 1
- src/dashboard/Class/src/data/data_loader.py:14:1 expected 2 blank lines, found 1
- src/dashboard/Class/src/data/ssa_columns.py:6:1 expected 2 blank lines, found 1
- src/dashboard/Class/src/data/ssa_data.py:7:1 expected 2 blank lines, found 1
- src/dashboard/Class/src/utils/data_validator.py:8:1 expected 2 blank lines, found 1
- src/dashboard/Class/src/utils/data_validator.py:16:1 expected 2 blank lines, found 1
- src/dashboard/Class/src/utils/file_manager.py:9:1 expected 2 blank lines, found 1

## F821 (23 ocorrências)

- src/utils/lixo_para_servir_de_base.py:89:5 undefined name 'self'
- src/utils/lixo_para_servir_de_base.py:89:23 undefined name 'data'
- src/utils/lixo_para_servir_de_base.py:90:5 undefined name 'self'
- src/utils/lixo_para_servir_de_base.py:90:20 undefined name 'self'
- src/utils/lixo_para_servir_de_base.py:90:37 undefined name 'data'
- src/utils/lixo_para_servir_de_base.py:91:5 undefined name 'self'
- src/utils/lixo_para_servir_de_base.py:91:27 undefined name 'data'
- src/utils/lixo_para_servir_de_base.py:92:5 undefined name 'self'
- src/utils/lixo_para_servir_de_base.py:92:23 undefined name 'data'
- src/utils/lixo_para_servir_de_base.py:93:5 undefined name 'self'

## E722 (21 ocorrências)
- Evitar 'except:' genérico; especificar exceções.

- src/dashboard/Class/main.py:207:9 do not use bare 'except'
- src/dashboard/Class/run.py:63:9 do not use bare 'except'
- src/dashboard/Class/src/data/data_loader.py:49:13 do not use bare 'except'
- src/dashboard/Class/src/data/data_loader.py:53:17 do not use bare 'except'
- src/dashboard/Class/src/utils/date_utils.py:149:13 do not use bare 'except'
- src/dashboard/Class/src/utils/date_utils.py:208:5 do not use bare 'except'
- src/dashboard/Report_from_excel.py:100:13 do not use bare 'except'
- src/dashboard/Report_from_excel.py:104:17 do not use bare 'except'
- src/dashboard/Scrap-Playwright_otimizado_tratamento_de_erro_rede.py:214:9 do not use bare 'except'
- src/dashboard/Scrap-Playwright_otimizado_tratamento_de_erro_rede.py:880:9 do not use bare 'except'

## E303 (12 ocorrências)

- src/dashboard/Class/src/dashboard/ssa_dashboard.py:1559:5 too many blank lines (2)
- src/dashboard/Class/src/dashboard/ssa_visualizer.py:215:5 too many blank lines (2)
- src/dashboard/Class/src/dashboard/ssa_visualizer.py:399:5 too many blank lines (2)
- src/dashboard/Class/src/data/data_loader.py:287:5 too many blank lines (2)
- src/dashboard/Class/src/data/data_loader.py:440:5 too many blank lines (2)
- src/dashboard/Class/src/utils/data_validator.py:155:5 too many blank lines (3)
- src/dashboard/Class/src/utils/data_validator.py:211:5 too many blank lines (2)
- src/dashboard/Report_from_excel.py:113:5 too many blank lines (2)
- src/scrapers/legacy/Scrap-Playwright.py:157:5 too many blank lines (2)
- src/utils/lixo_para_servir_de_base.py:3469:5 too many blank lines (2)

## E128 (11 ocorrências)

- src/dashboard/Class/src/utils/data_validator.py:121:36 continuation line under-indented for visual indent
- src/dashboard/Class/src/utils/file_manager.py:57:24 continuation line under-indented for visual indent
- src/dashboard/Class/src/utils/log_manager.py:177:32 continuation line under-indented for visual indent
- src/dashboard/Class/src/utils/log_manager.py:187:29 continuation line under-indented for visual indent
- src/dashboard/Class/src/utils/log_manager.py:192:29 continuation line under-indented for visual indent
- src/dashboard/Report_from_excel.py:3582:32 continuation line under-indented for visual indent
- src/dashboard/Report_from_excel.py:3592:29 continuation line under-indented for visual indent
- src/dashboard/Report_from_excel.py:3597:29 continuation line under-indented for visual indent
- src/utils/lixo_para_servir_de_base.py:1627:24 continuation line under-indented for visual indent
- src/utils/lixo_para_servir_de_base.py:2411:13 continuation line under-indented for visual indent

## E402 (11 ocorrências)
- Mover imports para o topo do arquivo.

- src/dashboard/Class/main.py:39:1 module level import not at top of file
- src/dashboard/Class/main.py:40:1 module level import not at top of file
- src/dashboard/Class/main.py:41:1 module level import not at top of file
- src/dashboard/Class/main.py:42:1 module level import not at top of file
- src/dashboard/Class/main.py:43:1 module level import not at top of file
- src/dashboard/Class/main.py:44:1 module level import not at top of file
- src/dashboard/Class/main.py:45:1 module level import not at top of file
- src/dashboard/Class/run.py:32:1 module level import not at top of file
- src/dashboard/Class/run.py:33:1 module level import not at top of file
- src/dashboard/Class/run.py:34:1 module level import not at top of file

## F841 (11 ocorrências)

- src/dashboard/Class/src/dashboard/ssa_dashboard.py:23:9 local variable 'suppress_callback_exceptions' is assigned to but never used
- src/dashboard/Class/src/dashboard/ssa_dashboard.py:480:9 local variable 'state_colors' is assigned to but never used
- src/dashboard/Class/src/dashboard/ssa_dashboard.py:1023:9 local variable 'stats' is assigned to but never used
- src/dashboard/Class/src/dashboard/ssa_dashboard.py:1024:9 local variable 'state_counts' is assigned to but never used
- src/dashboard/Dashboard_SM.py:48:9 local variable 'stats' is assigned to but never used
- src/dashboard/Report_from_excel.py:1443:13 local variable 'header_format' is assigned to but never used
- src/dashboard/Report_from_excel.py:2081:9 local variable 'state_counts' is assigned to but never used
- src/dashboard/Report_from_excel.py:3310:21 local variable 'ssas_by_category' is assigned to but never used
- src/utils/lixo_para_servir_de_base.py:698:13 local variable 'header_format' is assigned to but never used
- src/utils/lixo_para_servir_de_base.py:3163:9 local variable 'responsiveness' is assigned to but never used

## F541 (8 ocorrências)

- src/dashboard/Report_from_excel.py:365:30 f-string is missing placeholders
- src/dashboard/Scrap-Playwright_otimizado_tratamento_de_erro_rede.py:986:23 f-string is missing placeholders
- src/dashboard/Scrap-Playwright_otimizado_tratamento_de_erro_rede.py:991:23 f-string is missing placeholders
- src/scrapers/Scrap-Playwright_otimizado_tratamento_de_erro_rede.py:986:23 f-string is missing placeholders
- src/scrapers/Scrap-Playwright_otimizado_tratamento_de_erro_rede.py:991:23 f-string is missing placeholders
- src/scrapers/scrap_sam_main.py:986:23 f-string is missing placeholders
- src/scrapers/scrap_sam_main.py:991:23 f-string is missing placeholders
- src/utils/lixo_para_servir_de_base.py:3798:28 f-string is missing placeholders

## E305 (7 ocorrências)

- src/dashboard/Class/run.py:25:1 expected 2 blank lines after class or function definition, found 1
- src/dashboard/Class/run.py:120:1 expected 2 blank lines after class or function definition, found 1
- src/dashboard/Dashboard_SM.py:512:1 expected 2 blank lines after class or function definition, found 1
- src/scrapers/legacy/scrap_SAM_BETA.py:64:1 expected 2 blank lines after class or function definition, found 1
- src/scrapers/legacy/scrap_SAM_BETA.py:93:1 expected 2 blank lines after class or function definition, found 1
- src/utils/Acha_botao.py:16:1 expected 2 blank lines after class or function definition, found 1
- src/utils/scrap_installer.py:28:1 expected 2 blank lines after class or function definition, found 1

## W292 (5 ocorrências)

- src/dashboard/Class/run.py:121:11 no newline at end of file
- src/dashboard/Class/src/utils/file_manager.py:181:18 no newline at end of file
- src/scrapers/__init__.py:18:59 no newline at end of file
- src/scrapers/legacy/scrap_SAM_BETA.py:235:64 no newline at end of file
- src/utils/Acha_botao.py:53:14 no newline at end of file

## E231 (1 ocorrências)

- src/dashboard/Report_from_excel.py:7:48 missing whitespace after ','

## E301 (1 ocorrências)

- src/dashboard/Class/src/utils/data_validator.py:212:5 expected 1 blank line, found 0

## E306 (1 ocorrências)

- src/dashboard/Class/src/dashboard/ssa_dashboard.py:1737:9 expected 1 blank line before a nested definition, found 0

