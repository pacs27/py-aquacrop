import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.irr_generator import generate_irrigation_file
from aquacrop.constants import Constants

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_irr_file_specified_events(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_irr_events.irr")
    description = "given irrigation schedule"
    
    # Define irrigation events based on Table 2.23q - 3 example
    irrigation_events = [
        {'day': 91, 'depth': 50, 'ec': 1.5},
        {'day': 101, 'depth': 50, 'ec': 1.5},
        {'day': 111, 'depth': 50, 'ec': 1.5},
        {'day': 121, 'depth': 50, 'ec': 1.5},
        {'day': 131, 'depth': 50, 'ec': 1.5},
        {'day': 141, 'depth': 50, 'ec': 1.5},
        {'day': 161, 'depth': 50, 'ec': 1.5}
    ]
    
    # Generate the file
    generate_irrigation_file(
        file_path=test_file,
        description=description,
        irrigation_method=1,  # Sprinkler
        surface_wetted=100,   # 100% of surface wetted
        irrigation_mode=1,    # Specification of irrigation events
        reference_day=28490,  # Reference day number
        irrigation_events=irrigation_events
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content based on Table 2.23q - 3
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert "1 : Sprinkler irrigation" in content
    assert "100 : Percentage of soil surface wetted by irrigation" in content
    assert "1 : Specification of irrigation events" in content
    assert "28490 : Reference DayNr for Day 1" in content
    assert "Day Depth (mm) ECw (dS/m)" in content
    
    # Check irrigation events
    for event in irrigation_events:
        assert f"{event['day']} {event['depth']} {event['ec']:.1f}" in content

def test_irr_file_generated_schedule(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_irr_generated.irr")
    description = "Generation of irrigation schedule"
    
    # Define generation rules based on Table 2.23q - 4 example
    generation_rules = [
        {'from_day': 1, 'time_value': 40, 'depth_value': 40, 'ec': 0.4},
        {'from_day': 41, 'time_value': 7, 'depth_value': 40, 'ec': 0.6},
        {'from_day': 116, 'time_value': 100, 'depth_value': 40, 'ec': 0.8}
    ]
    
    # Generate the file
    generate_irrigation_file(
        file_path=test_file,
        description=description,
        irrigation_method=1,  # Sprinkler
        surface_wetted=100,   # 100% of surface wetted
        irrigation_mode=2,    # Generate irrigation schedule
        time_criterion=1,     # Fixed intervals
        depth_criterion=2,    # Fixed application depth
        generation_rules=generation_rules
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content based on Table 2.23q - 4
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert "1 : Sprinkler irrigation" in content
    assert "100 : Percentage of soil surface wetted by irrigation" in content
    assert "2 : Generate irrigation schedule" in content
    assert "1 : Time criterion = fixed intervals" in content
    assert "2 : Depth criterion = fixed application depth" in content
    assert "From day Interval (days) Application depth (mm) ECw (dS/m)" in content
    
    # Check generation rules
    assert "1 40 40 0.4" in content
    assert "41 7 40 0.6" in content
    assert "116 100 40 0.8" in content

def test_irr_file_net_requirement(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_irr_net_req.irr")
    description = "Determination of Net irrigation requirement (allowable depletion 73 % RAW)"
    
    # Generate the file
    generate_irrigation_file(
        file_path=test_file,
        description=description,
        irrigation_method=1,  # Method not considered for net irrigation requirement
        surface_wetted=100,   # Not considered for net irrigation requirement
        irrigation_mode=3,    # Determination of net irrigation requirement
        depletion_threshold=73  # 73% RAW as threshold
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content based on Table 2.23q - 5
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert "1 : Sprinkler irrigation" in content
    assert "100 : Percentage of soil surface wetted by irrigation" in content
    assert "3 : Determination of net irrigation water requirement" in content
    assert "73 : Threshold for irrigation (% of RAW)" in content

def test_different_irrigation_methods(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    # Test different irrigation methods
    methods = {
        1: "Sprinkler irrigation",
        2: "Surface irrigation: Basin",
        3: "Surface irrigation: Border",
        4: "Surface irrigation: Furrow",
        5: "Drip irrigation"
    }
    
    for method_code, method_name in methods.items():
        test_file = os.path.join(temp_dir, f"test_irr_method_{method_code}.irr")
        description = f"Irrigation using {method_name}"
        
        # Generate the file with different irrigation method
        generate_irrigation_file(
            file_path=test_file,
            description=description,
            irrigation_method=method_code,
            surface_wetted=100,
            irrigation_mode=3,  # Simple mode for testing
            depletion_threshold=50
        )
        
        # Check if file exists
        assert os.path.isfile(test_file)
        
        # Read and verify the irrigation method
        with open(test_file, 'r') as f:
            content = f.read()
            
        assert f"{method_code} : {method_name}" in content

def test_time_criteria_for_generated_schedule(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    # Test different time criteria for generation
    criteria = {
        1: "Time criterion = fixed intervals",
        2: "Time criterion = allowable depletion (mm water)",
        3: "Time criterion = allowable depletion (% of RAW)",
        4: "Time criterion = keep minimum level of surface water layer"
    }
    
    for criterion_code, criterion_name in criteria.items():
        test_file = os.path.join(temp_dir, f"test_irr_criterion_{criterion_code}.irr")
        description = f"Irrigation generation using {criterion_name}"
        
        # Sample rule for testing
        generation_rules = [
            {'from_day': 1, 'time_value': 10, 'depth_value': 50, 'ec': 1.0}
        ]
        
        # Generate the file with different time criterion
        generate_irrigation_file(
            file_path=test_file,
            description=description,
            irrigation_method=1,
            surface_wetted=100,
            irrigation_mode=2,  # Generate schedule
            time_criterion=criterion_code,
            depth_criterion=1,  # Back to FC
            generation_rules=generation_rules
        )
        
        # Check if file exists
        assert os.path.isfile(test_file)
        
        # Read and verify the time criterion
        with open(test_file, 'r') as f:
            content = f.read()
            
        assert f"{criterion_code} : {criterion_name}" in content