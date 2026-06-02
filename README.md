# Open Data AI Analytics

Проєкт для лабораторної роботи з використання системи контролю версій Git.
Мета проєкту - підготувати модульну структуру для завантаження, перевірки
якості, дослідження та візуалізації відкритих даних.

## Джерело даних

Використано відкритий набір даних Data.gov.ua:
[Чисельність та склад населення](https://data.gov.ua/dataset/5184e388-c554-45f2-871c-ac8527b6e2ac).

Розпорядник: Державна служба статистики України.

Основний CSV-ресурс:
`https://data.gov.ua/dataset/7b2cffb7-28f9-488b-85c6-fe364a42adde/resource/7e10f79a-871f-40f0-874e-6f2ff9da56e3/download/135-chiselnist-naiavnogo-naselennia-na-pochatok-periodu.csv`

## Модулі проєкту

- `src/data_load.py` - завантаження та нормалізація CSV-даних.
- `src/data_quality_analysis.py` - перевірка якості даних.
- `src/data_research.py` - базове дослідження та розрахунок показників.
- `src/visualization.py` - побудова графіка за підготовленими даними.
- `services/` - Docker-сервіси для запуску модулів у контейнерах.
- `web/` - простий веб-інтерфейс для перегляду результатів.

## Docker

Запуск усіх сервісів:

```powershell
docker compose up --build
```

Веб-інтерфейс:

```text
http://localhost:8000
```

Сервіси:

- `data_load` - читає `data/sample_population.csv`, створює SQLite БД і завантажує дані.
- `data_quality_analysis` - перевіряє пропуски, дублікати, дати та значення.
- `data_research` - рахує базову статистику.
- `visualization` - створює два SVG-графіки.
- `web` - показує дані, звіти і графіки в браузері.

Порт: `8000`.

Volumes:

- `db_data` - база SQLite.
- `reports_data` - JSON-звіти та SVG-графіки.

## Azure Terraform

Файли для розгортання у Microsoft Azure знаходяться в `infra/terraform/`.
Конфігурація створює Resource Group, Virtual Network, Subnet, Public IP,
Network Security Group, Network Interface і Linux VM. Під час першого запуску
VM отримує `cloud-init.yaml`, встановлює Docker, клонує цей репозиторій і
запускає Docker Compose.

Запуск в Azure Cloud Shell:

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
test -f ~/.ssh/id_rsa.pub || ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Після `terraform apply` у виводі буде `web_url`, наприклад:

```text
http://PUBLIC_IP:8000
```

Перевірка:

```bash
curl http://PUBLIC_IP:8000
```

Після демонстрації ресурси потрібно видалити:

```bash
terraform destroy
```

## Питання та гіпотези для аналізу

1. Як змінювалась чисельність наявного населення України у періоді, представленому в наборі даних?
2. Чи є в даних пропуски, дублікати або некоректні значення, які можуть впливати на аналіз?
3. Який середній темп зміни чисельності населення між першим і останнім доступними періодами?

## Аналітичний фокус

У модулі якості даних основна увага приділяється повноті, відсутності дублікатів,
коректності дат і числових значень. Після цієї перевірки набір даних
використовується для дослідження динаміки показника: початкового та кінцевого
значення, абсолютної зміни, відсоткової зміни та середнього помісячного темпу.

## Структура репозиторію

```text
open-data-ai-analytics/
├── data/
│   └── README.md
├── notebooks/
├── reports/
│   └── figures/
├── infra/
│   └── terraform/
├── services/
├── src/
├── web/
├── .gitignore
├── CHANGELOG.md
├── compose.yaml
└── README.md
```
