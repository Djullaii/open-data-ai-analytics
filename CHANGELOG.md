# Changelog

## v0.6.0 - 2026-06-03

### Added

- Додано GitOps-структуру з Kubernetes manifest-файлами для web-застосунку.
- Додано Argo CD Application для автоматичної синхронізації папки `gitops/app`.
- Оновлено cloud-init для встановлення k3s, Argo CD та імпорту web-образу в k3s.
- Додано GitOps-повідомлення у веб-інтерфейс для демонстрації update і rollback.
- Оновлено Terraform outputs і NSG rules для GitOps NodePort та Argo CD.

## v0.5.0 - 2026-06-03

### Added

- Додано monitoring compose-файл з Prometheus, Grafana, node-exporter та cAdvisor.
- Додано Prometheus scrape targets для VM, Docker-контейнерів, Prometheus і веб-застосунку.
- Додано `/metrics` endpoint у веб-сервіс для базових метрик застосунку.
- Додано provisioning Grafana data source і dashboard `Open Data Monitoring`.
- Оновлено Terraform і cloud-init для запуску monitoring stack в Azure.

## v0.4.0 - 2026-06-03

### Added

- Додано Terraform-конфігурацію для розгортання Docker-проєкту в Azure.
- Додано cloud-init сценарій для автоматичного встановлення Docker на Linux VM.
- Додано інструкцію запуску через Azure Cloud Shell.

## v0.3.0 - 2026-06-02

### Added

- Додано Dockerfile для сервісів `data_load`, `data_quality_analysis`, `data_research`, `visualization` і `web`.
- Додано `compose.yaml` для локального запуску всіх контейнерів.
- Додано SQLite-базу через Docker volume.
- Додано простий веб-інтерфейс на порту `8000`.
- Додано приклад CSV-файлу для Docker-запуску.

## v0.2.0 - 2026-06-02

### Added

- Додано GitHub Actions workflow для запуску модулів.
- Додано workflow для ручного запуску на self-hosted runner.
- Результати запуску зберігаються як artifacts.

## v0.1.0 - 2026-06-02

### Added

- Додано базову структуру репозиторію для лабораторної роботи.
- Налаштовано `.gitignore` для кешів Python, notebook checkpoints, virtual environments і сирих даних.
- Додано README з метою проєкту, джерелом відкритих даних та гіпотезами аналізу.
- Реалізовано модуль `data_load` для завантаження та нормалізації CSV з Data.gov.ua.
- Реалізовано модуль `data_quality_analysis` для перевірки пропусків, дублікатів, дат і числових значень.
- Реалізовано модуль `data_research` для аналізу динаміки чисельності населення.
- Реалізовано модуль `visualization` для побудови SVG-графіка без зовнішніх залежностей.
- Створено та розв'язано merge-конфлікт у `README.md`.
