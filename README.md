
<p align="center">
  <img src="assets/logo.png" width="160">
</p>


<p align="center">
  Dynamic Portfolio Risk Analysis Platform
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue">
  <img src="https://img.shields.io/badge/status-in%20progress-yellow">
</p>

## Overview  

Strata is a portfolio risk analysis platform focused on understanding how ETF-based portfolios behave over time.

The project analyzes:

- Rolling volatility dynamics  
- Time-varying correlations  
- Diversification breakdown under stress  
- Portfolio drawdowns  
- Market regime shifts  

The objective is to produce portfolio-level risk insights using historical ETF data.

---

## Roadmap  

Implementation sequence:

```mermaid
flowchart LR
    A[Phase 1<br>Configuration & Infrastructure]
    B[Phase 2<br>Data Ingestion]
    C[Phase 3<br>Feature Engineering]
    D[Phase 4<br>Portfolio Risk Analysis]
    E[Phase 5<br>Reporting]

    A --> B --> C --> D --> E
````

---

### Phase 1 — Configuration & Infrastructure

* Configuration loader
* Storage abstraction
* Environment handling

### Phase 2 — Data Ingestion

* Historical ETF data ingestion
* Raw dataset storage

### Phase 3 — Feature Engineering

* Log returns
* Rolling volatility
* Rolling correlation
* Drawdown computation

### Phase 4 — Portfolio Risk Analysis

* Portfolio-level rolling risk
* Correlation matrix evolution
* Risk concentration analysis
* Regime detection
* Final analytical datasets

### Phase 5 — Reporting

* Analytical notebook
* Portfolio risk summaries
* Optional visualization layer

---

## Example Use Case

Given a portfolio composed of:

* SPY
* QQQ
* TLT
* GLD
* EEM

Strata enables the user to:

* Measure rolling portfolio volatility
* Track correlation shifts
* Identify diversification failures
* Observe drawdown development
* Detect regime transitions

---

## Current Status

Project initialized.

Phase 1 in progress.

## Authors  

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Tomasmoralessp">
        <img src="https://github.com/Tomasmoralessp.png" width="120">
      </a>
      <br>
      <b>Tomás Morales Galván</b>
    </td>
    <td align="center">
      <a href="https://github.com/MIGUELBACHILLERGH55">
        <img src="https://github.com/MIGUELBACHILLERGH55.png" width="120">
      </a>
      <br>
      <b>Miguel Bachiller Segovia</b>
    </td>
  </tr>
</table>

