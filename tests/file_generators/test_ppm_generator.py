import os
import pytest
import tempfile
from aquacrop.file_generators.PARAM.ppn_generator import generate_parameter_file

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_parameter_file_default_values(temp_dir):
    test_file = os.path.join(temp_dir, "test_default_params.pp1")
    
    # Generate the file with default parameters
    generate_parameter_file(file_path=test_file)
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check default parameter values based on Table 2.23w-7
    assert "4         : Evaporation decline factor for stage II" in content
    assert "1.10      : Ke(x) Soil evaporation coefficient for fully wet and non-shaded soil surface" in content
    assert "5         : Threshold for green CC below which HI can no longer increase (% cover)" in content
    assert "70         : Starting depth of root zone expansion curve (% of Zmin)" in content
    assert "5.00      : Maximum allowable root zone expansion (fixed at 5 cm/day)" in content
    assert "-6         : Shape factor for effect water stress on root zone expansion" in content
    assert "20         : Required soil water content in top soil for germination (% TAW)" in content
    assert "1.0       : Adjustment factor for FAO-adjustment soil water depletion (p) by ETo" in content
    assert "3         : Number of days after which deficient aeration is fully effective" in content
    assert "1.00      : Exponent of senescence factor adjusting drop in photosynthetic activity of dying crop" in content
    assert "12         : Decrease of p(sen) once early canopy senescence is triggered (% of p(sen))" in content
    assert "10         : Thickness top soil (cm) in which soil water depletion has to be determined" in content
    
    # Check soil parameters
    assert "30         : Depth [cm] of soil profile affected by water extraction by soil evaporation" in content
    assert "0.30      : Considered depth (m) of soil profile for calculation of mean soil water content for CN adjustment" in content
    assert "1         : CN is adjusted to Antecedent Moisture Class" in content
    assert "20         : Salt diffusion factor (capacity for salt diffusion in micro pores) [%]" in content
    assert "100         : Salt solubility [g/liter]" in content
    assert "16         : Shape factor for effect of soil water content gradient on capillary rise" in content
    
    # Check temperature parameters
    assert "12.0       : Default minimum temperature (degC) if no temperature file is specified" in content
    assert "28.0       : Default maximum temperature (degC) if no temperature file is specified" in content
    assert "3         : Default method for the calculation of growing degree days" in content
    
    # Check rainfall parameters
    assert "1         : Daily rainfall is estimated by USDA-SCS procedure (when input is 10-day/monthly rainfall)" in content
    assert "70         : Percentage of effective rainfall (when input is 10-day/monthly rainfall)" in content
    assert "2         : Number of showers in a decade for run-off estimate (when input is 10-day/monthly rainfall)" in content
    assert "5         : Parameter for reduction of soil evaporation (when input is 10-day/monthly rainfall)" in content

