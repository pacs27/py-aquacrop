# AquaCrop Python API

[![PyPI version](https://img.shields.io/badge/pypi-v0.1.2-blue.svg)](https://pypi.org/project/aquacrop-py/)
[![Python Versions](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10-blue)](https://pypi.org/project/aquacrop-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://github.com/aquacropos/aquacrop-py)

A Python wrapper for the FAO AquaCrop crop growth model that enables programmatic control of simulations, input/output handling, and integration with data science workflows.

## Overview

AquaCrop is the crop water productivity model developed by the Land and Water Division of FAO. It simulates yield response to water and is particularly suited to address conditions where water is a key limiting factor in crop production.

This Python API provides a high-level interface to the AquaCrop executable, allowing you to:

- Configure and run AquaCrop simulations directly from Python
- Programmatically generate input files for all model components
- Parse and analyze output results as Pandas DataFrames
- Integrate crop modeling into reproducible scientific workflows
- Run multi-year simulations and sensitivity analyses

## Installation

```bash
pip install aquacrop-py
```
## Documentation and Examples
For examples and usage instructions, please refer to the notebooks directory containing Jupyter notebooks that demonstrate various features of the library.

## Components
The main components of the AquaCrop model that can be configured through this API include:

Crop: Growth parameters, water stress responses, and yield formation
Soil: Soil profile characteristics including horizons, hydraulic properties
Weather: Temperature, rainfall, ET0, and CO2 concentration
Irrigation: Irrigation scheduling and water application methods
Field Management: Soil fertility, mulches, weed management
Initial Conditions: Starting soil water content and crop development
Groundwater: Groundwater table characteristics
Calendar: Planting dates and season timing

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
This Python API was developed to facilitate access to the AquaCrop model developed by the Food and Agriculture Organization of the United Nations (FAO).
For more information about AquaCrop itself, visit FAO's AquaCrop page.