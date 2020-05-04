from pathlib import Path
from typing import List

import logging

logger = logging.getLogger(__name__)


class DebugHelper:
    def __init__(self, root_dir='.'):
        print("root_dir: ", root_dir)
        self.debug_dir = self.create_debug_dir(root_dir)

    def create_debug_dir(self, root_dir):
        debug_dir = Path(root_dir).joinpath('.debug')
        debug_dir.mkdir(exist_ok=True)

        return debug_dir

    def generate_debug_image(self, page, objects: List, filename: str):
        im = page.to_image()

        im.debug_tablefinder(dict(snap_tolerance=7), )

        if len(objects) > 0:
            boxes = objects if isinstance(objects[0], dict) else [o.bbox for o in objects]
            im.draw_rects(boxes)

        path = str(self.debug_dir.joinpath(filename).absolute())

        if not Path(path).parent.exists():
            Path(path).parent.mkdir(parents=True, exist_ok=True)

        logger.info(f'Debug image: {path}')
        im.save(path)

        return path
