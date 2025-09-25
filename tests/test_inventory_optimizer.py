import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from inventory_optimizer import InventoryOptimizer

class TestInventoryOptimizer(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.optimizer = InventoryOptimizer()
        self.optimizer.load_data()  # Load sample data
    
    def test_initialization(self):
        """Test if the optimizer initializes correctly."""
        self.assertIsNotNone(self.optimizer)
        self.assertIsNone(self.optimizer.orders_data)  # Before loading data
        
        optimizer = InventoryOptimizer()
        optimizer.load_data()
        self.assertIsNotNone(optimizer.orders_data)
        self.assertIsNotNone(optimizer.inventory_data)
        self.assertIsNotNone(optimizer.recipes_data)
    
    def test_sample_data_creation(self):
        """Test if sample data is created correctly."""
        self.assertFalse(self.optimizer.orders_data.empty)
        self.assertFalse(self.optimizer.inventory_data.empty)
        self.assertFalse(self.optimizer.recipes_data.empty)
        
        # Check data structure
        required_order_columns = ['date', 'dish_name', 'quantity_sold', 'revenue']
        for col in required_order_columns:
            self.assertIn(col, self.optimizer.orders_data.columns)
        
        required_inventory_columns = ['material_name', 'current_stock', 'unit', 'expiry_date', 'cost_per_unit', 'minimum_stock_level']
        for col in required_inventory_columns:
            self.assertIn(col, self.optimizer.inventory_data.columns)
        
        required_recipe_columns = ['dish_name', 'material_name', 'quantity_needed']
        for col in required_recipe_columns:
            self.assertIn(col, self.optimizer.recipes_data.columns)
    
    def test_demand_forecasting(self):
        """Test demand forecasting functionality."""
        forecast = self.optimizer.forecast_demand(days_ahead=7)
        
        self.assertFalse(forecast.empty)
        self.assertEqual(len(forecast['date'].unique()), 7)
        self.assertTrue(all(forecast['predicted_quantity'] >= 0))
        
        # Check if seasonal factors are applied
        required_columns = ['date', 'dish_name', 'predicted_quantity', 'seasonal_factor', 'weekend_factor']
        for col in required_columns:
            self.assertIn(col, forecast.columns)
    
    def test_material_requirements_calculation(self):
        """Test material requirements calculation."""
        forecast = self.optimizer.forecast_demand(days_ahead=3)
        requirements = self.optimizer.calculate_material_requirements(forecast)
        
        self.assertFalse(requirements.empty)
        self.assertTrue(all(requirements['total_material_needed'] >= 0))
        
        required_columns = ['date', 'material_name', 'total_material_needed']
        for col in required_columns:
            self.assertIn(col, requirements.columns)
    
    def test_restocking_needs_calculation(self):
        """Test restocking needs calculation."""
        forecast = self.optimizer.forecast_demand(days_ahead=7)
        requirements = self.optimizer.calculate_material_requirements(forecast)
        restocking = self.optimizer.calculate_restocking_needs(requirements)
        
        # Restocking data might be empty if no restocking is needed
        if not restocking.empty:
            self.assertTrue(all(restocking['needs_restocking']))
            self.assertTrue(all(restocking['restock_quantity'] > 0))
            self.assertTrue(all(restocking['restock_cost'] >= 0))
    
    def test_near_expiry_materials(self):
        """Test near expiry materials identification."""
        near_expiry = self.optimizer.find_near_expiry_materials(days_threshold=30)  # Use longer threshold for testing
        
        # Near expiry data might be empty
        if not near_expiry.empty:
            self.assertTrue(all(near_expiry['days_until_expiry'] <= 30))
            self.assertTrue(all(near_expiry['current_stock'] >= 0))
    
    def test_optimization_report_generation(self):
        """Test comprehensive optimization report generation."""
        report = self.optimizer.generate_optimization_report()
        
        self.assertIsInstance(report, dict)
        
        required_keys = ['summary', 'demand_forecast', 'material_requirements', 'restocking_needs', 'near_expiry_materials']
        for key in required_keys:
            self.assertIn(key, report)
        
        # Test summary structure
        summary = report['summary']
        required_summary_keys = ['forecast_period_days', 'total_restock_cost', 'materials_to_restock', 'materials_near_expiry', 'report_generated']
        for key in required_summary_keys:
            self.assertIn(key, summary)
        
        self.assertEqual(summary['forecast_period_days'], 7)
        self.assertGreaterEqual(summary['total_restock_cost'], 0)
        self.assertGreaterEqual(summary['materials_to_restock'], 0)
        self.assertGreaterEqual(summary['materials_near_expiry'], 0)
    
    def test_seasonal_factors(self):
        """Test seasonal factors functionality."""
        self.assertIsNotNone(self.optimizer.seasonal_factors)
        self.assertIn('factors', self.optimizer.seasonal_factors)
        self.assertIn('winter_months', self.optimizer.seasonal_factors)
        self.assertIn('weekend_factor', self.optimizer.seasonal_factors)
    
    def test_data_validation(self):
        """Test data validation and error handling."""
        # Test with unloaded data
        empty_optimizer = InventoryOptimizer()
        
        with self.assertRaises(ValueError):
            empty_optimizer.forecast_demand()
        
        with self.assertRaises(ValueError):
            empty_optimizer.find_near_expiry_materials()
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with zero days forecast
        forecast_zero = self.optimizer.forecast_demand(days_ahead=0)
        self.assertTrue(forecast_zero.empty)
        
        # Test with large forecast period
        forecast_large = self.optimizer.forecast_demand(days_ahead=365)
        self.assertEqual(len(forecast_large['date'].unique()), 365)
        
        # Test with zero threshold for expiry
        near_expiry_zero = self.optimizer.find_near_expiry_materials(days_threshold=0)
        # Should return materials expiring today or already expired

class TestDataIntegrity(unittest.TestCase):
    """Test data integrity and consistency."""
    
    def setUp(self):
        self.optimizer = InventoryOptimizer()
        self.optimizer.load_data()
    
    def test_data_consistency(self):
        """Test data consistency across different datasets."""
        # Check if all dishes in orders exist in recipes
        order_dishes = set(self.optimizer.orders_data['dish_name'].unique())
        recipe_dishes = set(self.optimizer.recipes_data['dish_name'].unique())
        
        # At least some dishes should have recipes
        self.assertTrue(len(order_dishes.intersection(recipe_dishes)) > 0)
        
        # Check if all materials in recipes exist in inventory
        recipe_materials = set(self.optimizer.recipes_data['material_name'].unique())
        inventory_materials = set(self.optimizer.inventory_data['material_name'].unique())
        
        # At least some materials should exist in both
        self.assertTrue(len(recipe_materials.intersection(inventory_materials)) > 0)
    
    def test_data_types(self):
        """Test if data types are correct."""
        # Orders data types
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(pd.to_datetime(self.optimizer.orders_data['date'])))
        self.assertTrue(pd.api.types.is_numeric_dtype(self.optimizer.orders_data['quantity_sold']))
        self.assertTrue(pd.api.types.is_numeric_dtype(self.optimizer.orders_data['revenue']))
        
        # Inventory data types
        self.assertTrue(pd.api.types.is_numeric_dtype(self.optimizer.inventory_data['current_stock']))
        self.assertTrue(pd.api.types.is_numeric_dtype(self.optimizer.inventory_data['cost_per_unit']))
        self.assertTrue(pd.api.types.is_numeric_dtype(self.optimizer.inventory_data['minimum_stock_level']))
        
        # Recipe data types
        self.assertTrue(pd.api.types.is_numeric_dtype(self.optimizer.recipes_data['quantity_needed']))
    
    def test_data_ranges(self):
        """Test if data values are within expected ranges."""
        # Quantities should be non-negative
        self.assertTrue(all(self.optimizer.orders_data['quantity_sold'] >= 0))
        self.assertTrue(all(self.optimizer.inventory_data['current_stock'] >= 0))
        self.assertTrue(all(self.optimizer.recipes_data['quantity_needed'] > 0))
        
        # Costs should be positive
        self.assertTrue(all(self.optimizer.inventory_data['cost_per_unit'] > 0))
        self.assertTrue(all(self.optimizer.orders_data['revenue'] >= 0))

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)