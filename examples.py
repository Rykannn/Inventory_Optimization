#!/usr/bin/env python3
"""
Example usage script for the Inventory Optimization System.
This script demonstrates various ways to use the system components.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.inventory_optimizer import InventoryOptimizer
from src.visualizer import InventoryVisualizer
import pandas as pd
from datetime import datetime, timedelta

def example_basic_usage():
    """Basic usage example."""
    print("=== BASIC USAGE EXAMPLE ===\n")
    
    # Initialize the system
    optimizer = InventoryOptimizer()
    optimizer.load_data()
    
    # Get 3-day forecast
    forecast = optimizer.forecast_demand(days_ahead=3)
    print("3-Day Demand Forecast:")
    print(forecast.groupby('dish_name')['predicted_quantity'].sum().to_string())
    
    # Check materials near expiry
    near_expiry = optimizer.find_near_expiry_materials(days_threshold=5)
    if not near_expiry.empty:
        print(f"\nMaterials expiring in 5 days: {len(near_expiry['material_name'].unique())}")
    else:
        print("\nNo materials expiring in the next 5 days.")

def example_custom_data():
    """Example with custom data."""
    print("\n=== CUSTOM DATA EXAMPLE ===\n")
    
    # Create custom orders data
    custom_orders = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=30, freq='D'),
        'dish_name': ['Custom Dish'] * 30,
        'quantity_sold': [10, 15, 12, 8, 20] * 6,
        'revenue': [100, 150, 120, 80, 200] * 6
    })
    
    # Create custom inventory
    custom_inventory = pd.DataFrame({
        'material_name': ['Custom Material'],
        'current_stock': [50],
        'unit': ['kg'],
        'expiry_date': [datetime.now() + timedelta(days=2)],
        'cost_per_unit': [5.0],
        'minimum_stock_level': [10]
    })
    
    # Create custom recipes
    custom_recipes = pd.DataFrame({
        'dish_name': ['Custom Dish'],
        'material_name': ['Custom Material'],
        'quantity_needed': [0.5]
    })
    
    optimizer = InventoryOptimizer()
    optimizer.orders_data = custom_orders
    optimizer.inventory_data = custom_inventory
    optimizer.recipes_data = custom_recipes
    optimizer.seasonal_factors = optimizer._create_seasonal_factors()
    
    # Generate forecast
    forecast = optimizer.forecast_demand(days_ahead=5)
    print("Custom Forecast:")
    print(forecast[['date', 'dish_name', 'predicted_quantity']].to_string(index=False))

def example_detailed_analysis():
    """Detailed analysis example."""
    print("\n=== DETAILED ANALYSIS EXAMPLE ===\n")
    
    optimizer = InventoryOptimizer()
    optimizer.load_data()
    
    # Generate comprehensive report
    report = optimizer.generate_optimization_report()
    
    print("ANALYSIS RESULTS:")
    print("-" * 40)
    
    # Analyze demand patterns
    forecast = report['demand_forecast']
    dish_totals = forecast.groupby('dish_name')['predicted_quantity'].sum().sort_values(ascending=False)
    print(f"Top 3 dishes by predicted demand:")
    for i, (dish, quantity) in enumerate(dish_totals.head(3).items()):
        print(f"{i+1}. {dish}: {quantity} servings")
    
    # Analyze restocking priorities
    if not report['restocking_needs'].empty:
        restock = report['restocking_needs']
        print(f"\nHigh-priority restocking (top 3 by cost):")
        top_restock = restock.nlargest(3, 'restock_cost')
        for _, row in top_restock.iterrows():
            print(f"- {row['material_name']}: {row['restock_quantity']:.1f} units (${row['restock_cost']:.2f})")
    
    # Analyze expiry risks
    if not report['near_expiry_materials'].empty:
        expiry = report['near_expiry_materials']
        critical_materials = expiry[expiry['days_until_expiry'] <= 2]
        if not critical_materials.empty:
            print(f"\nCRITICAL: Materials expiring in ≤2 days:")
            for material in critical_materials['material_name'].unique():
                print(f"- {material}")

def example_visualization():
    """Visualization example."""
    print("\n=== VISUALIZATION EXAMPLE ===\n")
    
    try:
        optimizer = InventoryOptimizer()
        optimizer.load_data()
        visualizer = InventoryVisualizer()
        
        # Generate sample visualizations
        print("Generating visualizations...")
        
        # Demand forecast plot
        forecast = optimizer.forecast_demand(days_ahead=7)
        print("✓ Creating demand forecast chart")
        visualizer.plot_demand_forecast(forecast)
        
        # Inventory status plot
        print("✓ Creating inventory status chart")
        visualizer.plot_inventory_status(optimizer.inventory_data)
        
        # Seasonal trends
        print("✓ Creating seasonal trends chart")
        visualizer.plot_seasonal_trends(optimizer.orders_data)
        
        print("Visualization complete!")
        
    except ImportError as e:
        print(f"Visualization libraries not available: {e}")
        print("Install matplotlib and seaborn to enable visualizations.")

def example_cost_optimization():
    """Cost optimization example."""
    print("\n=== COST OPTIMIZATION EXAMPLE ===\n")
    
    optimizer = InventoryOptimizer()
    optimizer.load_data()
    
    # Calculate different forecast periods
    periods = [3, 7, 14]
    print("Cost analysis for different forecast periods:")
    print("-" * 50)
    
    for period in periods:
        forecast = optimizer.forecast_demand(days_ahead=period)
        requirements = optimizer.calculate_material_requirements(forecast)
        restocking = optimizer.calculate_restocking_needs(requirements)
        
        total_cost = restocking['restock_cost'].sum() if not restocking.empty else 0
        materials_count = len(restocking) if not restocking.empty else 0
        
        print(f"{period:2d} days: ${total_cost:8.2f} ({materials_count:2d} materials)")
    
    # Find most cost-effective materials
    report = optimizer.generate_optimization_report()
    if not report['restocking_needs'].empty:
        restock = report['restocking_needs']
        cost_efficiency = restock['restock_quantity'] / restock['restock_cost']
        restock['cost_efficiency'] = cost_efficiency
        
        print(f"\nMost cost-efficient materials to restock:")
        efficient = restock.nlargest(3, 'cost_efficiency')
        for _, row in efficient.iterrows():
            print(f"- {row['material_name']}: {row['cost_efficiency']:.2f} units per $")

def main():
    """Run all examples."""
    print("INVENTORY OPTIMIZATION SYSTEM - EXAMPLES")
    print("=" * 50)
    
    try:
        example_basic_usage()
        example_custom_data()
        example_detailed_analysis()
        example_cost_optimization()
        example_visualization()
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure all dependencies are installed.")
    
    print("\n" + "=" * 50)
    print("Examples completed! Check the main.py for full system demo.")

if __name__ == "__main__":
    main()