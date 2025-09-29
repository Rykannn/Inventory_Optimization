import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime

class InventoryVisualizer:
    """
    Class for creating visualizations for inventory optimization analysis.
    """
    
    def __init__(self):
        # Set style for matplotlib
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def plot_demand_forecast(self, forecast_data: pd.DataFrame, save_path: str = None):
        """
        Create visualization for demand forecast by dish over time.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Pivot data for better plotting
        pivot_data = forecast_data.pivot(index='date', columns='dish_name', values='predicted_quantity')
        
        # Create stacked area plot
        pivot_data.plot(kind='area', stacked=True, ax=ax, alpha=0.7)
        
        ax.set_title('7-Day Demand Forecast by Dish', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Predicted Quantity', fontsize=12)
        ax.legend(title='Dishes', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_inventory_status(self, inventory_data: pd.DataFrame, save_path: str = None):
        """
        Create visualization for current inventory status.
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Current stock levels
        inventory_data.plot(x='material_name', y='current_stock', kind='bar', ax=ax1, color='skyblue')
        ax1.set_title('Current Stock Levels', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Stock Quantity')
        ax1.tick_params(axis='x', rotation=45)
        
        # Cost per unit
        inventory_data.plot(x='material_name', y='cost_per_unit', kind='bar', ax=ax2, color='lightcoral')
        ax2.set_title('Cost per Unit', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Cost ($)')
        ax2.tick_params(axis='x', rotation=45)
        
        # Stock vs minimum levels
        ax3.bar(inventory_data['material_name'], inventory_data['current_stock'], 
                label='Current Stock', alpha=0.7, color='green')
        ax3.bar(inventory_data['material_name'], inventory_data['minimum_stock_level'], 
                label='Minimum Level', alpha=0.7, color='red')
        ax3.set_title('Current Stock vs Minimum Levels', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Quantity')
        ax3.legend()
        ax3.tick_params(axis='x', rotation=45)
        
        # Days until expiry
        inventory_data['days_until_expiry'] = (
            pd.to_datetime(inventory_data['expiry_date']) - datetime.now()
        ).dt.days
        
        colors = ['red' if days <= 3 else 'orange' if days <= 7 else 'green' 
                 for days in inventory_data['days_until_expiry']]
        
        ax4.bar(inventory_data['material_name'], inventory_data['days_until_expiry'], color=colors)
        ax4.set_title('Days Until Expiry', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Days')
        ax4.axhline(y=3, color='red', linestyle='--', alpha=0.7, label='Critical (3 days)')
        ax4.axhline(y=7, color='orange', linestyle='--', alpha=0.7, label='Warning (7 days)')
        ax4.legend()
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_restocking_analysis(self, restocking_data: pd.DataFrame, save_path: str = None):
        """
        Create visualization for restocking analysis.
        """
        if restocking_data.empty:
            print("No restocking needed!")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Restocking quantities needed
        ax1.barh(restocking_data['material_name'], restocking_data['restock_quantity'], color='orange')
        ax1.set_title('Materials Requiring Restocking', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Quantity to Restock')
        
        # Restocking costs
        ax2.barh(restocking_data['material_name'], restocking_data['restock_cost'], color='red')
        ax2.set_title('Restocking Costs', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Cost ($)')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_near_expiry_materials(self, near_expiry_data: pd.DataFrame, save_path: str = None):
        """
        Create visualization for materials near expiry.
        """
        if near_expiry_data.empty:
            print("No materials near expiry!")
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Group by material and get minimum days until expiry
        expiry_summary = near_expiry_data.groupby('material_name').agg({
            'days_until_expiry': 'min',
            'current_stock': 'first',
            'max_dishes_possible': 'sum'
        }).reset_index()
        
        # Create scatter plot
        scatter = ax.scatter(expiry_summary['days_until_expiry'], 
                           expiry_summary['current_stock'],
                           s=expiry_summary['max_dishes_possible']*10,
                           c=expiry_summary['days_until_expiry'],
                           cmap='RdYlGn_r',
                           alpha=0.7)
        
        # Add material names as labels
        for i, row in expiry_summary.iterrows():
            ax.annotate(row['material_name'], 
                       (row['days_until_expiry'], row['current_stock']),
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, alpha=0.8)
        
        ax.set_title('Materials Near Expiry Analysis', fontsize=16, fontweight='bold')
        ax.set_xlabel('Days Until Expiry')
        ax.set_ylabel('Current Stock')
        ax.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('Days Until Expiry')
        
        # Add critical zones
        ax.axvline(x=3, color='red', linestyle='--', alpha=0.7, label='Critical (3 days)')
        ax.axvline(x=7, color='orange', linestyle='--', alpha=0.7, label='Warning (7 days)')
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_seasonal_trends(self, orders_data: pd.DataFrame, save_path: str = None):
        """
        Plot seasonal trends in order data.
        """
        # Ensure date column is datetime
        orders_data['date'] = pd.to_datetime(orders_data['date'])
        orders_data['month'] = orders_data['date'].dt.month
        orders_data['weekday'] = orders_data['date'].dt.day_name()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Monthly trends
        monthly_sales = orders_data.groupby('month')['quantity_sold'].sum()
        ax1.plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2, markersize=8)
        ax1.set_title('Monthly Sales Trends', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Total Quantity Sold')
        ax1.grid(True, alpha=0.3)
        
        # Weekly trends
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_sales = orders_data.groupby('weekday')['quantity_sold'].mean().reindex(weekday_order)
        ax2.bar(weekly_sales.index, weekly_sales.values, color='lightblue')
        ax2.set_title('Average Daily Sales by Weekday', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Average Quantity Sold')
        ax2.tick_params(axis='x', rotation=45)
        
        # Dish popularity
        dish_popularity = orders_data.groupby('dish_name')['quantity_sold'].sum().sort_values(ascending=True)
        ax3.barh(dish_popularity.index, dish_popularity.values, color='lightgreen')
        ax3.set_title('Total Sales by Dish', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Total Quantity Sold')
        
        # Revenue trends
        revenue_trends = orders_data.groupby('month')['revenue'].sum()
        ax4.plot(revenue_trends.index, revenue_trends.values, marker='s', color='red', linewidth=2, markersize=8)
        ax4.set_title('Monthly Revenue Trends', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Month')
        ax4.set_ylabel('Total Revenue ($)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_dish_recommendations(self, recommendations_data: pd.DataFrame, save_path: str = None):
        """
        Create visualization for dish recommendations.
        """
        if recommendations_data.empty:
            print("No dish recommendations available!")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Recommendation scores by dish
        colors = ['gold' if urgent else 'lightblue' 
                 for urgent in recommendations_data['uses_expiring_materials']]
        bars1 = ax1.barh(recommendations_data['dish_name'], 
                        recommendations_data['recommendation_score'], 
                        color=colors)
        ax1.set_title('Dish Recommendation Scores', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Recommendation Score')
        
        # Add score labels on bars
        for i, (bar, score) in enumerate(zip(bars1, recommendations_data['recommendation_score'])):
            ax1.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
                    f'{score:.2f}', va='center', fontsize=10)
        
        # 2. Maximum servings possible
        bars2 = ax2.bar(recommendations_data['dish_name'], 
                       recommendations_data['max_servings_possible'],
                       color='lightgreen')
        ax2.set_title('Maximum Servings Possible', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Servings')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add serving labels on bars
        for bar, servings in zip(bars2, recommendations_data['max_servings_possible']):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    str(servings), ha='center', va='bottom', fontsize=10)
        
        # 3. Cost efficiency vs Expiry urgency scatter plot
        scatter = ax3.scatter(recommendations_data['cost_efficiency_score'], 
                            recommendations_data['expiry_urgency_score'],
                            s=recommendations_data['recommendation_score']*50,
                            c=recommendations_data['seasonal_preference_score'],
                            cmap='RdYlGn', alpha=0.7)
        ax3.set_title('Cost Efficiency vs Expiry Urgency', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Cost Efficiency Score')
        ax3.set_ylabel('Expiry Urgency Score')
        ax3.grid(True, alpha=0.3)
        
        # Add dish names as labels
        for i, dish in enumerate(recommendations_data['dish_name']):
            ax3.annotate(dish, 
                        (recommendations_data['cost_efficiency_score'].iloc[i], 
                         recommendations_data['expiry_urgency_score'].iloc[i]),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=8, alpha=0.8)
        
        # Add colorbar for seasonal preference
        cbar = plt.colorbar(scatter, ax=ax3)
        cbar.set_label('Seasonal Preference Score')
        
        # 4. Score components breakdown
        score_components = recommendations_data[['dish_name', 'material_availability_score', 
                                               'expiry_urgency_score', 'seasonal_preference_score', 
                                               'cost_efficiency_score']].set_index('dish_name')
        
        score_components.plot(kind='bar', stacked=True, ax=ax4, 
                            color=['skyblue', 'orange', 'lightgreen', 'pink'])
        ax4.set_title('Recommendation Score Components', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Score')
        ax4.tick_params(axis='x', rotation=45)
        ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()