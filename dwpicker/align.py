from dwpicker.pyside import QtCore
from dwpicker.geometry import split_line


def align_shapes(shapes, direction):
    _direction_matches[direction](shapes)


def align_left(shapes):
    left = min(s.bounding_rect().left() for s in shapes)
    for shape in shapes:
        shape_left = left + (shape.rect.left() - shape.bounding_rect().left())
        shape.rect.moveLeft(shape_left)
        shape.synchronize_rect()
        shape.update_path()


def align_h_center(shapes):
    x = sum(s.bounding_rect().center().x() for s in shapes) / len(shapes)
    for shape in shapes:
        offset = shape.bounding_rect().center().x() - shape.rect.center().x()
        shape_x = x - offset
        shape.rect.moveCenter(QtCore.QPointF(shape_x, shape.rect.center().y()))
        shape.synchronize_rect()
        shape.update_path()


def align_right(shapes):
    right = max(s.bounding_rect().right() for s in shapes)
    for shape in shapes:
        offset = right - shape.bounding_rect().right()
        shape.rect.moveLeft(shape.rect.left() + offset)
        shape.synchronize_rect()
        shape.update_path()


def align_top(shapes):
    top = min(s.bounding_rect().top() for s in shapes)
    for shape in shapes:
        shape_top = top + (shape.rect.top() - shape.bounding_rect().top())
        shape.rect.moveTop(shape_top)
        shape.synchronize_rect()
        shape.update_path()


def align_v_center(shapes):
    y = sum(s.bounding_rect().center().y() for s in shapes) / len(shapes)
    for shape in shapes:
        offset = shape.bounding_rect().center().y() - shape.rect.center().y()
        shape_y = y - offset
        shape.rect.moveCenter(QtCore.QPointF(shape.rect.center().x(), shape_y))
        shape.synchronize_rect()
        shape.update_path()


def align_bottom(shapes):
    bottom = max(s.bounding_rect().bottom() for s in shapes)
    for shape in shapes:
        offset = shape.rect.bottom() - shape.bounding_rect().bottom()
        shape_bottom = bottom + offset
        shape.rect.moveBottom(shape_bottom)
        shape.synchronize_rect()
        shape.update_path()


def arrange_horizontal(shapes):
    if len(shapes) < 3:
        return
    shapes = sorted(shapes, key=lambda s: s.bounding_rect().left())
    bounds = [shape.bounding_rect() for shape in shapes]
    total_width = sum(rect.width() for rect in bounds)
    gap = (
        bounds[-1].right() - bounds[0].left() - total_width
    ) / (len(shapes) - 1)
    position = bounds[0].left()
    for shape, rect in zip(shapes, bounds):
        shape.rect.translate(position - rect.left(), 0)
        shape.synchronize_rect()
        shape.update_path()
        position += rect.width() + gap


def arrange_vertical(shapes):
    if len(shapes) < 3:
        return
    shapes = sorted(shapes, key=lambda s: s.bounding_rect().top())
    bounds = [shape.bounding_rect() for shape in shapes]
    total_height = sum(rect.height() for rect in bounds)
    gap = (
        bounds[-1].bottom() - bounds[0].top() - total_height
    ) / (len(shapes) - 1)
    position = bounds[0].top()
    for shape, rect in zip(shapes, bounds):
        shape.rect.translate(0, position - rect.top())
        shape.synchronize_rect()
        shape.update_path()
        position += rect.height() + gap


def align_shapes_on_line(shapes, point1, point2):
    centers = split_line(point1, point2, len(shapes))
    for center, shape in zip(centers, shapes):
        shape.rect.moveCenter(center)
        shape.synchronize_rect()
        shape.update_path()


_direction_matches = {
    'left': align_left,
    'h_center': align_h_center,
    'right': align_right,
    'top': align_top,
    'v_center': align_v_center,
    'bottom': align_bottom
}
