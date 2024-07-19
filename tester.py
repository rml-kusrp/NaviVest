from directions import Directions
directions = Directions()
intensity = 100  # Example intensity value (adjust as needed)

# Trigger haptic feedback for different directions
directions.fwd(intensity)
directions.bwd(intensity)
directions.right(intensity)
directions.left(intensity)
