# Inventory Optimization for F&B Industry

This project provides a comprehensive solution for inventory management in Food & Beverage businesses, featuring demand forecasting, restocking optimization, and waste reduction strategies.

## Features

-   **Demand Forecasting**: Predict material requirements based on historical orders and seasonal patterns
-   **Smart Restocking**: Calculate optimal reorder quantities and timing
-   **Expiry Management**: Identify materials near expiration and suggest usage strategies
-   **Data Visualization**: Interactive charts and reports for inventory insights
-   **Cost Optimization**: Minimize waste while ensuring adequate stock levels

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/inventory-optimization.git
cd inventory-optimization
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the main application:

```bash
python main.py
```

### Using Individual Components

```python
from src.inventory_optimizer import InventoryOptimizer
from src.visualizer import InventoryVisualizer

# Initialize the optimizer
optimizer = InventoryOptimizer()

# Load your data (or use sample data)
optimizer.load_data()

# Generate forecasts
forecast = optimizer.forecast_demand(days_ahead=7)

# Calculate material requirements
requirements = optimizer.calculate_material_requirements(forecast)

# Identify restocking needs
restocking = optimizer.calculate_restocking_needs(requirements)

# Find materials near expiry
near_expiry = optimizer.find_near_expiry_materials(days_threshold=3)

# Generate comprehensive report
report = optimizer.generate_optimization_report()
```

### Creating Visualizations

```python
visualizer = InventoryVisualizer()

# Plot demand forecast
visualizer.plot_demand_forecast(forecast_data)

# Show inventory status
visualizer.plot_inventory_status(inventory_data)

# Display restocking analysis
visualizer.plot_restocking_analysis(restocking_data)

# Create interactive dashboard
dashboard = visualizer.create_interactive_dashboard(report)
dashboard.show()
```

## Data Structure

### Orders Data

-   `date`: Order date
-   `dish_name`: Name of the dish
-   `quantity_sold`: Number of servings sold
-   `revenue`: Revenue generated

### Inventory Data

-   `material_name`: Name of the raw material
-   `current_stock`: Current quantity in stock
-   `unit`: Unit of measurement (kg, pieces, etc.)
-   `expiry_date`: Expiration date
-   `cost_per_unit`: Cost per unit
-   `minimum_stock_level`: Minimum required stock level

### Recipe Data

-   `dish_name`: Name of the dish
-   `material_name`: Required material
-   `quantity_needed`: Quantity needed per serving

## Output

The system generates:

1. **Console Report**: Summary of key metrics and recommendations
2. **CSV Files**: Detailed data exports in `data/outputs/`
3. **Visualizations**: Charts saved as PNG files
4. **Interactive Dashboard**: HTML file with interactive plots

## Key Metrics

-   **Forecast Accuracy**: Seasonal and trend-adjusted demand predictions
-   **Restock Optimization**: Minimize costs while avoiding stockouts
-   **Waste Reduction**: Identify materials near expiry
-   **Cost Analysis**: Track inventory investment and potential savings

## Customization

### Seasonal Factors

Modify seasonal adjustment factors in `inventory_optimizer.py`:

```python
seasonal_factors = {
    'winter': 1.3,  # 30% increase in winter
    'summer': 1.1,  # 10% increase in summer
    'weekend_factor': 1.2,  # 20% increase on weekends
}
```

### Expiry Thresholds

Adjust expiry warning periods:

```python
near_expiry = optimizer.find_near_expiry_materials(days_threshold=5)
```

## Example Output

```
==========================================================
           INVENTORY OPTIMIZATION SYSTEM
           F&B Industry Solution
==========================================================

==================================================
           OPTIMIZATION SUMMARY
==================================================
Report Generated: 2024-09-25 14:30:15
Forecast Period: 7 days
Materials Requiring Restock: 5
Materials Near Expiry: 3
Total Restocking Cost: $1,247.85

--------------------------------------------------
           7-DAY DEMAND FORECAST
--------------------------------------------------
Vegetable Salad      : 140 servings
Pasta Marinara      : 126 servings
Chicken Curry       : 105 servings
Fish Soup           :  84 servings
Beef Steak          :  70 servings

--------------------------------------------------
           RESTOCKING REQUIREMENTS
--------------------------------------------------
Mixed Vegetables    :   45.2 units ($  226.00)
Pasta              :   25.2 units ($  151.20)
Chicken Breast     :   31.5 units ($  472.50)
Tomato Sauce       :   28.7 units ($  172.20)
Fish Fillet        :   21.0 units ($  315.00)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions and support, please open an issue on GitHub or contact the development team.

## Future Enhancements

-   Machine learning models for improved demand prediction
-   Integration with POS systems and suppliers
-   Mobile app for inventory management
-   Real-time alerts and notifications
-   Multi-location inventory management
-   Supplier performance analytics
