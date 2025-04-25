import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.sol_generator import generate_soil_file
from aquacrop.constants import Constants

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_soil_file_single_horizon(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_soil_single.sol")
    description = "Sandy soil with single horizon"
    
    # Define a single soil horizon
    horizons = [
        {
            'thickness': 1.20,
            'sat': 36.0,
            'fc': 13.0,
            'wp': 6.0,
            'ksat': 1500.0,
            'penetrability': 100,
            'gravel': 0,
            'cra': -0.390600,
            'crb': 1.255600,
            'description': 'sandy soil'
        }
    ]
    
    # Generate the file
    generate_soil_file(
        file_path=test_file,
        description=description,
        horizons=horizons,
        curve_number=61,
        readily_evaporable_water=9
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check basic structure
    assert description in content
    assert "number of soil horizons" in content
    assert "1" in content  # One horizon
    assert "sandy soil" in content  # Horizon description
    
    # Check horizon values
    assert "1.20" in content  # Thickness
    assert "36.0" in content  # Sat
    assert "13.0" in content  # FC
    assert "6.0" in content  # WP
    assert "1500.0" in content  # Ksat
    assert "100" in content  # Penetrability
    assert "0" in content  # Gravel
    assert "-0.390600" in content  # CRa
    assert "1.255600" in content  # CRb

def test_soil_file_multiple_horizons(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_soil_multiple.sol")
    description = "4 layered sandy clay soil"
    
    # Define multiple soil horizons based on Table 2.23s – 2 example
    horizons = [
        {
            'thickness': 0.30,
            'sat': 43.8,
            'fc': 41.6,
            'wp': 27.1,
            'ksat': 150.0,
            'penetrability': 100,
            'gravel': 0,
            'cra': -0.573700,
            'crb': -0.751602,
            'description': 'sandy clay'
        },
        {
            'thickness': 0.30,
            'sat': 48.7,
            'fc': 42.5,
            'wp': 27.7,
            'ksat': 150.0,
            'penetrability': 100,
            'gravel': 0,
            'cra': -0.573700,
            'crb': -0.751602,
            'description': 'sandy clay'
        },
        {
            'thickness': 0.30,
            'sat': 48.3,
            'fc': 40.9,
            'wp': 28.0,
            'ksat': 150.0,
            'penetrability': 100,
            'gravel': 0,
            'cra': -0.573700,
            'crb': -0.751602,
            'description': 'sandy clay'
        },
        {
            'thickness': 0.65,
            'sat': 45.7,
            'fc': 42.2,
            'wp': 28.1,
            'ksat': 150.0,
            'penetrability': 100,
            'gravel': 0,
            'cra': -0.573700,
            'crb': -0.751602,
            'description': 'sandy clay'
        }
    ]
    
    # Generate the file
    generate_soil_file(
        file_path=test_file,
        description=description,
        horizons=horizons,
        curve_number=72,
        readily_evaporable_water=5
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check basic structure based on Table 2.23s - 2
    assert description in content
    assert "        7.1                 : AquaCrop Version (August 2023)" in content
    assert "       72                   : CN (Curve Number)" in content
    assert "        5                   : Readily evaporable water from top layer (mm)" in content
    assert "        4                   : number of soil horizons" in content
    assert "  Thickness  Sat   FC    WP     Ksat   Penetrability  Gravel  CRa       CRb           description" in content
    
    # Check if all horizons are in the file
    assert "    0.30    43.8  41.6  27.1  150.0        100         0     -0.573700  -0.751602   sandy clay" in content
    assert "    0.30    48.7  42.5  27.7  150.0        100         0     -0.573700  -0.751602   sandy clay" in content
    assert "    0.30    48.3  40.9  28.0  150.0        100         0     -0.573700  -0.751602   sandy clay" in content
    assert "    0.65    45.7  42.2  28.1  150.0        100         0     -0.573700  -0.751602   sandy clay" in content

def test_soil_file_default_parameters(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_soil_default.sol")
    description = "Test soil with default parameters"
    
    # Define horizons with minimal parameters, others should use defaults
    horizons = [
        {
            'thickness': 0.50,
            'sat': 40.0,
            'fc': 30.0,
            'wp': 15.0,
            'ksat': 200.0,
            'description': 'loam'
        }
    ]
    
    # Generate the file
    generate_soil_file(
        file_path=test_file,
        description=description,
        horizons=horizons
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check if default values are used
    assert "100" in content  # Penetrability default value
    assert "0" in content    # Gravel default value
    
    # Default CN and REW
    assert "       61                   : CN (Curve Number)" in content
    assert "        9                   : Readily evaporable water from top layer (mm)" in content

def test_soil_file_max_horizons(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_soil_max.sol")
    description = "Soil with maximum number of horizons (5)"
    
    # Define 5 horizons (maximum allowed in AquaCrop)
    horizons = []
    for i in range(5):
        horizons.append({
            'thickness': 0.20,
            'sat': 40.0 - i,
            'fc': 30.0 - i,
            'wp': 15.0 - i,
            'ksat': 200.0 - i*20,
            'description': f'horizon {i+1}'
        })
    
    # Generate the file
    generate_soil_file(
        file_path=test_file,
        description=description,
        horizons=horizons
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check if all 5 horizons are in the file
    assert "        5                   : number of soil horizons" in content
    
    for i in range(5):
        assert f'horizon {i+1}' in content