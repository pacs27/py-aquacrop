import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.gwt_generator import generate_groundwater_file
from aquacrop.constants import Constants

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_no_groundwater_table(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_gwt_none.gwt")
    description = "no shallow groundwater table"
    
    # Generate the file with no groundwater
    generate_groundwater_file(
        file_path=test_file,
        description=description,
        groundwater_type=0  # No groundwater table
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content based on Table 2.23t - 2
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert "0 : no groundwater table" in content
    
    # Should not have any additional lines for groundwater observations
    assert "Day Depth (m) ECw (dS/m)" not in content

def test_constant_groundwater_table(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_gwt_constant.gwt")
    description = "constant groundwater table at 1.50 m and with salinity level of 1.5 dS/m"
    
    # Groundwater observation based on Table 2.23t - 3
    groundwater_observations = [
        {'day': 1, 'depth': 1.50, 'ec': 1.5}
    ]
    
    # Generate the file with constant groundwater
    generate_groundwater_file(
        file_path=test_file,
        description=description,
        groundwater_type=1,  # Fixed groundwater table
        groundwater_observations=groundwater_observations
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content based on Table 2.23t - 3
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert "1 : groundwater table at fixed depth and with constant salinity" in content
    assert "Day Depth (m) ECw (dS/m)" in content
    assert "====================================" in content
    assert "1 1.50 1.5" in content

def test_variable_groundwater_table(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_gwt_variable.gwt")
    description = "variable groundwater table for year 2000"
    
    # Groundwater observations based on Table 2.23t - 4
    groundwater_observations = [
        {'day': 50, 'depth': 1.00, 'ec': 1.0},
        {'day': 100, 'depth': 2.00, 'ec': 2.0},
        {'day': 200, 'depth': 3.00, 'ec': 3.0},
        {'day': 300, 'depth': 1.50, 'ec': 1.7},
        {'day': 400, 'depth': 0.80, 'ec': 0.7},
        {'day': 500, 'depth': 1.50, 'ec': 0.5}
    ]
    
    # Generate the file with variable groundwater
    generate_groundwater_file(
        file_path=test_file,
        description=description,
        groundwater_type=2,  # Variable groundwater table
        first_day=1,
        first_month=1,
        first_year=2000,
        groundwater_observations=groundwater_observations
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content based on Table 2.23t - 4
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert "2 : variable groundwater table" in content
    assert "1 : first day of observations" in content
    assert "1 : first month of observations" in content
    assert "2000 : first year of observations" in content
    assert "Day Depth (m) ECw (dS/m)" in content
    assert "====================================" in content
    
    # Check all groundwater observations
    assert "50 1.00 1.0" in content
    assert "100 2.00 2.0" in content
    assert "200 3.00 3.0" in content
    assert "300 1.50 1.7" in content
    assert "400 0.80 0.7" in content
    assert "500 1.50 0.5" in content

def test_not_linked_to_specific_year(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_gwt_generic.gwt")
    description = "variable groundwater table not linked to specific year"
    
    # Simple groundwater observations
    groundwater_observations = [
        {'day': 1, 'depth': 1.00, 'ec': 0.5},
        {'day': 180, 'depth': 2.00, 'ec': 1.0},
        {'day': 365, 'depth': 1.00, 'ec': 0.5}
    ]
    
    # Generate the file with variable groundwater not linked to specific year
    generate_groundwater_file(
        file_path=test_file,
        description=description,
        groundwater_type=2,  # Variable groundwater table
        first_day=1,
        first_month=1,
        first_year=1901,  # 1901 indicates not linked to specific year
        groundwater_observations=groundwater_observations
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check for the special year description
    assert "1901 : first year of observations (1901 if not linked to a specific year)" in content

def test_empty_observations(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_gwt_empty.gwt")
    description = "groundwater with empty observations"
    
    # Generate the file with empty observations
    generate_groundwater_file(
        file_path=test_file,
        description=description,
        groundwater_type=1,  # Fixed groundwater table
        groundwater_observations=[]  # Empty observations
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Should still have the headers but no data
    assert description in content
    assert "1 : groundwater table at fixed depth and with constant salinity" in content
    assert "Day Depth (m) ECw (dS/m)" in content
    assert "====================================" in content
    
    # Count the number of lines - should be just the headers (5 lines)
    assert len(content.strip().split('\n')) == 5