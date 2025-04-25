import os
import pytest
import tempfile
from aquacrop.file_generators.SIMUL.aggregation_result_generator import generate_aggregation_results_settings
from aquacrop.file_generators.SIMUL.daily_results_generator import generate_daily_results_settings
from aquacrop.file_generators.SIMUL.particular_result_generator import generate_particular_results_settings

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

# Tests for aggregation_result_generator.py
def test_aggregation_results_none(temp_dir):
    test_file = os.path.join(temp_dir, "test_agg_none.sim")
    
    # Generate file with no aggregation (default)
    generate_aggregation_results_settings(
        file_path=test_file,
        aggregation_level=0
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content
    assert "0 : Time aggregation for intermediate results" in content
    assert "none" in content

def test_aggregation_results_daily(temp_dir):
    test_file = os.path.join(temp_dir, "test_agg_daily.sim")
    
    # Generate file with daily aggregation
    generate_aggregation_results_settings(
        file_path=test_file,
        aggregation_level=1
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content
    assert "1 : Time aggregation for intermediate results" in content
    assert "daily" in content

def test_aggregation_results_10day(temp_dir):
    test_file = os.path.join(temp_dir, "test_agg_10day.sim")
    
    # Generate file with 10-day aggregation
    generate_aggregation_results_settings(
        file_path=test_file,
        aggregation_level=2
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content
    assert "2 : Time aggregation for intermediate results" in content
    assert "10-daily" in content

def test_aggregation_results_monthly(temp_dir):
    test_file = os.path.join(temp_dir, "test_agg_monthly.sim")
    
    # Generate file with monthly aggregation
    generate_aggregation_results_settings(
        file_path=test_file,
        aggregation_level=3
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content
    assert "3 : Time aggregation for intermediate results" in content
    assert "monthly" in content

def test_aggregation_results_invalid_level(temp_dir):
    test_file = os.path.join(temp_dir, "test_agg_invalid.sim")
    
    # Generate file with invalid aggregation level (should default to 0)
    generate_aggregation_results_settings(
        file_path=test_file,
        aggregation_level=5  # Invalid level
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content - should default to 0
    assert "0 : Time aggregation for intermediate results" in content
    assert "none" in content

# Tests for daily_results_generator.py
def test_daily_results_all_types(temp_dir):
    test_file = os.path.join(temp_dir, "test_daily_all.sim")
    
    # Generate file with all output types
    output_types = [1, 2, 3, 4, 5, 6, 7, 8]
    
    generate_daily_results_settings(
        file_path=test_file,
        output_types=output_types
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content - should have all output types
    assert "1 : Various parameters of the soil water balance" in content
    assert "2 : Crop development and production" in content
    assert "3 : Soil water content in the soil profile and root zone" in content
    assert "4 : Soil salinity in the soil profile and root zone" in content
    assert "5 : Soil water content at various depths of the soil profile" in content
    assert "6 : Soil salinity at various depths of the soil profile" in content
    assert "7 : Climate input parameters" in content
    assert "8 : Irrigation events and intervals" in content

def test_daily_results_selective_types(temp_dir):
    test_file = os.path.join(temp_dir, "test_daily_selected.sim")
    
    # Generate file with selected output types
    output_types = [1, 3, 5, 7]
    
    generate_daily_results_settings(
        file_path=test_file,
        output_types=output_types
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content - should have only the selected output types
    assert "1 : Various parameters of the soil water balance" in content
    assert "3 : Soil water content in the soil profile and root zone" in content
    assert "5 : Soil water content at various depths of the soil profile" in content
    assert "7 : Climate input parameters" in content
    
    # Should not contain the unselected types
    assert "2 : Crop development and production" not in content
    assert "4 : Soil salinity in the soil profile and root zone" not in content
    assert "6 : Soil salinity at various depths of the soil profile" not in content
    assert "8 : Irrigation events and intervals" not in content

def test_daily_results_default(temp_dir):
    test_file = os.path.join(temp_dir, "test_daily_default.sim")
    
    # Generate file with default output types
    generate_daily_results_settings(
        file_path=test_file,
        output_types=None  # Use default
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content - should have types 1-7 by default
    assert "1 : Various parameters of the soil water balance" in content
    assert "2 : Crop development and production" in content
    assert "3 : Soil water content in the soil profile and root zone" in content
    assert "4 : Soil salinity in the soil profile and root zone" in content
    assert "5 : Soil water content at various depths of the soil profile" in content
    assert "6 : Soil salinity at various depths of the soil profile" in content
    assert "7 : Climate input parameters" in content
    
    # Should not contain type 8 by default
    assert "8 : Irrigation events and intervals" not in content

def test_daily_results_invalid_types(temp_dir):
    test_file = os.path.join(temp_dir, "test_daily_invalid.sim")
    
    # Generate file with some invalid output types
    output_types = [1, 9, 2, 10]  # 9 and 10 are invalid
    
    generate_daily_results_settings(
        file_path=test_file,
        output_types=output_types
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content - should only include valid types
    assert "1 : Various parameters of the soil water balance" in content
    assert "2 : Crop development and production" in content
    
    # Invalid types should be ignored
    assert "9" not in content
    assert "10" not in content

# Tests for particular_result_generator.py
def test_particular_results_all(temp_dir):
    test_file = os.path.join(temp_dir, "test_particular_all.sim")
    
    # Generate file with all particular output types
    output_types = [1, 2]
    
    generate_particular_results_settings(
        file_path=test_file,
        output_types=output_types
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content - should have both types
    assert "1 : Biomass and Yield at Multiple cuttings (for herbaceous forage crops)" in content
    assert "2 : Evaluation of simulation results (when Field Data)" in content

def test_particular_results_selected(temp_dir):
    test_file = os.path.join(temp_dir, "test_particular_selected.sim")
    
    # Generate file with just one particular output type
    output_types = [1]
    
    generate_particular_results_settings(
        file_path=test_file,
        output_types=output_types
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content - should have only type 1
    assert "1 : Biomass and Yield at Multiple cuttings (for herbaceous forage crops)" in content
    assert "2 : Evaluation of simulation results (when Field Data)" not in content

def test_particular_results_default(temp_dir):
    test_file = os.path.join(temp_dir, "test_particular_default.sim")
    
    # Generate file with default output types
    generate_particular_results_settings(
        file_path=test_file,
        output_types=None  # Use default
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content - should have both types by default
    assert "1 : Biomass and Yield at Multiple cuttings (for herbaceous forage crops)" in content
    assert "2 : Evaluation of simulation results (when Field Data)" in content

def test_particular_results_invalid(temp_dir):
    test_file = os.path.join(temp_dir, "test_particular_invalid.sim")
    
    # Generate file with an invalid output type
    output_types = [3]  # Invalid type
    
    generate_particular_results_settings(
        file_path=test_file,
        output_types=output_types
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check content - should be empty except for newline
    assert content.strip() == ""