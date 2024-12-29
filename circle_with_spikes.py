#!/usr/bin/env python
# coding=utf-8
import inkex
import math
from lxml import etree

class RegularPolygonGenerator(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--num_spikes", type=int, default=5, help="Number of spikes in the circle")
        pars.add_argument("--radius",     type=float, default=100.0, help="Length of radius")
        pars.add_argument("--fall_radius_percent", type=float, default=30.0, help="Fall of radius in percent")

    def effect(self):
        num_spikes = self.options.num_spikes
        radius = self.options.radius
        fall_radius_percent = self.options.fall_radius_percent/100.0;

        if num_spikes < 3:
            inkex.errormsg("The number of sides must be at least 3.")
            return

        # Calculate the angle between the vertices
        angle = 2 * math.pi / num_spikes

        # Calculate the coordinates of the vertices
        points = []
        for i in range(num_spikes):
            x = radius+radius * math.cos(i * angle)
            y = radius+radius * math.sin(i * angle)
            points.append(f"{x},{y}")
            
            x = radius+radius*(1.0-fall_radius_percent) * math.cos(i * angle+angle/2.0)
            y = radius+radius*(1.0-fall_radius_percent) * math.sin(i * angle+angle/2.0)
            points.append(f"{x},{y}")

        # Create the polygon element
        polygon = etree.Element(
            inkex.addNS("polygon", "svg"),
            {
                "points": " ".join(points),
                "style": "fill:none;stroke:black;stroke-width:1",
            },
        )
        self.svg.get_current_layer().append(polygon)

if __name__ == "__main__":
    RegularPolygonGenerator().run()

