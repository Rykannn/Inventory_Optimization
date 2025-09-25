import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    
    def create_interactive_dashboard(self, report_data: Dict):
        """
        Create an interactive dashboard using Plotly.
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Demand Forecast', 'Inventory Status', 'Restocking Costs', 'Expiry Timeline'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 1. Demand Forecast
        forecast_data = report_data['demand_forecast']
        for dish in forecast_data['dish_name'].unique():
            dish_data = forecast_data[forecast_data['dish_name'] == dish]
            fig.add_trace(
                go.Scatter(x=dish_data['date'], y=dish_data['predicted_quantity'],
                          mode='lines+markers', name=dish, showlegend=True),
                row=1, col=1
            )
        
        # 2. Inventory Status (if restocking data exists)
        if not report_data['restocking_needs'].empty:
            restock_data = report_data['restocking_needs']
            fig.add_trace(
                go.Bar(x=restock_data['material_name'], y=restock_data['current_stock'],
                      name='Current Stock', showlegend=True),
                row=1, col=2
            )
            fig.add_trace(
                go.Bar(x=restock_data['material_name'], y=restock_data['minimum_stock_level'],
                      name='Min Level', showlegend=True),
                row=1, col=2
            )
        
        # 3. Restocking Costs
        if not report_data['restocking_needs'].empty:
            fig.add_trace(
                go.Bar(x=report_data['restocking_needs']['material_name'],
                      y=report_data['restocking_needs']['restock_cost'],
                      name='Restock Cost', showlegend=False, marker_color='red'),
                row=2, col=1
            )
        
        # 4. Expiry Timeline
        if not report_data['near_expiry_materials'].empty:
            expiry_data = report_data['near_expiry_materials']
            expiry_summary = expiry_data.groupby('material_name')['days_until_expiry'].min().reset_index()
            
            fig.add_trace(
                go.Scatter(x=expiry_summary['material_name'], 
                          y=expiry_summary['days_until_expiry'],
                          mode='markers', name='Days to Expiry', 
                          marker=dict(size=10, color=expiry_summary['days_until_expiry'],
                                    colorscale='RdYlGn_r', showscale=True),
                          showlegend=False),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title_text="Inventory Optimization Dashboard",
            title_x=0.5,
            showlegend=True,
            height=800,
            template="plotly_white"
        )
        
        # Update x-axis labels
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Material", row=1, col=2, tickangle=45)
        fig.update_xaxes(title_text="Material", row=2, col=1, tickangle=45)
        fig.update_xaxes(title_text="Material", row=2, col=2, tickangle=45)
        
        # Update y-axis labels
        fig.update_yaxes(title_text="Quantity", row=1, col=1)
        fig.update_yaxes(title_text="Stock Level", row=1, col=2)
        fig.update_yaxes(title_text="Cost ($)", row=2, col=1)
        fig.update_yaxes(title_text="Days", row=2, col=2)
        
        return fig
    
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