import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.cli_generator import generate_climate_file
from aquacrop.constants import Constants

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_climate_file(temp_dir, monkeypatch):
    # Mock the Constants.AQUACROP_VERSION_NUMBER and Constants.AQUACROP_VERSION_DATE
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_climate.cli")
    location = "Tunis (Tunisia) climatic data"
    tnx_file = "Tunis.TMP"
    eto_file = "Tunis.ETo"
    plu_file = "Tunis.Plu"
    co2_file = "MaunaLoa.CO2"
    
    # Generate the file
    generate_climate_file(
        file_path=test_file,
        location=location,
        tnx_file=tnx_file,
        eto_file=eto_file,
        plu_file=plu_file,
        co2_file=co2_file
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Expected content based on Table 2.23b example
    expected_content = (
        f"{location}\n"
        f" 7.1   : AquaCrop Version (August 2023)\n"
        f"{tnx_file}\n"
        f"{eto_file}\n"
        f"{plu_file}\n"
        f"{co2_file}"
    )
    assert content == expected_content

def test_alternate_climate_file(temp_dir, monkeypatch):
    # Test with different climate files
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_alt_climate.cli")
    location = "London (UK) climatic data"
    tnx_file = "London.TNX"
    eto_file = "London.ETo"
    plu_file = "London.PLU"
    co2_file = "Custom.CO2"
    
    # Generate the file
    generate_climate_file(
        file_path=test_file,
        location=location,
        tnx_file=tnx_file,
        eto_file=eto_file,
        plu_file=plu_file,
        co2_file=co2_file
    )
    
    # Check if file exists and content is correct
    assert os.path.isfile(test_file)
    
    with open(test_file, 'r') as f:
        content = f.read()
        
    expected_content = (
        f"{location}\n"
        f" 7.1   : AquaCrop Version (August 2023)\n"
        f"{tnx_file}\n"
        f"{eto_file}\n"
        f"{plu_file}\n"
        f"{co2_file}"
    )
    assert content == expected_content