def test_parameter_file_custom_values(temp_dir):
    test_file = os.path.join(temp_dir, "test_custom_params.pp1")
    
    # Define custom parameters
    custom_params = {
        'evaporation_decline_factor': 6,
        'kex': 1.20,
        'cc_threshold_for_hi': 8,
        'root_expansion_start_depth': 75,
        'max_root_expansion': 6.00,
        'shape_root_water_stress': -8,
        'germination_soil_water': 25,
        'fao_adjustment_factor': 1.2,
        'aeration_days': 4,
        'senescence_factor': 1.50,
        'senescence_reduction': 15,
        'top_soil_thickness': 12,
        'evaporation_depth': 35,
        'cn_depth': 0.40,
        'cn_adjustment': 0,  # No adjustment
        'salt_diffusion_factor': 30,
        'salt_solubility': 120,
        'soil_water_gradient_factor': 20,
        'default_min_temp': 10.0,
        'default_max_temp': 30.0,
        'gdd_method': 2,
        'rainfall_estimation': 2,  # Fixed percentage
        'effective_rainfall_pct': 80,
        'showers_per_decade': 3,
        'soil_evaporation_reduction': 7
    }
    
    # Generate the file with custom parameters
    generate_parameter_file(
        file_path=test_file,
        params=custom_params
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check custom parameter values
    assert "6         : Evaporation decline factor for stage II" in content
    assert "1.20      : Ke(x) Soil evaporation coefficient for fully wet and non-shaded soil surface" in content
    assert "8         : Threshold for green CC below which HI can no longer increase (% cover)" in content
    assert "75         : Starting depth of root zone expansion curve (% of Zmin)" in content
    assert "6.00      : Maximum allowable root zone expansion (fixed at 5 cm/day)" in content
    assert "-8         : Shape factor for effect water stress on root zone expansion" in content
    assert "25         : Required soil water content in top soil for germination (% TAW)" in content
    assert "1.2       : Adjustment factor for FAO-adjustment soil water depletion (p) by ETo" in content
    assert "4         : Number of days after which deficient aeration is fully effective" in content
    assert "1.50      : Exponent of senescence factor adjusting drop in photosynthetic activity of dying crop" in content
    assert "15         : Decrease of p(sen) once early canopy senescence is triggered (% of p(sen))" in content
    assert "12         : Thickness top soil (cm) in which soil water depletion has to be determined" in content
    
    # Check custom soil parameters
    assert "35         : Depth [cm] of soil profile affected by water extraction by soil evaporation" in content
    assert "0.40      : Considered depth (m) of soil profile for calculation of mean soil water content for CN adjustment" in content
    assert "0         : CN is adjusted to Antecedent Moisture Class" in content  # No adjustment
    assert "30         : Salt diffusion factor (capacity for salt diffusion in micro pores) [%]" in content
    assert "120         : Salt solubility [g/liter]" in content
    assert "20         : Shape factor for effect of soil water content gradient on capillary rise" in content
    
    # Check custom temperature parameters
    assert "10.0       : Default minimum temperature (degC) if no temperature file is specified" in content
    assert "30.0       : Default maximum temperature (degC) if no temperature file is specified" in content
    assert "2         : Default method for the calculation of growing degree days" in content
    
    # Check custom rainfall parameters
    assert "2         : Daily rainfall is estimated by USDA-SCS procedure (when input is 10-day/monthly rainfall)" in content
    assert "80         : Percentage of effective rainfall (when input is 10-day/monthly rainfall)" in content
    assert "3         : Number of showers in a decade for run-off estimate (when input is 10-day/monthly rainfall)" in content
    assert "7         : Parameter for reduction of soil evaporation (when input is 10-day/monthly rainfall)" in content

def test_parameter_file_partial_customization(temp_dir):
    test_file = os.path.join(temp_dir, "test_partial_params.ppn")
    
    # Define only a few custom parameters
    partial_params = {
        'evaporation_decline_factor': 5,
        'kex': 1.15,
        'default_min_temp': 8.0,
        'default_max_temp': 25.0
    }
    
    # Generate the file with partial custom parameters
    generate_parameter_file(
        file_path=test_file,
        params=partial_params
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check the custom parameter values
    assert "5         : Evaporation decline factor for stage II" in content
    assert "1.15      : Ke(x) Soil evaporation coefficient for fully wet and non-shaded soil surface" in content
    assert "8.0       : Default minimum temperature (degC) if no temperature file is specified" in content
    assert "25.0       : Default maximum temperature (degC) if no temperature file is specified" in content
    
    # Check that other parameters have default values
    assert "5         : Threshold for green CC below which HI can no longer increase (% cover)" in content
    assert "70         : Starting depth of root zone expansion curve (% of Zmin)" in content
    assert "5.00      : Maximum allowable root zone expansion (fixed at 5 cm/day)" in content
    assert "20         : Required soil water content in top soil for germination (% TAW)" in content
    assert "70         : Percentage of effective rainfall (when input is 10-day/monthly rainfall)" in content

def test_parameter_file_extreme_values(temp_dir):
    test_file = os.path.join(temp_dir, "test_extreme_params.pp1")
    
    # Define parameters with extreme values
    extreme_params = {
        'evaporation_decline_factor': 10,
        'kex': 2.00,
        'cc_threshold_for_hi': 20,
        'root_expansion_start_depth': 100,
        'max_root_expansion': 10.00,
        'shape_root_water_stress': -20,
        'germination_soil_water': 50,
        'fao_adjustment_factor': 2.0,
        'aeration_days': 10,
        'senescence_factor': 5.00,
        'senescence_reduction': 50,
        'top_soil_thickness': 50,
        'evaporation_depth': 100,
        'cn_depth': 1.00,
        'salt_diffusion_factor': 100,
        'salt_solubility': 500,
        'soil_water_gradient_factor': 50,
        'default_min_temp': 0.0,
        'default_max_temp': 40.0,
        'effective_rainfall_pct': 100,
        'showers_per_decade': 10,
        'soil_evaporation_reduction': 20
    }
    
    # Generate the file with extreme parameters
    generate_parameter_file(
        file_path=test_file,
        params=extreme_params
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check the extreme parameter values
    assert "10         : Evaporation decline factor for stage II" in content
    assert "2.00      : Ke(x) Soil evaporation coefficient for fully wet and non-shaded soil surface" in content
    assert "20         : Threshold for green CC below which HI can no longer increase (% cover)" in content
    assert "100         : Starting depth of root zone expansion curve (% of Zmin)" in content
    assert "10.00      : Maximum allowable root zone expansion (fixed at 5 cm/day)" in content
    assert "-20         : Shape factor for effect water stress on root zone expansion" in content
    assert "50         : Required soil water content in top soil for germination (% TAW)" in content
    assert "2.0       : Adjustment factor for FAO-adjustment soil water depletion (p) by ETo" in content
    assert "10         : Number of days after which deficient aeration is fully effective" in content
    assert "5.00      : Exponent of senescence factor adjusting drop in photosynthetic activity of dying crop" in content
    assert "50         : Decrease of p(sen) once early canopy senescence is triggered (% of p(sen))" in content
    assert "50         : Thickness top soil (cm) in which soil water depletion has to be determined" in content
    assert "100         : Depth [cm] of soil profile affected by water extraction by soil evaporation" in content
    assert "1.00      : Considered depth (m) of soil profile for calculation of mean soil water content for CN adjustment" in content
    assert "100         : Salt diffusion factor (capacity for salt diffusion in micro pores) [%]" in content
    assert "500         : Salt solubility [g/liter]" in content
    assert "50         : Shape factor for effect of soil water content gradient on capillary rise" in content
    assert "0.0       : Default minimum temperature (degC) if no temperature file is specified" in content
    assert "40.0       : Default maximum temperature (degC) if no temperature file is specified" in content
    assert "100         : Percentage of effective rainfall (when input is 10-day/monthly rainfall)" in content
    assert "10         : Number of showers in a decade for run-off estimate (when input is 10-day/monthly rainfall)" in content
    assert "20         : Parameter for reduction of soil evaporation (when input is 10-day/monthly rainfall)" in content