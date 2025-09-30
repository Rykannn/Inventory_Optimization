# Inventory Optimization Project

## 🧮 Algorithms Used

### 1. **Demand Forecasting Algorithm**
- **Type**: Time Series-based Historical Average with Seasonal Adjustments
- **Location**: `forecast_demand()` method in `inventory_optimizer.py`
- **Approach**:
  - Calculates the historical average daily demand for each dish using `groupby().mean()`
  - Applies seasonal factors:
    - Winter: 1.3x
    - Summer: 1.1x
    - Spring/Fall: 1.0x
  - Applies a weekend multiplier (1.2x for weekends)
  - Uses Poisson distribution for realistic demand variation in sample data generation

### 2. **Material Requirements Planning (MRP)**
- **Type**: Bill of Materials (BOM) Explosion Algorithm
- **Location**: `calculate_material_requirements()` method
- **Approach**:
  - Merges demand forecast with recipe data
  - Multiplies predicted dish quantities by material requirements per dish
  - Aggregates total material needs across all dishes and dates

### 3. **Inventory Restocking Algorithm**
- **Type**: Economic Order Quantity (EOQ) with Safety Stock
- **Location**: `calculate_restocking_needs()` method
- **Approach**:
  - Calculates shortage: `required_materials - current_stock`
  - Considers minimum stock levels as safety stock
  - Uses `np.maximum()` to ensure restocking meets both shortage and minimum levels
  - Prioritizes by cost (descending order)

### 4. **Expiry Management Algorithm**
- **Type**: First Expired, First Out (FEFO) with Optimization
- **Location**: `find_near_expiry_materials()` method
- **Approach**:
  - Filters materials by expiry threshold (default: 3 days)
  - Calculates the maximum number of dishes that can be prepared with available stock
  - Sorts by urgency (days until expiry)
  - Suggests optimal dish utilization to minimize waste

### 5. **Data Generation Algorithms**
- **Poisson Process**: For realistic demand simulation
- **Seasonal Modeling**: Month-based demand patterns
- **Random Distribution**: For inventory attributes (stock levels, costs, expiry dates)

## Optimization Strategies
- **Multi-objective Optimization**:
  - Minimize waste (expiry management)
  - Minimize stockouts (adequate inventory)
  - Minimize costs (efficient restocking)

## Visualization Algorithms
- **Data Aggregation**: `groupby()` operations for trend analysis
- **Pivot Tables**: For multi-dimensional data visualization
- **Statistical Analysis**: Monthly/weekly trend calculations
- **Color-coded Priority Systems**: Red/Orange/Green for urgency levels

## Mathematical Foundations
- **Algorithm Complexity**:
  - **Time Complexity**: O(n×m) where `n` = number of dishes, `m` = forecast days
  - **Space Complexity**: O(n×m×k) where `k` = number of materials
  - **Scalability**: Linear scaling with data size

## Key Features
- ✅ **Reactive**: Responds to current inventory levels
- ✅ **Predictive**: Uses historical data for forecasting
- ✅ **Seasonal-aware**: Adjusts for seasonal demand patterns
- ✅ **Cost-optimized**: Prioritizes by financial impact
- ✅ **Waste-minimizing**: FEFO expiry management

---

This system uses classical inventory management algorithms, focusing on practicality, interpretability, and suitability for small to medium F&B operations. The algorithms are deterministic and rule-based, ensuring consistent and explainable results. Advanced ML techniques are not used, making it easier to maintain and scale across various types of inventory systems.
