import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.co2_generator import generate_co2_file

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_co2_file_with_default_records(temp_dir):
    test_file = os.path.join(temp_dir, "test_co2_default.co2")
    description = "Default atmospheric CO2 concentration"
    
    # Generate the file with default records
    generate_co2_file(
        file_path=test_file,
        description=description
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check basic structure of the file
    assert description in content
    assert "Year     CO2 (ppm by volume)" in content
    assert "============================" in content
    
    # Check presence of some key years in default data
    assert "1902  297.40" in content
    assert "1980" in content  # Should have 1980s data
    assert "2020" in content  # Should have projected data

def test_co2_file_with_custom_records(temp_dir):
    test_file = os.path.join(temp_dir, "test_co2_custom.co2")
    description = "Custom atmospheric CO2 concentration from 1902 to 2099"
    
    # Custom CO2 records based on Table 2.23k example
    custom_records = [
        (1902, 297.4),
        (1905, 298.2),
        (1912, 300.7),
        (1915, 301.3),
        (1924, 304.5),
        (2010, 389.90),
        (2011, 391.65),
        (2020, 409.57),
        (2099, 567.57)
    ]
    
    # Generate the file
    generate_co2_file(
        file_path=test_file,
        description=description,
        records=custom_records
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check the structure and specific content based on Table 2.23k
    assert description in content
    assert "Year     CO2 (ppm by volume)" in content
    assert "============================" in content
    
    # Check some specific records
    assert "1902  297.40" in content
    assert "1915  301.30" in content
    assert "2020  409.57" in content
    assert "2099  567.57" in content

def test_co2_file_single_value(temp_dir):
    test_file = os.path.join(temp_dir, "test_co2_single.co2")
    description = "Constant CO2 concentration of 550 ppm"
    
    # Single CO2 record (Table 2.23n example)
    constant_record = [(2050, 550.0)]
    
    # Generate the file
    generate_co2_file(
        file_path=test_file,
        description=description,
        records=constant_record
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check the structure and specific content based on Table 2.23n
    assert description in content
    assert "Year     CO2 (ppm by volume)" in content
    assert "============================" in content
    assert "2050  550.00" in content

def test_co2_file_chronological_order(temp_dir):
    test_file = os.path.join(temp_dir, "test_co2_order.co2")
    description = "CO2 records in non-chronological order"
    
    # Records in non-chronological order
    unordered_records = [
        (2020, 410.0),
        (1980, 340.0),
        (2000, 370.0),
        (1960, 320.0)
    ]
    
    # Generate the file
    generate_co2_file(
        file_path=test_file,
        description=description,
        records=unordered_records
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.readlines()
    
    # Check if records are in chronological order regardless of input order
    years_in_file = []
    for line in content:
        # Skip header lines and description
        if line.strip() and not line.startswith("Year") and not line.startswith("====") and not line.startswith(description):
            try:
                year = int(line.strip().split()[0])
                years_in_file.append(year)
            except ValueError:
                # Skip lines that don't have a proper year format
                continue
    
    # Check if years are sorted in ascending order
    assert years_in_file == sorted(years_in_file)
    
    # Verify the specific years are in the file
    assert 1960 in years_in_file
    assert 1980 in years_in_file
    assert 2000 in years_in_file
    assert 2020 in years_in_file