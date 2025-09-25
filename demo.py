"""
Quick Demo Script for Inventory Optimization System
Run this for a fast demonstration of key features.
"""

from src.inventory_optimizer import InventoryOptimizer

def quick_demo():
    print("🚀 INVENTORY OPTIMIZATION - QUICK DEMO")
    print("=" * 45)
    
    # Initialize system
    optimizer = InventoryOptimizer()
    optimizer.load_data()
    
    # Show data loaded
    print(f"📊 Data Loaded:")
    print(f"   • {len(optimizer.orders_data):,} order records")
    print(f"   • {len(optimizer.inventory_data)} inventory items")
    print(f"   • {len(optimizer.recipes_data)} recipe entries")
    
    # Quick forecast
    print(f"\n📈 7-Day Demand Forecast:")
    forecast = optimizer.forecast_demand(7)
    top_dishes = forecast.groupby('dish_name')['predicted_quantity'].sum().nlargest(3)
    for dish, qty in top_dishes.items():
        print(f"   • {dish}: {qty} servings")
    
    # Check inventory alerts
    near_expiry = optimizer.find_near_expiry_materials(3)
    if not near_expiry.empty:
        print(f"\n⚠️  Materials expiring in ≤3 days:")
        for material in near_expiry['material_name'].unique()[:3]:
            print(f"   • {material}")
    
    # Generate quick report
    report = optimizer.generate_optimization_report()
    summary = report['summary']
    
    print(f"\n💰 Financial Summary:")
    print(f"   • Restocking cost: ${summary['total_restock_cost']:.2f}")
    print(f"   • Materials to restock: {summary['materials_to_restock']}")
    
    # Recommendations
    print(f"\n🎯 Quick Recommendations:")
    if summary['materials_to_restock'] > 0:
        print(f"   🔴 {summary['materials_to_restock']} materials need restocking")
    if summary['materials_near_expiry'] > 0:
        print(f"   🟡 {summary['materials_near_expiry']} materials expire soon")
    if summary['materials_to_restock'] == 0 and summary['materials_near_expiry'] == 0:
        print(f"   🟢 Inventory levels optimal!")
    
    print("\n✅ Demo complete! Run 'python main.py' for full analysis.")
    print("📁 Check 'data/outputs/' for detailed reports and charts.")

if __name__ == "__main__":
    quick_demo()