import random
import uuid
from datetime import datetime
from typing import Dict, Any, List
from .base_agent import BaseAgent


class NutritionAgent(BaseAgent):
    """Plans space-optimized meals with inventory tracking"""

    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "nutrition_agent",
            name="Nutritionist",
            agent_type="physical",
            capabilities=[
                "meal_planning",
                "nutrient_tracking",
                "inventory_management",
                "hydration_monitoring",
            ],
        )
        
        self.meals = {
            "breakfast": [
                {"name": "Fortified Oatmeal with Dried Fruits", "calories": 350, "protein": 12, "carbs": 55},
                {"name": "Breakfast Burrito (Rehydrated)", "calories": 420, "protein": 18, "carbs": 45},
                {"name": "Instant Pancakes with Syrup", "calories": 380, "protein": 10, "carbs": 60},
            ],
            "lunch": [
                {"name": "Chicken Curry with Rice", "calories": 450, "protein": 30, "carbs": 50},
                {"name": "Tuna Salad Wrap", "calories": 380, "protein": 28, "carbs": 35},
                {"name": "Vegetable Soup with Crackers", "calories": 320, "protein": 12, "carbs": 45},
            ],
            "dinner": [
                {"name": "Beef Steak with Vegetables", "calories": 520, "protein": 40, "carbs": 30},
                {"name": "Shrimp Pasta with Sauce", "calories": 480, "protein": 25, "carbs": 55},
                {"name": "Turkey Tetrazzini", "calories": 460, "protein": 32, "carbs": 45},
            ],
            "snacks": [
                {"name": "Mixed Nuts", "calories": 170, "protein": 5, "carbs": 7},
                {"name": "Chocolate Pudding", "calories": 150, "protein": 3, "carbs": 25},
                {"name": "Dried Fruit Mix", "calories": 130, "protein": 2, "carbs": 30},
            ],
        }
        
        self.inventory = self._initialize_inventory()
        self.meal_history = []
        self.hydration_log = []

    def _initialize_inventory(self) -> Dict[str, Any]:
        """Initialize food inventory"""
        return {
            "breakfast_items": random.randint(15, 30),
            "lunch_items": random.randint(20, 40),
            "dinner_items": random.randint(20, 40),
            "snacks": random.randint(30, 50),
            "water_reserve_liters": random.randint(50, 100),
            "expiry_alerts": [],
        }

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process nutrition request"""
        action = input_data.get("action", "generate_meal_plan")
        
        if action == "generate_meal_plan":
            return await self._generate_meal_plan(input_data)
        elif action == "get_nutrition_info":
            return await self._get_nutrition_info(input_data)
        elif action == "check_inventory":
            return await self._check_inventory()
        elif action == "log_meal":
            return await self._log_meal(input_data)
        elif action == "track_hydration":
            return await self._track_hydration(input_data)
        else:
            return {"error": f"Unknown action: {action}"}

    async def _generate_meal_plan(self, data: Dict) -> Dict[str, Any]:
        """Generate daily meal plan"""
        day_type = data.get("day_type", "regular")
        
        calorie_target = 2500 if day_type == "heavy_exercise" else 2000
        
        plan = {
            "date": datetime.now().date().isoformat(),
            "meals": {},
            "total_calories": 0,
            "total_protein": 0,
            "total_carbs": 0,
        }
        
        for meal_type in ["breakfast", "lunch", "dinner", "snacks"]:
            meal = random.choice(self.meals[meal_type])
            plan["meals"][meal_type] = {
                **meal,
                "id": str(uuid.uuid4()),
                "time": self._get_meal_time(meal_type),
            }
            plan["total_calories"] += meal["calories"]
            plan["total_protein"] += meal["protein"]
            plan["total_carbs"] += meal["carbs"]
        
        if self.inventory.get(meal_type.replace("snacks", "snacks") + "_items", 1) <= 0:
            plan["low_stock_alerts"] = [meal_type]
        
        return {
            "agent": self.name,
            "meal_plan": plan,
            "calorie_target": calorie_target,
            "meets_target": abs(plan["total_calories"] - calorie_target) < 200,
            "timestamp": datetime.now().isoformat(),
        }

    def _get_meal_time(self, meal_type: str) -> str:
        """Get scheduled time for meal"""
        times = {
            "breakfast": "07:00",
            "lunch": "12:00",
            "dinner": "18:00",
            "snacks": "10:00, 15:00, 21:00",
        }
        return times.get(meal_type, "12:00")

    async def _get_nutrition_info(self, data: Dict) -> Dict[str, Any]:
        """Get nutritional information for specific food"""
        food_name = data.get("food_name", "")
        
        return {
            "agent": self.name,
            "nutrition": {
                "calories": random.randint(200, 600),
                "protein": random.randint(10, 40),
                "carbs": random.randint(20, 60),
                "fat": random.randint(5, 25),
                "fiber": random.randint(2, 10),
                "sodium": random.randint(200, 800),
                "vitamins": ["Vitamin A", "Vitamin C", "Vitamin D", "B Complex"],
                "minerals": ["Iron", "Calcium", "Potassium", "Zinc"],
            },
            "space_benefits": [
                "Shelf-stable without refrigeration",
                "Lightweight packaging",
                "Specially formulated for bone health in microgravity",
            ],
            "timestamp": datetime.now().isoformat(),
        }

    async def _check_inventory(self) -> Dict[str, Any]:
        """Check current food inventory"""
        inventory = self.inventory
        
        alerts = []
        for category, count in inventory.items():
            if isinstance(count, int) and count < 10:
                alerts.append(f"Low stock: {category}")
        
        return {
            "agent": self.name,
            "inventory": inventory,
            "alerts": alerts,
            "days_remaining": min(
                inventory.get("breakfast_items", 0),
                inventory.get("lunch_items", 0),
                inventory.get("dinner_items", 0),
            ),
            "water_reserve": f"{inventory.get('water_reserve_liters', 0)} liters",
            "timestamp": datetime.now().isoformat(),
        }

    async def _log_meal(self, data: Dict) -> Dict[str, Any]:
        """Log completed meal"""
        meal_log = {
            "id": str(uuid.uuid4()),
            "meal_type": data.get("meal_type"),
            "food_name": data.get("food_name"),
            "calories": data.get("calories", 0),
            "logged_at": datetime.now().isoformat(),
            "satisfaction": data.get("satisfaction", 5),
        }
        
        self.meal_history.append(meal_log)
        
        if data.get("meal_type"):
            key = f"{data['meal_type']}_items"
            if key in self.inventory:
                self.inventory[key] -= 1
        
        return {
            "agent": self.name,
            "logged": meal_log,
            "today_total_calories": sum(m.get("calories", 0) for m in self.meal_history 
                                        if m["logged_at"][:10] == datetime.now().date().isoformat()),
            "timestamp": datetime.now().isoformat(),
        }

    async def _track_hydration(self, data: Dict) -> Dict[str, Any]:
        """Track water intake"""
        action = data.get("action_type", "log")
        
        if action_type == "log":
            amount = data.get("amount_ml", 250)
            self.hydration_log.append({
                "amount_ml": amount,
                "timestamp": datetime.now().isoformat(),
            })
            
            if "water_reserve_liters" in self.inventory:
                self.inventory["water_reserve_liters"] -= amount / 1000
                
        today_total = sum(h["amount_ml"] for h in self.hydration_log 
                          if h["timestamp"][:10] == datetime.now().date().isoformat())
        
        target = 2500
        percentage = min(100, (today_total / target) * 100)
        
        return {
            "agent": self.name,
            "today_intake_ml": today_total,
            "target_ml": target,
            "percentage": round(percentage, 1),
            "status": "good" if percentage >= 80 else "needs_attention",
            "recommendations": self._get_hydration_recommendations(percentage),
            "timestamp": datetime.now().isoformat(),
        }

    def _get_hydration_recommendations(self, percentage: float) -> List[str]:
        """Get hydration recommendations"""
        if percentage < 50:
            return [
                "Drink at least 500ml of water immediately",
                "Set reminders every 30 minutes",
                "Include water-rich foods in next meal",
            ]
        elif percentage < 80:
            return [
                "Keep water accessible at all times",
                "Drink before feeling thirsty",
            ]
        else:
            return ["Hydration is optimal! Keep it up."]
