from pycircuit.formats import extends
from pycircuit.pcb import Pcb, Segment, NetClass
from shapely.ops import linemerge
from shapely.geometry import Point, LineString, MultiLineString
import itertools
import math

grid_size = 0.05

@extends(Pcb)
def to_route(self, filename):
    #grid_size = self.net_class.segment_width + \
    #            self.net_class.segment_clearance
    width, height = self.size()
    bounds = self.boundary()
    grid_width = int(width / grid_size + 1)
    grid_height = int(height / grid_size + 1)

    def vid(x, y):
        return str(y * grid_width + x)

    def grid(x, y):
        return (
            int((x - bounds[0]) / grid_size),
            int((y - bounds[1]) / grid_size)
        )

    with open(filename, 'w') as f:
        print('G', grid_width, grid_height, file=f)
        for net in self.netlist.nets:
            vids = []
            for pad in net.attributes.iter_pads():
                vids.append(vid(*grid(*pad.location[0:2])))
            print('N', ' '.join(vids), file=f)
        #for inst in self.netlist.insts:
        #    for pad in inst.attributes.iter_pads():
        #        loc = grid(pad.location[0] - pad.size[0] / 2,
        #                   pad.location[1] - pad.size[1] / 2)
        #        width = int(math.ceil(pad.size[0] / grid_size))
        #        height = int(math.ceil(pad.size[1] / grid_size))
        #        vids = []
        #        for x in range(width):
        #            for y in range(height):
        #                vids.append(vid(x + loc[0], y + loc[1]))
                #print('C', ' '.join(vids), file=f)





@extends(Pcb)
def from_route(self, filename):
    bounds = self.boundary()
    with open(filename) as f:
        #grid_size = self.net_class.segment_width + \
        #            self.net_class.segment_clearance
        grid_width = 0
        grid_height = 0
        nets = []
        for line in f:
            words = line.split(' ')
            if words[0] == 'G':
                grid_width = int(words[1])
                grid_height = int(words[2])
            if words[0] == 'N':
                nets.append([])
                for segment in words[1:]:
                    if segment == '\n':
                        continue
                    nets[-1].append([])
                    for vid in segment.split(','):
                        vid = int(vid)
                        x = vid % grid_width
                        y = int(vid / grid_width)
                        nets[-1][-1].append((x, y))

        for segments, net in zip(nets, self.netlist.nets):
            for segment in segments:
                for i, coord in enumerate(segment[1:]):
                    start = (segment[i][0] * grid_size + bounds[0],
                             segment[i][1] * grid_size + bounds[1])
                    end = (coord[0] * grid_size + bounds[0],
                           coord[1] * grid_size + bounds[1])
                    Segment(net, self.net_class, start, end, self.layers[0])
