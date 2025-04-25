import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.man_generator import generate_management_file
from aquacrop.constants import Constants

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_management_file_default(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_man_default.man")
    description = "No soil fertility stress, no organic mulches, no practices affecting surface run-off, perfect weed management and no multiple harvests"
    
    # Generate the file with default parameters
    generate_management_file(
        file_path=test_file,
        description=description
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check basic structure and default values based on Table 2.23r - 3 example
    assert description in content
    assert "7.1       : AquaCrop Version (August 2023)" in content
    assert "0         : percentage (%) of ground surface covered by mulches IN growing period" in content
    assert "50         : effect (%) of mulches on reduction of soil evaporation" in content
    assert "50         : Degree of soil fertility stress (%) - Effect is crop specific" in content
    assert "0.00      : height (m) of soil bunds" in content
    assert "0         : surface runoff NOT affected by field surface practices" in content
    assert "0         : relative cover of weeds at canopy closure (%)" in content
    assert "0         : increase of relative cover of weeds in mid-season (+%)" in content
    assert "100.00      : shape factor of the CC expansion function in a weed infested field" in content
    assert "100         : replacement (%) by weeds of the self-thinned part of the CC - only for perennials" in content
    assert "0         : Multiple cuttings are NOT considered" in content

def test_management_file_with_soil_fertility_and_mulches(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_man_fertility_mulches.man")
    description = "Management with soil fertility stress and mulches"
    
    # Generate the file with fertility stress and mulches
    generate_management_file(
        file_path=test_file,
        description=description,
        fertility_stress=80,
        mulch_cover=60,
        mulch_effect=75
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check specific values
    assert "60         : percentage (%) of ground surface covered by mulches IN growing period" in content
    assert "75         : effect (%) of mulches on reduction of soil evaporation" in content
    assert "80         : Degree of soil fertility stress (%) - Effect is crop specific" in content

def test_management_file_with_surface_runoff_settings(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_man_surface_runoff.man")
    description = "Management with surface runoff settings"
    
    # Generate the file with surface runoff settings
    generate_management_file(
        file_path=test_file,
        description=description,
        bund_height=0.15,
        surface_runoff_affected=1,
        runoff_adjustment=10
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check specific values
    assert "0.15      : height (m) of soil bunds" in content
    assert "1         : surface runoff IS affected by field surface practices" in content
    assert "10         : surface runoff is affected by field practices" in content

def test_management_file_with_weeds(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_man_weeds.man")
    description = "Management with weed infestation"
    
    # Generate the file with weed settings
    generate_management_file(
        file_path=test_file,
        description=description,
        weed_cover_initial=20,
        weed_cover_increase=30,
        weed_shape_factor=0.5,
        weed_replacement=75
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check specific values
    assert "20         : relative cover of weeds at canopy closure (%)" in content
    assert "30         : increase of relative cover of weeds in mid-season (+%)" in content
    assert "0.50      : shape factor of the CC expansion function in a weed infested field" in content
    assert "75         : replacement (%) by weeds of the self-thinned part of the CC - only for perennials" in content

def test_management_file_with_multiple_cuttings(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_man_multiple_cuttings.man")
    description = "Management with multiple cuttings"
    
    # Harvest days based on Table 2.23r - 3 example
    harvest_days = [174, 203, 244, 293]
    
    # Generate the file with multiple cutting settings
    generate_management_file(
        file_path=test_file,
        description=description,
        multiple_cuttings=True,
        canopy_after_cutting=25,
        cgc_increase_after_cutting=20,
        cutting_window_start_day=1,
        cutting_window_length=-9,  # Total growth cycle
        cutting_schedule_type=0,   # Specified schedule
        cutting_time_criterion=0,  # Not applicable
        final_harvest_at_maturity=0,
        day_nr_base=40909,
        harvest_days=harvest_days
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check specific values for multiple cuttings
    assert "1         : Multiple cuttings are considered" in content
    assert "25         : Canopy cover (%) after cutting" in content
    assert "20         : Increase (%) of Canopy Growth Coefficient (CGC) after cutting" in content
    assert "1         : First day of window for multiple cuttings (1 = start of growth cycle)" in content
    assert "-9         : Number of days in window for multiple cuttings (-9 = total growth cycle)" in content
    assert "0         : Multiple cuttings schedule is specified" in content
    assert "0         : Time criterion: Not Applicable" in content
    assert "0         : final harvest at crop maturity is not considered" in content
    assert "40909         : dayNr for Day 1 of list of cuttings" in content
    
    # Check harvest days
    assert "Harvest Day" in content
    assert "==============" in content
    for day in harvest_days:
        assert str(day) in content