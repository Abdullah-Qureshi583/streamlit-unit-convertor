
import streamlit as st

UNITS = {
    "Length": {
        "Meter": 1,          # Base unit for length
        "Kilometer": 1000,   # 1 km = 1000 m
        "Centimeter": 0.01,  # 1 cm = 0.01 m
        "Millimeter": 0.001, # 1 mm = 0.001 m
        "Mile": 1609.34,     # 1 mile = 1609.34 m
        "Yard": 0.9144,      # 1 yard = 0.9144 m
        "Foot": 0.3048,      # 1 foot = 0.3048 m
        "Inch": 0.0254       # 1 inch = 0.0254 m
    },
    "Weight": {
        "Kilogram": 1,       # Base unit for weight
        "Gram": 0.001,       # 1 g = 0.001 kg
        "Milligram": 0.000001, # 1 mg = 0.000001 kg
        "Pound": 0.453592,   # 1 lb = 0.453592 kg
        "Ounce": 0.0283495   # 1 oz = 0.0283495 kg
    },
    "Temperature": {
        "Celsius": "C",      # Temperature units use special conversion
        "Fahrenheit": "F",   # as they have different zero points
        "Kelvin": "K"
    }
}

def convert_temperature(value:float, from_unit:float, to_unit):
    """
    Convert temperature between different scales (Celsius, Fahrenheit, Kelvin)
    
    Args:
        value (float): The temperature value to convert
        from_unit (str): The source temperature unit
        to_unit (str): The target temperature unit
    
    Returns:
        float: The converted temperature value
    """
    # If units are the same, return the original value
    if from_unit == to_unit:
        return value
    
    # First convert to Celsius as our intermediate unit
    # Base unit is Celcius
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        celsius = value
    
    # Then convert from Celsius to the target unit
    if to_unit == "Fahrenheit":
        return (celsius * 9/5) + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    return celsius

def convert_unit(value, unit_from, unit_to, unit_type):
    """
    Convert a value between different units of the same type
    
    Args:
        value (float): The value to convert
        unit_from (str): The source unit
        unit_to (str): The target unit
        unit_type (str): The type of unit (Length, Weight, Temperature)
    
    Returns:
        float: The converted value
    """
    # Special handling for temperature conversions
    if unit_type == "Temperature":
        return convert_temperature(value, unit_from, unit_to)
    
    # For other unit types, convert using the conversion factors
    # First convert to base unit, then to target unit
    base_value = value * UNITS[unit_type][unit_from]
    return base_value / UNITS[unit_type][unit_to]

def main():
    """
    Main function to create and run the Streamlit web interface
    """
    # Configure the Streamlit page
    st.set_page_config(
        page_title="Unit Converter",
        page_icon="🔄",
        layout="centered"
    )
    
    # Display the main title and description
    st.title("📐 Unit Converter")
    st.write("Convert between different units of measurement")
    
    # Create a dropdown for selecting the type of unit to convert
    unit_type = st.selectbox(
        "Select Unit Type",
        options=list(UNITS.keys()),
        key="unit_type"
        
    )
    
    # Create two columns for the input and output sections
    col1, col2 = st.columns(2)
    
    # Left column: Input section
    with col1:
        st.subheader("From")
        # Number input field for the value to convert
        input_value = st.number_input(
            "Enter Value",
            value=0.0,
            format="%f"
        )
        # Dropdown for selecting the source unit
        from_unit = st.selectbox(
            label   ="From Unit",
            options=list(UNITS[unit_type].keys()),
            key="from_unit"
        )
    
    # Right column: Output section
    with col2:
        st.subheader("To")
        # Dropdown for selecting the target unit
        to_unit = st.selectbox(
            "To Unit",
            options=list(UNITS[unit_type].keys()),
            key="to_unit"
        )
        
    # Perform the conversion and display results
    try:
        result = convert_unit(input_value, from_unit, to_unit, unit_type)
        
        # Display the conversion result in a formatted way
        st.markdown("---")
        st.subheader("Result")
        col3, col4 = st.columns([2, 3])
        
        with col3:
            st.info(f"{input_value:,.4f} {from_unit}")
        with col4:
            st.success(f"= {result:,.4f} {to_unit}")
            
    except Exception as e:
        st.error(f"Error in conversion: {str(e)}")
    
    # Add an expandable section with information about supported units
    with st.expander("ℹ️ About"):
        st.write("""
        This unit converter supports:
        - Length (m, km, cm, mm, mile, yard, foot, inch)
        - Weight (kg, g, mg, lb, oz)
        - Temperature (°C, °F, K)
        
        Values are rounded to 4 decimal places for display.
        """)

# Entry point of the application
if __name__ == "__main__":
    main()
    
