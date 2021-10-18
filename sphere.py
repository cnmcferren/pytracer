import math

class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersects(self, ray):
        sphereToRay = ray.origin - self.center
        #a = 1
        b = 2 * ray.direction.dot(sphereToRay)
        c = sphereToRay.dot(sphereToRay) - self.radius * self.radius
        discriminate = b * b - 4 * c

        if discriminate >= 0:
            dist = (-b - math.sqrt(discriminate)) / 2
            if dist > 0:
                return dist

        return None

    def normal(self, surfacePoint):
        return (surfacePoint - self.center).normalize()