
import pygame

class Animation:
    def __init__(self):
        self.animations = []
        self.is_animating = False

    def add_move(self, tile_value, from_pos, to_pos, duration=10, is_merge=False):
        animation = {
            "type": "move",
            "value": tile_value,
            "from_pos": from_pos,
            "to_pos": to_pos,
            "duration": duration,
            "frame": 0,
            "is_merge": is_merge
        }
        self.animations.append(animation)
        self.is_animating = True

    def add_appear(self, tile_value, pos, duration=10, is_merge=False):
        animation = {
            "type": "appear",
            "value": tile_value,
            "pos": pos,
            "duration": duration,
            "frame": 0,
            "is_merge": is_merge
        }
        self.animations.append(animation)
        self.is_animating = True

    def update(self):
        if not self.is_animating:
            return

        still_animating = False
        for anim in self.animations:
            anim["frame"] += 1
            if anim["frame"] < anim["duration"]:
                still_animating = True
        
        if not still_animating:
            self.animations = []
            self.is_animating = False
