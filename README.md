# AquaCrop Python API

[![PyPI version](https://img.shields.io/pypi/v/pyaquacrop.svg)](https://pypi.org/project/pyaquacrop/)
[![Python Versions](https://img.shields.io/badge/python-3.11-blue)](https://pypi.org/project/pyaquacrop/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python wrapper for the FAO AquaCrop crop growth model that enables programmatic control of simulations, input/output handling, and integration with data science workflows.

## Overview

AquaCrop is the crop water productivity model developed by the Land and Water Division of FAO. It simulates yield response to water and is particularly suited to address conditions where water is a key limiting factor in crop production.

This Python API provides a high-level interface to the AquaCrop executable (version 7.2, [release details](https://github.com/KUL-RSDA/AquaCrop/releases/tag/v7.2)), allowing you to:

- Configure and run AquaCrop simulations directly from Python
- Programmatically generate input files for all model components
- Parse and analyze output results as Pandas DataFrames
- Integrate crop modeling into reproducible scientific workflows
- Run multi-year simulations and sensitivity analyses

## Installation

```bash
pip install pyaquacrop
```

## Quick Start

Here's a simple example showing how to set up and run a basic AquaCrop simulation:

```python
import os
from datetime import date
import pandas as pd
from aquacrop import AquaCrop, Crop, Soil, Weather, FieldManagement, Irrigation

# Import pre-configured templates for Ottawa
from aquacrop.templates import (
    ottawa_alfalfa, ottawa_sandy_loam, ottawa_temperatures,
    ottawa_rain, ottawa_eto, manuloa_co2_records, ottawa_management
)

# 1. Define simulation period
simulation_period = [{
    "start_date": date(2014, 5, 21),
    "end_date": date(2014, 10, 31),
    "planting_date": date(2014, 5, 21),
    "is_seeding_year": True,
}]

# 2. Create climate object
climate = Weather(
    location="Ottawa",
    temperatures=ottawa_temperatures,
    eto_values=ottawa_eto,
    rainfall_values=ottawa_rain,
    record_type=1,  # Daily records
    first_day=1,
    first_month=1,
    first_year=2014,
    co2_records=manuloa_co2_records,
)

# 3. Create irrigation schedule
irrigation_events = []
for i in range(1, 10):  # 9 irrigation events
    day = i * 14  # Every 14 days
    irrigation_events.append({'day': day, 'depth': 30, 'ec': 0.0})  # 30 mm depth

irrigation = Irrigation(
    name="Sprinkler Schedule",
    description="Sprinkler irrigation every 14 days",
    params={
        'irrigation_method': 1,  # Sprinkler
        'surface_wetted': 100,
        'irrigation_mode': 1,  # Specification of events
        'reference_day': -9,  # Reference day is onset of growing period
        'irrigation_events': irrigation_events
    }
)

# 4. Set up and run the simulation
simulation = AquaCrop(
    simulation_periods=simulation_period,
    crop=ottawa_alfalfa,
    soil=ottawa_sandy_loam,
    management=ottawa_management,
    irrigation=irrigation,  # Remove this line for rainfed conditions
    climate=climate,
    need_daily_output=True,
    need_seasonal_output=True
)

# Run the simulation
results = simulation.run()
print("Simulation completed successfully!")

# 5. Access results
seasonal_results = results['season']
daily_results = results['day']

# Print available columns in seasonal results to check what's available
print("\nAvailable columns in seasonal results:")
print(seasonal_results.columns.tolist())

# Safe function to get values from dataframe
def get_value(df, column, default=0):
    if column in df.columns:
        return df[column].values[0]
    else:
        print(f"Warning: Column '{column}' not found in results.")
        return default

# Example: Print key seasonal results
print("\nSeasonal Results:")
print(f"Total Biomass: {get_value(seasonal_results, 'BioMass', 0):.2f} ton/ha")
print(f"Total Yield: {get_value(seasonal_results, 'Y(dry)', 0):.2f} ton/ha")
print(f"Total Rainfall: {get_value(seasonal_results, 'Rain', 0):.1f} mm")
print(f"Total Irrigation: {get_value(seasonal_results, 'Irri', 0):.1f} mm")
print(f"Water Productivity: {get_value(seasonal_results, 'WPet', 0):.2f} kg/m³")

# You can also access daily results to see biomass accumulation over time
if isinstance(daily_results, dict):
    # For multiple runs, get the first run's dataframe
    run_key = list(daily_results.keys())[0]
    daily_df = daily_results[run_key]
else:
    # Single DataFrame case
    daily_df = daily_results

# Print biomass from daily results if available
biomass_col = None
for col in daily_df.columns:
    if 'Biomass' in col or 'BioMass' in col:
        biomass_col = col
        break

if biomass_col:
    last_day = daily_df.iloc[-1]
    print(f"\nFinal Biomass from daily results: {last_day[biomass_col]:.2f} ton/ha")
```

## Quick Start with Interactive Tutorials

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1eQKVXELy6PkCWOCx5xJnrNCMKC_c3-Df?usp=sharing)

Try PyAquaCrop directly in your browser with our tutorials:

1. <a href="https://colab.research.google.com/github/pacs27/py-aquacrop/blob/main/docs/notebooks/01_basic_simulation.ipynb">Basic Crop Simulation</a>
2. <a href="https://colab.research.google.com/github/pacs27/py-aquacrop/blob/main/docs/notebooks/02_ottawa_simulation.ipynb">Advanced Crop Simulation</a>
3. <a href="https://colab.research.google.com/github/pacs27/py-aquacrop/blob/main/docs/notebooks/03_irrigation.ipynb">Basic Irrigation Simulation</a>

## Components

PyAquaCrop provides a high-level interface to all major components of the AquaCrop model:

### Core Simulation Components

- **Crop**: Define crop growth parameters, water stress responses, yield formation, and phenology
- **Soil**: Configure soil profile characteristics including multiple horizons and hydraulic properties
- **Weather**: Manage temperature, rainfall, ET₀, and CO₂ concentration inputs
- **Irrigation**: Set up irrigation scheduling, methods, and water application strategies
- **Field Management**: Control soil fertility, mulches, weed management, and field practices

### Additional Configuration Components

- **Initial Conditions**: Specify starting soil water content and crop development state
- **Groundwater**: Define groundwater table characteristics and dynamics
- **Calendar**: Set planting dates, growing periods, and season timing
- **Off-Season**: Configure conditions between growing periods
- **Parameter**: Fine-tune model parameters for specific simulation requirements

### Simulation Outputs

- **Daily Results**: Track detailed daily changes in soil water balance, crop development
- **Seasonal Results**: Obtain season-long performance indicators and yields
- **Harvest Data**: Access biomass and yield information for multiple cutting events
- **Evaluation Statistics**: Compare simulation results against field observations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This Python API was developed to facilitate access to the AquaCrop model developed by the Food and Agriculture Organization of the United Nations (FAO).
For more information about AquaCrop itself, visit FAO's AquaCrop page.
