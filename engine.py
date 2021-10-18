import tempfile
from pathlib import Path
import shutil
from multiprocessing import Value
from multiprocessing import Process

from image import Image
from point import Point
from ray import Ray
from color import Color

class RenderEngine:

    MAX_DEPTH = 5
    MIN_DISPLACE = 0.0001

    def renderMultiprocess(self, scene, processes, imgFile):
        def splitRange(count, parts):
            d, r = divmod(count, parts)
            return [
                (i * d + min(i,r), (i + 1) * d + min(i + 1, r)) for i in range(parts)
            ]
        width = scene.width
        height = scene.height
        ranges = splitRange(height, processes)

        tempDir = Path(tempfile.mkdtemp())
        tempFileTemplate = "renderpart{}.temp"
        processList = []
        try:
            rowsDone = Value("i", 0)
            for hmin, hmax in ranges:
                partFile = tempDir / tempFileTemplate.format(hmin)
                processList.append(Process(target=self.render, args=(scene,hmin,hmax, partFile, rowsDone)))

            for process in processList:
                process.start()
            for process in processList:
                process.join()

            Image.writePPMHeader(imgFile, height=height, width=width)
            for hmin, _ in ranges:
                partFile = tempDir / tempFileTemplate.format(hmin)
                imgFile.write(open(partFile,'r').read())

        finally:
            shutil.rmtree(tempDir)



    def render(self, scene, hmin, hmax, partFile, rowsDone):
        width = scene.width
        height = scene.height
        aspectRatio = float(width) / height
        x0 = -1.0
        x1 = 1.0
        xstep = (x1 - x0) / (width - 1)
        y0 = -1.0 / aspectRatio
        y1 = 1.0 / aspectRatio
        ystep = (y1 - y0) / (height - 1)

        camera = scene.camera
        pixels = Image(width, hmax-hmin)

        for j in range(hmin, hmax):
            y = y0 + j*ystep
            for i in range(width):
                x = x0 + i*xstep
                ray = Ray(camera, Point(x,y) - camera)
                pixels.setPixel(i, j-hmin, self.rayTrace(ray, scene))

            if rowsDone:
                with rowsDone.get_lock():
                    rowsDone.value += 1
                    print("{:3.0f}%".format(float(rowsDone.value) / float(height) * 100), end="\r")
            
        with open(partFile, 'w') as partFileObj:
            pixels.writePPMRaw(partFileObj)

        return pixels

    def rayTrace(self, ray, scene, depth=0):
        color = Color(0,0,0)
        distHit, objHit = self.findNearest(ray, scene)
        if objHit == None:
            return color
        hitPos = ray.origin + ray.direction * distHit
        hitNormal = objHit.normal(hitPos)
        color += self.colorAt(objHit, hitPos, hitNormal, scene)
        if depth < self.MAX_DEPTH:
            newRayPos = hitPos + hitNormal * self.MIN_DISPLACE
            newRayDir = ray.direction - 2 * ray.direction.dot(hitNormal) * hitNormal
            newRay = Ray(newRayPos, newRayDir)
            color += self.rayTrace(newRay, scene, depth+1) * objHit.material.reflection
        return color

    def findNearest(self, ray, scene):
        distMin = None
        objHit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (objHit is None or dist < distMin):
                distMin = dist
                objHit = obj

        return (distMin, objHit)

    def colorAt(self, objHit, hitPos, normal, scene):
        material = objHit.material
        objColor = material.colorAt(hitPos)
        toCam = scene.camera - hitPos
        specularK = 50
        color = material.ambient * Color.fromHex("#FFFFFF")
        for light in scene.lights:
            toLight = Ray(hitPos, light.position - hitPos)
            #diffuse (lambert)
            color += objColor * material.diffuse * max(normal.dot(toLight.direction), 0)
            #specular (blinn-phong)
            halfVector = (toLight.direction + toCam).normalize()
            color += light.color * material.specular * max(normal.dot(halfVector), 0) ** specularK
        return color