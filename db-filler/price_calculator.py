PRINT_TYPES = ["Banner", "Documento", "Flyer", "Plano", "Tarjeta"]
SIZES = ["A2", "A3", "A4", "Grande"]
MATERIALS = ["Bond", "Cartulina", "Couche", "Vinil"]

class PrintOrder:
  def __init__(self, job_type, quantity, size, material, color):
    self.JobType = job_type
    self.Quantity = quantity
    self.Size = size
    self.Material = material
    self.Color = color

def calculate_print_price(order: PrintOrder) -> float:
  base_prices = {
    "Banner": 15.0,
    "Documento": 0.10,
    "Flyer": 0.20,
    "Plano": 8.0,
    "Tarjeta": 0.15,
  }

  size_multipliers = {
    "A4": 1.0,
    "A3": 1.8,
    "A2": 3.0,
    "Grande": 4.5,
  }

  material_costs = {
    "Bond": 0.0,
    "Cartulina": 0.20,
    "Couche": 0.25,
    "Vinil": 5.0,
  }

  if order.JobType not in base_prices:
    raise ValueError(f"Invalid job type: '{order.JobType}'")
  if order.Size not in size_multipliers:
    raise ValueError(f"Invalid size: '{order.Size}'")
  if order.Material not in material_costs:
    raise ValueError(f"Invalid material: '{order.Material}'")

  base = base_prices[order.JobType]
  size_mult = size_multipliers[order.Size]
  material_extra = material_costs[order.Material]

  color_mult = 1.5 if order.Color else 1.0

  unit_price = (base * size_mult + material_extra) * color_mult

  if order.Quantity >= 1000:
    unit_price *= 0.70
  elif order.Quantity >= 500:
    unit_price *= 0.80
  elif order.Quantity >= 100:
    unit_price *= 0.90

  total_price = unit_price * order.Quantity

  return round(total_price, 2)