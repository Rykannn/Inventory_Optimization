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
    
    # Create visualizations
    print("\n4. Generating visualizations...")
    
    try:
        # Create data directory for outputs
        os.makedirs('data/outputs', exist_ok=True)
        
        print("   ✓ Creating demand forecast plot...")
        visualizer.plot_demand_forecast(report['demand_forecast'], 'data/outputs/demand_forecast.png')
        
        print("   ✓ Creating inventory status plot...")
        visualizer.plot_inventory_status(optimizer.inventory_data, 'data/outputs/inventory_status.png')
        
        if not report['restocking_needs'].empty:
            print("   ✓ Creating restocking analysis plot...")
            visualizer.plot_restocking_analysis(report['restocking_needs'], 'data/outputs/restocking_analysis.png')
        
        if not report['near_expiry_materials'].empty:
            print("   ✓ Creating near-expiry materials plot...")
            visualizer.plot_near_expiry_materials(report['near_expiry_materials'], 'data/outputs/near_expiry.png')
        
        print("   ✓ Creating seasonal trends plot...")
        visualizer.plot_seasonal_trends(optimizer.orders_data, 'data/outputs/seasonal_trends.png')
        
        # Create interactive dashboard if plotly is available
        try:
            print("   ✓ Creating interactive dashboard...")
            dashboard = visualizer.create_interactive_dashboard(report)
            dashboard.write_html('data/outputs/interactive_dashboard.html')
            print("   ✓ Interactive dashboard saved as HTML")
        except ImportError:
            print("   ! Plotly not available - skipping interactive dashboard")
            
    except Exception as e:
        print(f"   ! Warning: Some visualizations failed to generate: {str(e)}")
    
    # Save reports to CSV
    print("\n5. Saving detailed reports...")
    try:
        report['demand_forecast'].to_csv('data/outputs/demand_forecast.csv', index=False)
        if not report['restocking_needs'].empty:
            report['restocking_needs'].to_csv('data/outputs/restocking_needs.csv', index=False)
        if not report['near_expiry_materials'].empty:
            report['near_expiry_materials'].to_csv('data/outputs/near_expiry_materials.csv', index=False)
        optimizer.inventory_data.to_csv('data/outputs/current_inventory.csv', index=False)
        print("   ✓ All reports saved to 'data/outputs/' directory")
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
    print("Report complete! Check 'data/outputs/' for detailed files.")
    print("="*60)

if __name__ == "__main__":
    main()