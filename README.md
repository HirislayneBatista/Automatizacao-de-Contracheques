# Automatização e Organização de Contracheques – Portal do Servidor (MA)

Este projeto automatiza a **emissão, organização e unificação de contracheques em PDF** a partir do Portal do Servidor do Maranhão, utilizando **Python + Selenium**.

O objetivo é eliminar o trabalho manual repetitivo de acessar mês a mês, baixar arquivos, renomear e organizar documentos, garantindo **padronização, rastreabilidade e economia de tempo**.

---

## 📌 Funcionalidades

### 1️⃣ Emissão automática de contracheques
- Login **manual e seguro** (sem captura de credenciais)
- Seleção automática de **ano e mês**
- Download do contracheque em PDF
- Renomeação automática no padrão:
  ```MM.AAAA.pdf```
- Organização em pastas por ano:
```
  Contracheques/
├── 2020/
├── 2021/
├── 2022/
└── ...
```

### 2️⃣ Unificação de PDFs por ano
- Junta automaticamente os PDFs mensais de cada ano
- Mantém a ordem cronológica (Janeiro → Dezembro)
- Gera um único arquivo final por ano: ex ```Contracheques_2020.pdf```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.13**
- **Selenium**
- **Chrome WebDriver**
- **pypdf**
- **webdriver-manager**

---

## ⚙️ Pré-requisitos

1. Python 3.10 ou superior
2. Google Chrome instalado
3. Instalar dependências:

```bash
pip install selenium webdriver-manager pypdf
