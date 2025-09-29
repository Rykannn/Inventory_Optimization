from src.inventory_optimizer import InventoryOptimizer
from src.visualizer import InventoryVisualizer
import pandas as pd
import numpy as np
from datetime import datetime
import os

def main():
    """
    Main function to demonstrate the inventory optimization system.
    """
    print("="*60)
    print("           INVENTORY OPTIMIZATION SYSTEM")
    print("           F&B Industry Solution")
    print("="*60)
    
    # Initialize the system
    print("\n1. Initializing Inventory Optimization System...")
    optimizer = InventoryOptimizer()
    visualizer = InventoryVisualizer()
    
    # Load data (using sample data for demonstration)
    print("2. Loading sample data...")
    optimizer.load_data()
    print(f"   ✓ Loaded {len(optimizer.orders_data)} order records")
    print(f"   ✓ Loaded {len(optimizer.inventory_data)} inventory items")
    print(f"   ✓ Loaded {len(optimizer.recipes_data)} recipe entries")
    
    # Generate comprehensive report
    print("\n3. Generating optimization report...")
    report = optimizer.generate_optimization_report()
    
    # Display summary
    print("\n" + "="*50)
    print("           OPTIMIZATION SUMMARY")
    print("="*50)
    summary = report['summary']
    print(f"Report Generated: {summary['report_generated']}")
    print(f"Forecast Period: {summary['forecast_period_days']} days")
    print(f"Materials Requiring Restock: {summary['materials_to_restock']}")
    print(f"Materials Near Expiry: {summary['materials_near_expiry']}")
    print(f"Recommended Dishes: {summary['recommended_dishes']}")
    print(f"Total Restocking Cost: ${summary['total_restock_cost']:.2f}")
    
    # Display demand forecast
    print("\n" + "-"*50)
    print("           7-DAY DEMAND FORECAST")
    print("-"*50)
    forecast_summary = report['demand_forecast'].groupby('dish_name')['predicted_quantity'].sum().sort_values(ascending=False)
    for dish, quantity in forecast_summary.items():
        print(f"{dish:20s}: {quantity:3d} servings")
    
    # Display restocking needs
    if not report['restocking_needs'].empty:
        print("\n" + "-"*50)
        print("           RESTOCKING REQUIREMENTS")
        print("-"*50)
        restock_data = report['restocking_needs'][['material_name', 'restock_quantity', 'restock_cost']].head(10)
        for _, row in restock_data.iterrows():
            print(f"{row['material_name']:20s}: {row['restock_quantity']:6.1f} units (${row['restock_cost']:7.2f})")
    else:
        print("\n✓ No immediate restocking required!")
    
    # Display near-expiry materials
    if not report['near_expiry_materials'].empty:
        print("\n" + "-"*50)
        print("           MATERIALS NEAR EXPIRY")
        print("-"*50)
        expiry_data = report['near_expiry_materials'][['material_name', 'days_until_expiry', 'dish_name', 'max_dishes_possible']].drop_duplicates()
        for _, row in expiry_data.iterrows():
            if pd.notna(row['dish_name']):
                print(f"{row['material_name']:20s}: {row['days_until_expiry']:2d} days → Use in {row['dish_name']} ({row['max_dishes_possible']} max servings)")
    else:
        print("\n✓ No materials near expiry!")
    
    # Display dish recommendations
    if not report['dish_recommendations'].empty:
        print("\n" + "-"*50)
        print("           RECOMMENDED DISHES")
        print("-"*50)
        recommendations = report['dish_recommendations'].head(5)
        for _, row in recommendations.iterrows():
            expiry_info = " (🔥 Uses expiring materials)" if row['uses_expiring_materials'] else ""
            expiring_materials = ", ".join(row['expiring_materials_used']) if row['expiring_materials_used'] else "None"
            print(f"{row['dish_name']:20s}: Score {row['recommendation_score']:.2f} | Max {row['max_servings_possible']:3d} servings | ${row['cost_per_serving']:.2f}/serving{expiry_info}")
            if row['expiring_materials_used']:
                print(f"{'':21s}  → Uses expiring: {expiring_materials}")
        print(f"\n   Season: {recommendations.iloc[0]['season'].title()} | Weather-based preferences applied")
    else:
        print("\n! No dish recommendations available!")

    # Create visualizations
    print("\n4. Generating visualizations...")
    
    try:
        # Create png directory for outputs
        os.makedirs('data/png', exist_ok=True)
        
        print("   ✓ Creating demand forecast plot...")
        visualizer.plot_demand_forecast(report['demand_forecast'], 'data/png/demand_forecast.png')
        
        print("   ✓ Creating inventory status plot...")
        visualizer.plot_inventory_status(optimizer.inventory_data, 'data/png/inventory_status.png')
        
        if not report['restocking_needs'].empty:
            print("   ✓ Creating restocking analysis plot...")
            visualizer.plot_restocking_analysis(report['restocking_needs'], 'data/png/restocking_analysis.png')
        
        if not report['near_expiry_materials'].empty:
            print("   ✓ Creating near-expiry materials plot...")
            visualizer.plot_near_expiry_materials(report['near_expiry_materials'], 'data/png/near_expiry.png')
        
        print("   ✓ Creating seasonal trends plot...")
        visualizer.plot_seasonal_trends(optimizer.orders_data, 'data/png/seasonal_trends.png')
        
        if not report['dish_recommendations'].empty:
            print("   ✓ Creating dish recommendations plot...")
            visualizer.plot_dish_recommendations(report['dish_recommendations'], 'data/png/dish_recommendations.png')
        

            
    except Exception as e:
        print(f"   ! Warning: Some visualizations failed to generate: {str(e)}")
    
    # Save reports to CSV
    print("\n5. Saving detailed reports...")
    try:
        # Create csv directory for outputs
        os.makedirs('data/csv', exist_ok=True)
        
        report['demand_forecast'].to_csv('data/csv/demand_forecast.csv', index=False)
        if not report['restocking_needs'].empty:
            report['restocking_needs'].to_csv('data/csv/restocking_needs.csv', index=False)
        if not report['near_expiry_materials'].empty:
            report['near_expiry_materials'].to_csv('data/csv/near_expiry_materials.csv', index=False)
        if not report['dish_recommendations'].empty:
            report['dish_recommendations'].to_csv('data/csv/dish_recommendations.csv', index=False)
        optimizer.inventory_data.to_csv('data/csv/current_inventory.csv', index=False)
        print("   ✓ All reports saved to 'data/csv/' directory")
    except Exception as e:
        print(f"   ! Error saving reports: {str(e)}")
    
    # Provide recommendations
    print("\n" + "="*50)
    print("           RECOMMENDATIONS")
    print("="*50)
    
    if summary['materials_to_restock'] > 0:
        print(f"🔴 URGENT: {summary['materials_to_restock']} materials need restocking")
        print(f"   Total investment required: ${summary['total_restock_cost']:.2f}")
    
    if summary['materials_near_expiry'] > 0:
        print(f"🟡 WARNING: {summary['materials_near_expiry']} materials expire soon")
        print("   Prioritize dishes using these materials to minimize waste")
    
    if summary['materials_to_restock'] == 0 and summary['materials_near_expiry'] == 0:
        print("🟢 GOOD: Inventory levels are optimal!")
        print("   Continue monitoring and maintain current stock levels")
    
    print("\n" + "="*60)
    print("Report complete! Check 'data/csv/' for CSV files and 'data/png/' for charts.")
    print("="*60)

if __name__ == "__main__":
    main()