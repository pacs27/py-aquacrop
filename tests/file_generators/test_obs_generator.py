import os
import pytest
import tempfile
from aquacrop.file_generators.OBS.obs_generator import generate_observation_file
from aquacrop.constants import Constants

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_observations_file_with_all_data_types(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_obs_all.obs")
    location = "measurements of CC, B and SWC at particular days"
    
    # Observations based on Table 2.23x - 2 example
    observations = [
        {
            'day': 11,
            'canopy_cover': (5.0, 3.0),
            'soil_water': (300.0, 20.0)
        },
        {
            'day': 30,
            'canopy_cover': (30.0, 5.0),
            'biomass': (1.000, 0.3)
        },
        {
            'day': 40,
            'canopy_cover': (50.0, -9.0),
            'soil_water': (250.0, 25.0)
        },
        {
            'day': 50,
            'canopy_cover': (60.0, 5.0)
        },
        {
            'day': 72,
            'biomass': (4.000, 0.2),
            'soil_water': (150.0, 30.0)
        },
        {
            'day': 90,
            'biomass': (4.400, 0.3)
        },
        {
            'day': 110,
            'canopy_cover': (45.0, 6.0),
            'biomass': (5.000, 0.5),
            'soil_water': (100.0, 10.0)
        },
        {
            'day': 120,
            'biomass': (5.500, 0.5),
            'soil_water': (100.0, 10.0)
        }
    ]
    
    # Generate the file
    generate_observation_file(
        file_path=test_file,
        location=location,
        observations=observations,
        soil_depth=1.00,
        first_day=22,
        first_month=3,
        first_year=1901
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content based on Table 2.23x - 2
    assert location in content
    assert "7.1   : AquaCrop Version (August 2023)" in content
    assert "1.00  : depth of sampled soil profile" in content
    assert "22     : first day of observations" in content
    assert "3     : first month of observations" in content
    assert "1901     : first year of observations (1901 if not linked to a specific year)" in content
    assert "Day    Canopy cover (%)    dry Biomass (ton/ha)    Soil water content (mm)" in content
    assert "Mean     Std         Mean       Std           Mean      Std" in content
    
    # Check a few specific observations
    # Check a few specific observations
    for obs in observations:
        day = obs['day']
        cc_mean, cc_std = obs.get('canopy_cover', (-9.0, -9.0))
        bio_mean, bio_std = obs.get('biomass', (-9.000, -9.0))
        sw_mean, sw_std = obs.get('soil_water', (-9.0, -9.0))
        
        # Check the values are in the file with flexible whitespace matching
        assert f"{day}" in content
        
        if 'canopy_cover' in obs:
            assert f"{cc_mean:.1f}" in content
            if cc_std != -9.0:
                assert f"{cc_std:.1f}" in content
                
        if 'biomass' in obs:
            assert f"{bio_mean:.3f}" in content
            if bio_std != -9.0:
                assert f"{bio_std:.1f}" in content
                
        if 'soil_water' in obs:
            assert f"{sw_mean:.1f}" in content
            if sw_std != -9.0:
                assert f"{sw_std:.1f}" in content

def test_observations_file_with_minimal_data(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_obs_minimal.obs")
    location = "Minimal canopy cover observations"
    
    # Only canopy cover observations
    observations = [
        {'day': 10, 'canopy_cover': (5.0, 1.0)},
        {'day': 20, 'canopy_cover': (15.0, 2.0)},
        {'day': 30, 'canopy_cover': (35.0, 3.0)},
        {'day': 40, 'canopy_cover': (65.0, 4.0)},
        {'day': 50, 'canopy_cover': (85.0, 5.0)},
        {'day': 60, 'canopy_cover': (90.0, 3.0)},
        {'day': 70, 'canopy_cover': (85.0, 4.0)},
        {'day': 80, 'canopy_cover': (75.0, 5.0)},
        {'day': 90, 'canopy_cover': (65.0, 6.0)},
        {'day': 100, 'canopy_cover': (45.0, 4.0)},
        {'day': 110, 'canopy_cover': (25.0, 3.0)},
        {'day': 120, 'canopy_cover': (5.0, 2.0)}
    ]
    
    # Generate the file
    generate_observation_file(
        file_path=test_file,
        location=location,
        observations=observations,
        soil_depth=0.80,
        first_day=1,
        first_month=5,
        first_year=2020
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check basic structure
    assert location in content
    assert "0.80  : depth of sampled soil profile" in content
    assert "1     : first day of observations" in content
    assert "5     : first month of observations" in content
    assert "2020     : first year of observations (1901 if not linked to a specific year)" in content
    
    # Verify that all entries have biomass and soil water as -9.0 (not measured)
    for obs in observations:
        day = obs['day']
        cc_mean = obs['canopy_cover'][0]
        cc_std = obs['canopy_cover'][1]
        # Check for the pattern with -9.0 for biomass and soil water
        assert f"{day}      {cc_mean:.1f}    {cc_std:.1f}" in content
        assert "-9.000     -9.0" in content  # Biomass not measured
        assert "-9.0     -9.0" in content  # Soil water not measured

def test_observations_file_biomass_only(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_obs_biomass.obs")
    location = "Biomass observations only"
    
    # Only biomass observations
    observations = [
        {'day': 30, 'biomass': (0.500, 0.1)},
        {'day': 60, 'biomass': (2.500, 0.3)},
        {'day': 90, 'biomass': (5.000, 0.5)},
        {'day': 120, 'biomass': (7.500, 0.7)}
    ]
    
    # Generate the file
    generate_observation_file(
        file_path=test_file,
        location=location,
        observations=observations,
        soil_depth=1.20,
        first_day=15,
        first_month=6,
        first_year=2021
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check basic structure
    assert location in content
    assert "1.20  : depth of sampled soil profile" in content
    
    # Check biomass values
    for obs in observations:
        day = obs['day']
        bio_mean, bio_std = obs.get('biomass', (-9.000, -9.0))
        
        # Check the values are in the file with flexible whitespace matching
        assert f"{day}" in content
        assert f"{bio_mean:.3f}" in content
        assert f"{bio_std:.1f}" in content

def test_observations_file_soil_water_only(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_obs_soil_water.obs")
    location = "Soil water observations only"
    
    # Only soil water observations
    observations = [
        {'day': 10, 'soil_water': (350.0, 20.0)},
        {'day': 30, 'soil_water': (300.0, 25.0)},
        {'day': 50, 'soil_water': (250.0, 20.0)},
        {'day': 70, 'soil_water': (200.0, 15.0)},
        {'day': 90, 'soil_water': (150.0, 10.0)},
        {'day': 110, 'soil_water': (100.0, 10.0)}
    ]
    
    # Generate the file
    generate_observation_file(
        file_path=test_file,
        location=location,
        observations=observations,
        soil_depth=1.50,
        first_day=1,
        first_month=4,
        first_year=2022
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check basic structure
    assert location in content
    assert "1.50  : depth of sampled soil profile" in content
    
    # Check soil water values
    for obs in observations:
        day = obs['day']
        sw_mean, sw_std = obs.get('soil_water', (-9.0, -9.0))
        
        # Check the values are in the file with flexible whitespace matching
        assert f"{day}" in content
        assert f"{sw_mean:.1f}" in content
        assert f"{sw_std:.1f}" in content

def test_observations_file_sorts_by_day(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_obs_sorted.obs")
    location = "Unsorted observations should be sorted in output"
    
    # Observations in non-chronological order
    observations = [
        {'day': 90, 'canopy_cover': (70.0, 5.0)},
        {'day': 30, 'canopy_cover': (20.0, 2.0)},
        {'day': 120, 'canopy_cover': (40.0, 4.0)},
        {'day': 1, 'canopy_cover': (5.0, 1.0)},
        {'day': 60, 'canopy_cover': (50.0, 3.0)}
    ]
    
    # Generate the file
    generate_observation_file(
        file_path=test_file,
        location=location,
        observations=observations,
        soil_depth=1.00,
        first_day=1,
        first_month=1,
        first_year=2023
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.readlines()
    
    # Extract day numbers from content to check sorting
    day_lines = []
    for line in content:
        if line.strip() and not line.startswith(location) and not "AquaCrop Version" in line and \
            not "depth of sampled" in line and not "first day" in line and not "first month" in line and \
            not "first year" in line and not "Day" in line and not "Mean" in line and \
            not "============" in line:
            try:
                # Attempt to extract a day number from the beginning of the line
                parts = line.strip().split()
                if parts and parts[0].isdigit():
                    day_lines.append(line)
            except:
                pass
    
    # Extract the day numbers
    days = [int(line.strip().split()[0]) for line in day_lines]

    # Check if days are sorted
    assert days == sorted(days)
    assert days == [1, 30, 60, 90, 120]