import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.sw0_generator import generate_initial_conditions_file
from aquacrop.constants import Constants

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_initial_conditions_water_between_bunds(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_sw0_bunds.sw0")
    description = "uniform silty soil at saturation with water between soil bunds"
    
    # Layer data based on Table 2.23u - 2 example
    layer_data = [
        {"thickness": 4.00, "water_content": 43.00, "ec": 0.00}
    ]
    
    # Generate the file
    generate_initial_conditions_file(
        file_path=test_file,
        description=description,
        initial_canopy_cover=-9.00,
        initial_biomass=0.000,
        initial_rooting_depth=-9.00,
        water_layer=150.0,
        water_layer_ec=0.00,
        soil_water_content_type=0,  # For specific layers
        soil_data=layer_data
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content based on Table 2.23u - 2
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert "-9.00 : initial canopy cover that can be reached without water stress will be used as default" in content
    assert "0.000 : biomass (ton/ha) produced before the start of the simulation period" in content
    assert "-9.00 : initial effective rooting depth that can be reached without water stress will be used as default" in content
    assert "150.0 : water layer (mm) stored between soil bunds (if present)" in content
    assert "0.00 : electrical conductivity (dS/m) of water layer stored between soil bunds (if present)" in content
    assert "0 : soil water content specified for specific layers" in content
    assert "1 : number of layers considered" in content
    
    # Check soil layer data
    assert "Thickness layer (m) Water content (vol%) ECe(dS/m)" in content
    assert "==============================================================" in content
    assert "4.00 43.00 0.00" in content

def test_initial_conditions_specific_layers(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_sw0_layers.sw0")
    description = "Soil water and salinity content in Field AZ123 on 21 March 2010"
    
    # Layer data based on Table 2.23u - 3 example
    layer_data = [
        {"thickness": 0.40, "water_content": 30.00, "ec": 1.00},
        {"thickness": 0.40, "water_content": 20.00, "ec": 2.00},
        {"thickness": 0.40, "water_content": 18.00, "ec": 2.50}
    ]
    
    # Generate the file
    generate_initial_conditions_file(
        file_path=test_file,
        description=description,
        initial_canopy_cover=-9.00,
        initial_biomass=0.000,
        initial_rooting_depth=-9.00,
        water_layer=0.0,
        water_layer_ec=0.00,
        soil_water_content_type=0,  # For specific layers
        soil_data=layer_data
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content based on Table 2.23u - 3
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert "0.0 : water layer (mm) stored between soil bunds (if present)" in content
    assert "0 : soil water content specified for specific layers" in content
    assert "3 : number of layers considered" in content
    
    # Check soil layer data
    assert "Thickness layer (m) Water content (vol%) ECe(dS/m)" in content
    assert "==============================================================" in content
    assert "0.40 30.00 1.00" in content
    assert "0.40 20.00 2.00" in content
    assert "0.40 18.00 2.50" in content

def test_initial_conditions_particular_depths(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_sw0_depths.sw0")
    description = "example with soil water content at particulars depths"
    
    # Depth data based on Table 2.23u - 4 example
    depth_data = [
        {"depth": 0.10, "water_content": 23.00, "ec": 0.00},
        {"depth": 0.29, "water_content": 15.00, "ec": 0.00},
        {"depth": 0.45, "water_content": 34.00, "ec": 0.00},
        {"depth": 0.66, "water_content": 15.00, "ec": 0.00},
        {"depth": 1.00, "water_content": 10.00, "ec": 0.00}
    ]
    
    # Generate the file
    generate_initial_conditions_file(
        file_path=test_file,
        description=description,
        initial_canopy_cover=-9.00,
        initial_biomass=0.000,
        initial_rooting_depth=-9.00,
        water_layer=0.0,
        water_layer_ec=0.00,
        soil_water_content_type=1,  # At particular depths
        soil_data=depth_data
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content based on Table 2.23u - 4
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert "1 : soil water content specified for particular depths" in content
    assert "5 : number of soil depths considered" in content
    
    # Check soil depth data
    assert "Soil depth (m) Water content (vol%) ECe (dS/m)" in content
    assert "==============================================================" in content
    assert "0.10 23.00 0.00" in content
    assert "0.29 15.00 0.00" in content
    assert "0.45 34.00 0.00" in content
    assert "0.66 15.00 0.00" in content
    assert "1.00 10.00 0.00" in content

def test_initial_conditions_after_planting(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_sw0_after_planting.sw0")
    description = "initial conditions 1 month after planting"
    
    # Depth data based on Table 2.23u - 5 example
    depth_data = [
        {"depth": 0.10, "water_content": 10.00, "ec": 0.00},
        {"depth": 0.40, "water_content": 15.00, "ec": 0.00},
        {"depth": 0.60, "water_content": 30.00, "ec": 0.00},
        {"depth": 0.80, "water_content": 30.00, "ec": 0.00},
        {"depth": 1.00, "water_content": 33.00, "ec": 0.00},
        {"depth": 1.20, "water_content": 25.00, "ec": 0.00}
    ]
    
    # Generate the file
    generate_initial_conditions_file(
        file_path=test_file,
        description=description,
        initial_canopy_cover=31.00,  # Actual value provided
        initial_biomass=0.150,
        initial_rooting_depth=-9.00,
        water_layer=0.0,
        water_layer_ec=0.00,
        soil_water_content_type=1,  # At particular depths
        soil_data=depth_data
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content based on Table 2.23u - 5
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert "31.00 : initial canopy cover (%) at start of simulation period" in content
    assert "0.150 : biomass (ton/ha) produced before the start of the simulation period" in content
    assert "-9.00 : initial effective rooting depth that can be reached without water stress will be used as default" in content
    assert "1 : soil water content specified for particular depths" in content
    assert "6 : number of soil depths considered" in content
    
    # Check soil depth data
    assert "0.10 10.00 0.00" in content
    assert "0.40 15.00 0.00" in content
    assert "0.60 30.00 0.00" in content
    assert "0.80 30.00 0.00" in content
    assert "1.00 33.00 0.00" in content
    assert "1.20 25.00 0.00" in content

def test_initial_conditions_empty_soil_data(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_sw0_empty.sw0")
    description = "Initial conditions with no soil data"
    
    # Generate the file with no soil data
    generate_initial_conditions_file(
        file_path=test_file,
        description=description,
        initial_canopy_cover=-9.00,
        initial_biomass=0.000,
        initial_rooting_depth=-9.00,
        water_layer=0.0,
        water_layer_ec=0.00,
        soil_water_content_type=0,  # For specific layers
        soil_data=[]  # Empty soil data
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check that soil data section shows 0 layers
    assert "0 : number of layers considered" in content