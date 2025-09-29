import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class InventoryOptimizer:
    """
    Main class for inventory optimization in F&B industry.
    Handles demand forecasting, restocking calculations, and near-expiry material utilization.
    """
    
    def __init__(self):
        self.orders_data = None
        self.inventory_data = None
        self.recipes_data = None
        self.seasonal_factors = None
        
    def load_data(self, orders_file: str = None, inventory_file: str = None, recipes_file: str = None):
        """Load data from files or create sample data for demonstration."""
        if orders_file:
            self.orders_data = pd.read_csv(orders_file)
        else:
            self.orders_data = self._create_sample_orders_data()
            
        if inventory_file:
            self.inventory_data = pd.read_csv(inventory_file)
        else:
            self.inventory_data = self._create_sample_inventory_data()
            
        if recipes_file:
            self.recipes_data = pd.read_csv(recipes_file)
        else:
            self.recipes_data = self._create_sample_recipes_data()
            
        self.seasonal_factors = self._create_seasonal_factors()
        
    def _create_sample_orders_data(self) -> pd.DataFrame:
        """Create sample order data for demonstration."""
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        dishes = ['Chicken Curry', 'Beef Steak', 'Vegetable Salad', 'Pasta Marinara', 'Fish Soup']
        
        data = []
        for date in dates:
            # Simulate seasonal variations
            base_multiplier = 1.0
            if date.month in [12, 1, 2]:  # Winter - higher demand
                base_multiplier = 1.3
            elif date.month in [6, 7, 8]:  # Summer - moderate demand
                base_multiplier = 1.1
            elif date.month in [3, 4, 5, 9, 10, 11]:  # Spring/Fall - normal demand
                base_multiplier = 1.0
                
            # Weekend effect
            if date.weekday() >= 5:  # Weekend
                base_multiplier *= 1.2
                
            for dish in dishes:
                # Base demand varies by dish
                base_demand = {'Chicken Curry': 15, 'Beef Steak': 10, 'Vegetable Salad': 20, 
                             'Pasta Marinara': 18, 'Fish Soup': 12}[dish]
                
                quantity = max(0, int(np.random.poisson(base_demand * base_multiplier)))
                if quantity > 0:
                    data.append({
                        'date': date,
                        'dish_name': dish,
                        'quantity_sold': quantity,
                        'revenue': quantity * np.random.uniform(8, 25)
                    })
        
        return pd.DataFrame(data)
    
    def _create_sample_inventory_data(self) -> pd.DataFrame:
        """Create sample inventory data."""
        materials = [
            'Chicken Breast', 'Beef Tenderloin', 'Mixed Vegetables', 'Pasta', 'Fish Fillet',
            'Tomato Sauce', 'Olive Oil', 'Onions', 'Garlic', 'Salt', 'Pepper', 'Herbs'
        ]
        
        data = []
        for material in materials:
            # Set realistic expiry dates
            days_to_expiry = np.random.randint(1, 15)
            expiry_date = datetime.now() + timedelta(days=days_to_expiry)
            
            data.append({
                'material_name': material,
                'current_stock': np.random.randint(10, 100),
                'unit': 'kg' if material in ['Chicken Breast', 'Beef Tenderloin', 'Mixed Vegetables', 'Fish Fillet'] else 'pieces',
                'expiry_date': expiry_date,
                'cost_per_unit': np.random.uniform(2, 50),
                'minimum_stock_level': np.random.randint(5, 20)
            })
            
        return pd.DataFrame(data)
    
    def _create_sample_recipes_data(self) -> pd.DataFrame:
        """Create sample recipe data showing material requirements per dish."""
        recipes = [
            {'dish_name': 'Chicken Curry', 'material_name': 'Chicken Breast', 'quantity_needed': 0.3},
            {'dish_name': 'Chicken Curry', 'material_name': 'Onions', 'quantity_needed': 0.1},
            {'dish_name': 'Chicken Curry', 'material_name': 'Tomato Sauce', 'quantity_needed': 0.2},
            {'dish_name': 'Chicken Curry', 'material_name': 'Herbs', 'quantity_needed': 0.05},
            
            {'dish_name': 'Beef Steak', 'material_name': 'Beef Tenderloin', 'quantity_needed': 0.4},
            {'dish_name': 'Beef Steak', 'material_name': 'Salt', 'quantity_needed': 0.01},
            {'dish_name': 'Beef Steak', 'material_name': 'Pepper', 'quantity_needed': 0.01},
            
            {'dish_name': 'Vegetable Salad', 'material_name': 'Mixed Vegetables', 'quantity_needed': 0.3},
            {'dish_name': 'Vegetable Salad', 'material_name': 'Olive Oil', 'quantity_needed': 0.02},
            
            {'dish_name': 'Pasta Marinara', 'material_name': 'Pasta', 'quantity_needed': 0.2},
            {'dish_name': 'Pasta Marinara', 'material_name': 'Tomato Sauce', 'quantity_needed': 0.15},
            {'dish_name': 'Pasta Marinara', 'material_name': 'Garlic', 'quantity_needed': 0.02},
            
            {'dish_name': 'Fish Soup', 'material_name': 'Fish Fillet', 'quantity_needed': 0.25},
            {'dish_name': 'Fish Soup', 'material_name': 'Onions', 'quantity_needed': 0.1},
            {'dish_name': 'Fish Soup', 'material_name': 'Herbs', 'quantity_needed': 0.03},
        ]
        
        return pd.DataFrame(recipes)
    
    def _create_seasonal_factors(self) -> Dict:
        """Create seasonal adjustment factors."""
        return {
            'winter_months': [12, 1, 2],
            'spring_months': [3, 4, 5], 
            'summer_months': [6, 7, 8],
            'fall_months': [9, 10, 11],
            'factors': {
                'winter': 1.3,
                'spring': 1.0,
                'summer': 1.1,
                'fall': 1.0
            },
            'weekend_factor': 1.2,
            'holiday_factor': 1.5
        }
    
    def forecast_demand(self, days_ahead: int = 7) -> pd.DataFrame:
        """
        Forecast demand for the next specified days using historical data and seasonal factors.
        """
        if self.orders_data is None:
            raise ValueError("Orders data not loaded. Please load data first.")
        
        # Prepare historical data
        self.orders_data['date'] = pd.to_datetime(self.orders_data['date'])
        
        # Calculate average daily demand for each dish
        daily_avg = self.orders_data.groupby('dish_name')['quantity_sold'].mean()
        
        # Generate forecast dates
        start_date = datetime.now().date()
        forecast_dates = [start_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
        
        forecasts = []
        for date in forecast_dates:
            # Apply seasonal factors
            month = date.month
            seasonal_factor = 1.0
            
            if month in self.seasonal_factors['winter_months']:
                seasonal_factor = self.seasonal_factors['factors']['winter']
            elif month in self.seasonal_factors['summer_months']:
                seasonal_factor = self.seasonal_factors['factors']['summer']
            
            # Apply weekend factor
            weekend_factor = 1.0
            if date.weekday() >= 5:  # Weekend
                weekend_factor = self.seasonal_factors['weekend_factor']
            
            for dish in daily_avg.index:
                predicted_quantity = int(daily_avg[dish] * seasonal_factor * weekend_factor)
                forecasts.append({
                    'date': date,
                    'dish_name': dish,
                    'predicted_quantity': max(0, predicted_quantity),
                    'seasonal_factor': seasonal_factor,
                    'weekend_factor': weekend_factor
                })
        
        return pd.DataFrame(forecasts)
    
    def calculate_material_requirements(self, forecast_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate raw material requirements based on demand forecast.
        """
        if self.recipes_data is None:
            raise ValueError("Recipe data not loaded. Please load data first.")
        
        # Merge forecast with recipes
        requirements = forecast_data.merge(self.recipes_data, on='dish_name', how='left')
        
        # Calculate total material needed
        requirements['total_material_needed'] = (
            requirements['predicted_quantity'] * requirements['quantity_needed']
        )
        
        # Aggregate by material and date
        material_requirements = requirements.groupby(['date', 'material_name']).agg({
            'total_material_needed': 'sum'
        }).reset_index()
        
        return material_requirements
    
    def calculate_restocking_needs(self, material_requirements: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate what materials need to be restocked based on current inventory and requirements.
        """
        if self.inventory_data is None:
            raise ValueError("Inventory data not loaded. Please load data first.")
        
        # Get total requirements for the forecast period
        total_requirements = material_requirements.groupby('material_name').agg({
            'total_material_needed': 'sum'
        }).reset_index()
        
        # Merge with current inventory
        restock_analysis = total_requirements.merge(
            self.inventory_data[['material_name', 'current_stock', 'minimum_stock_level', 'cost_per_unit']], 
            on='material_name', 
            how='left'
        )
        
        # Calculate restocking needs
        restock_analysis['shortage'] = (
            restock_analysis['total_material_needed'] - restock_analysis['current_stock']
        )
        restock_analysis['needs_restocking'] = restock_analysis['shortage'] > 0
        restock_analysis['restock_quantity'] = np.maximum(
            restock_analysis['shortage'], 
            restock_analysis['minimum_stock_level'] - restock_analysis['current_stock']
        )
        restock_analysis['restock_cost'] = (
            restock_analysis['restock_quantity'] * restock_analysis['cost_per_unit']
        )
        
        # Filter only items that need restocking
        return restock_analysis[restock_analysis['needs_restocking']].sort_values('restock_cost', ascending=False)
    
    def find_near_expiry_materials(self, days_threshold: int = 3) -> pd.DataFrame:
        """
        Find materials that are near expiry and suggest dishes that can use them.
        """
        if self.inventory_data is None:
            raise ValueError("Inventory data not loaded. Please load data first.")
        
        # Convert expiry_date to datetime if it's not already
        self.inventory_data['expiry_date'] = pd.to_datetime(self.inventory_data['expiry_date'])
        
        # Find materials expiring soon
        threshold_date = datetime.now() + timedelta(days=days_threshold)
        near_expiry = self.inventory_data[
            self.inventory_data['expiry_date'] <= threshold_date
        ].copy()
        
        if near_expiry.empty:
            return pd.DataFrame()
        
        # Find dishes that can use these materials
        near_expiry_with_dishes = near_expiry.merge(
            self.recipes_data, 
            on='material_name', 
            how='left'
        )
        
        # Calculate how many dishes can be made with current stock
        near_expiry_with_dishes['max_dishes_possible'] = (
            near_expiry_with_dishes['current_stock'] / near_expiry_with_dishes['quantity_needed']
        ).fillna(0).astype(int)
        
        # Calculate days until expiry
        near_expiry_with_dishes['days_until_expiry'] = (
            near_expiry_with_dishes['expiry_date'] - datetime.now()
        ).dt.days
        
        return near_expiry_with_dishes.sort_values('days_until_expiry')
    
    def generate_optimization_report(self) -> Dict:
        """
        Generate a comprehensive inventory optimization report.
        """
        # Get forecasts and requirements
        demand_forecast = self.forecast_demand(7)
        material_requirements = self.calculate_material_requirements(demand_forecast)
        restocking_needs = self.calculate_restocking_needs(material_requirements)
        near_expiry = self.find_near_expiry_materials(3)
        dish_recommendations = self.recommend_dishes(5)
        
        # Calculate summary statistics
        total_restock_cost = restocking_needs['restock_cost'].sum() if not restocking_needs.empty else 0
        materials_to_restock = len(restocking_needs) if not restocking_needs.empty else 0
        materials_near_expiry = len(near_expiry['material_name'].unique()) if not near_expiry.empty else 0
        recommended_dishes = len(dish_recommendations) if not dish_recommendations.empty else 0
        
        report = {
            'summary': {
                'forecast_period_days': 7,
                'total_restock_cost': total_restock_cost,
                'materials_to_restock': materials_to_restock,
                'materials_near_expiry': materials_near_expiry,
                'recommended_dishes': recommended_dishes,
                'report_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'demand_forecast': demand_forecast,
            'material_requirements': material_requirements,
            'restocking_needs': restocking_needs,
            'near_expiry_materials': near_expiry,
            'dish_recommendations': dish_recommendations
        }
        
        return report
    
    def _get_weather_preferences(self) -> Dict:
        """Get dish preferences based on weather/season."""
        current_month = datetime.now().month
        
        # Simulate weather preferences based on season
        if current_month in [12, 1, 2]:  # Winter
            return {
                'preferred_dishes': ['Chicken Curry', 'Fish Soup'],
                'season': 'winter',
                'temperature_factor': 'cold',
                'preference_multiplier': 1.4
            }
        elif current_month in [6, 7, 8]:  # Summer
            return {
                'preferred_dishes': ['Vegetable Salad', 'Fish Soup'],
                'season': 'summer',
                'temperature_factor': 'hot',
                'preference_multiplier': 1.3
            }
        elif current_month in [3, 4, 5]:  # Spring
            return {
                'preferred_dishes': ['Vegetable Salad', 'Pasta Marinara'],
                'season': 'spring',
                'temperature_factor': 'mild',
                'preference_multiplier': 1.2
            }
        else:  # Fall
            return {
                'preferred_dishes': ['Beef Steak', 'Pasta Marinara'],
                'season': 'fall',
                'temperature_factor': 'cool',
                'preference_multiplier': 1.2
            }
    
    def recommend_dishes(self, max_recommendations: int = 5) -> pd.DataFrame:
        """
        Recommend dishes based on available materials, expiry dates, weather, and seasonal factors.
        """
        if any(data is None for data in [self.inventory_data, self.recipes_data]):
            raise ValueError("Inventory and recipe data must be loaded first.")
        
        # Get current weather preferences
        weather_prefs = self._get_weather_preferences()
        
        # Find materials near expiry (within 5 days)
        near_expiry = self.find_near_expiry_materials(5)
        expiry_materials = set(near_expiry['material_name'].unique()) if not near_expiry.empty else set()
        
        # Get all possible dishes
        all_dishes = self.recipes_data['dish_name'].unique()
        recommendations = []
        
        for dish in all_dishes:
            dish_recipes = self.recipes_data[self.recipes_data['dish_name'] == dish]
            
            # Check if we have all required materials
            required_materials = set(dish_recipes['material_name'])
            available_materials = set(self.inventory_data['material_name'])
            
            if not required_materials.issubset(available_materials):
                continue  # Skip if we don't have all required materials
            
            # Calculate feasibility score
            score_components = {
                'material_availability': 0,
                'expiry_urgency': 0,
                'seasonal_preference': 0,
                'cost_efficiency': 0
            }
            
            total_cost = 0
            max_servings = float('inf')
            urgency_bonus = 0
            
            # Analyze each required material
            for _, recipe_row in dish_recipes.iterrows():
                material_name = recipe_row['material_name']
                qty_needed = recipe_row['quantity_needed']
                
                # Get material info from inventory
                material_info = self.inventory_data[
                    self.inventory_data['material_name'] == material_name
                ].iloc[0]
                
                current_stock = material_info['current_stock']
                cost_per_unit = material_info['cost_per_unit']
                
                # Calculate maximum servings possible with this material
                possible_servings = int(current_stock / qty_needed)
                max_servings = min(max_servings, possible_servings)
                
                # Calculate cost for this material
                total_cost += qty_needed * cost_per_unit
                
                # Material availability score (higher stock = higher score)
                stock_ratio = current_stock / (material_info['minimum_stock_level'] + 1)
                score_components['material_availability'] += min(stock_ratio, 2.0)
                
                # Expiry urgency bonus (higher bonus for using near-expiry materials)
                if material_name in expiry_materials:
                    expiry_info = near_expiry[near_expiry['material_name'] == material_name]
                    if not expiry_info.empty:
                        days_until_expiry = expiry_info['days_until_expiry'].min()
                        # Higher bonus for more urgent expiry
                        urgency_bonus += max(0, (5 - days_until_expiry) * 0.5)
            
            if max_servings <= 0:
                continue  # Can't make this dish
            
            # Normalize material availability score
            score_components['material_availability'] /= len(dish_recipes)
            score_components['expiry_urgency'] = urgency_bonus
            
            # Seasonal preference score
            if dish in weather_prefs['preferred_dishes']:
                score_components['seasonal_preference'] = weather_prefs['preference_multiplier']
            else:
                score_components['seasonal_preference'] = 1.0
            
            # Cost efficiency score (lower cost per serving = higher score)
            cost_per_serving = total_cost
            score_components['cost_efficiency'] = max(0, (10 - cost_per_serving) / 10)
            
            # Calculate overall recommendation score
            overall_score = (
                score_components['material_availability'] * 0.3 +
                score_components['expiry_urgency'] * 0.4 +
                score_components['seasonal_preference'] * 0.2 +
                score_components['cost_efficiency'] * 0.1
            )
            
            recommendations.append({
                'dish_name': dish,
                'max_servings_possible': max_servings,
                'cost_per_serving': round(cost_per_serving, 2),
                'recommendation_score': round(overall_score, 2),
                'material_availability_score': round(score_components['material_availability'], 2),
                'expiry_urgency_score': round(score_components['expiry_urgency'], 2),
                'seasonal_preference_score': round(score_components['seasonal_preference'], 2),
                'cost_efficiency_score': round(score_components['cost_efficiency'], 2),
                'season': weather_prefs['season'],
                'uses_expiring_materials': bool(required_materials.intersection(expiry_materials)),
                'expiring_materials_used': list(required_materials.intersection(expiry_materials))
            })
        
        # Convert to DataFrame and sort by recommendation score
        recommendations_df = pd.DataFrame(recommendations)
        if not recommendations_df.empty:
            recommendations_df = recommendations_df.sort_values(
                'recommendation_score', ascending=False
            ).head(max_recommendations).reset_index(drop=True)
        
        return recommendations_df