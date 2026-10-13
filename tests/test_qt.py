
from unittest import TestCase
from unittest.mock import patch

from PyQt5.QtCore import QEvent, QPointF, Qt
from PyQt5.QtGui import QMouseEvent, QPixmap
from PyQt5.QtWidgets import QMessageBox

from labelImg import get_main_app
from libs.shape import Shape


class TestMainWindow(TestCase):

    app = None
    win = None

    def setUp(self):
        self.app, self.win = get_main_app()

    def tearDown(self):
        self.win.set_clean()
        self.win.close()
        self.app.quit()

    def test_noop(self):
        pass

    def test_delete_can_be_undone_and_redone(self):
        shape = Shape(label='box')
        shape.points = [
            QPointF(10, 10),
            QPointF(30, 10),
            QPointF(30, 30),
            QPointF(10, 30),
        ]
        shape.close()
        self.win.canvas.shapes.append(shape)
        self.win.add_label(shape)
        self.win.reset_history()
        self.win.canvas.select_shape(shape)

        self.win.delete_selected_shape()

        self.assertEqual([], self.win.canvas.shapes)
        self.assertTrue(self.win.undo_action.isEnabled())
        self.win.undo()
        self.assertEqual(1, len(self.win.canvas.shapes))
        self.assertEqual(1, self.win.label_list.count())
        self.assertTrue(self.win.redo_action.isEnabled())

        self.win.redo()
        self.assertEqual([], self.win.canvas.shapes)
        self.assertEqual(0, self.win.label_list.count())

    def test_right_drag_moves_selected_box_without_copying(self):
        canvas = self.win.canvas
        canvas.resize(100, 100)
        canvas.load_pixmap(QPixmap(100, 100))
        shape = Shape(label='box')
        shape.points = [
            QPointF(10, 10),
            QPointF(30, 10),
            QPointF(30, 30),
            QPointF(10, 30),
        ]
        shape.close()
        canvas.load_shapes([shape])
        self.win.add_label(shape)
        self.win.reset_history()

        canvas.scale = 1.0
        offset = canvas.offset_to_center()
        start = QPointF(20 + offset.x(), 20 + offset.y())
        end = QPointF(35 + offset.x(), 30 + offset.y())
        canvas.mousePressEvent(QMouseEvent(
            QEvent.MouseButtonPress, start, Qt.RightButton,
            Qt.RightButton, Qt.NoModifier))
        canvas.mouseMoveEvent(QMouseEvent(
            QEvent.MouseMove, end, Qt.NoButton,
            Qt.RightButton, Qt.NoModifier))
        canvas.mouseReleaseEvent(QMouseEvent(
            QEvent.MouseButtonRelease, end, Qt.RightButton,
            Qt.NoButton, Qt.NoModifier))

        self.assertEqual(1, len(canvas.shapes))
        self.assertEqual(QPointF(25, 20), canvas.shapes[0][0])
        self.assertTrue(self.win.undo_action.isEnabled())

    def test_right_drag_moves_all_selected_boxes_left_from_between_them(self):
        canvas = self.win.canvas
        canvas.resize(100, 100)
        canvas.load_pixmap(QPixmap(100, 100))
        shapes = []
        for left in (30, 50):
            shape = Shape(label='box')
            shape.points = [
                QPointF(left, 20),
                QPointF(left + 10, 20),
                QPointF(left + 10, 40),
                QPointF(left, 40),
            ]
            shape.close()
            shapes.append(shape)
        canvas.load_shapes(shapes)
        self.win.add_labels(shapes)
        canvas.select_shapes(shapes)

        canvas.scale = 1.0
        offset = canvas.offset_to_center()
        start = QPointF(45 + offset.x(), 30 + offset.y())
        end = QPointF(20 + offset.x(), 30 + offset.y())
        canvas.mousePressEvent(QMouseEvent(
            QEvent.MouseButtonPress, start, Qt.RightButton,
            Qt.RightButton, Qt.NoModifier))
        canvas.mouseMoveEvent(QMouseEvent(
            QEvent.MouseMove, end, Qt.NoButton,
            Qt.RightButton, Qt.NoModifier))
        canvas.mouseReleaseEvent(QMouseEvent(
            QEvent.MouseButtonRelease, end, Qt.RightButton,
            Qt.NoButton, Qt.NoModifier))

        self.assertEqual(2, len(canvas.shapes))
        self.assertEqual(5, canvas.shapes[0][0].x())
        self.assertEqual(25, canvas.shapes[1][0].x())

    def test_left_drag_moves_all_selected_boxes(self):
        canvas = self.win.canvas
        canvas.resize(100, 100)
        canvas.load_pixmap(QPixmap(100, 100))
        shapes = []
        for left in (30, 50):
            shape = Shape(label='box')
            shape.points = [
                QPointF(left, 20),
                QPointF(left + 10, 20),
                QPointF(left + 10, 40),
                QPointF(left, 40),
            ]
            shape.close()
            shapes.append(shape)
        canvas.load_shapes(shapes)
        self.win.add_labels(shapes)
        canvas.select_shapes(shapes)

        canvas.scale = 1.0
        offset = canvas.offset_to_center()
        start = QPointF(35 + offset.x(), 30 + offset.y())
        end = QPointF(25 + offset.x(), 30 + offset.y())
        canvas.mousePressEvent(QMouseEvent(
            QEvent.MouseButtonPress, start, Qt.LeftButton,
            Qt.LeftButton, Qt.NoModifier))
        canvas.mouseMoveEvent(QMouseEvent(
            QEvent.MouseMove, end, Qt.NoButton,
            Qt.LeftButton, Qt.NoModifier))
        canvas.mouseReleaseEvent(QMouseEvent(
            QEvent.MouseButtonRelease, end, Qt.LeftButton,
            Qt.NoButton, Qt.NoModifier))

        self.assertEqual(2, len(canvas.shapes))
        self.assertEqual(20, canvas.shapes[0][0].x())
        self.assertEqual(40, canvas.shapes[1][0].x())

    def test_deleting_label_removes_all_its_boxes_after_confirmation(self):
        shape = Shape(label='tray')
        shape.points = [
            QPointF(10, 10),
            QPointF(30, 10),
            QPointF(30, 30),
            QPointF(10, 30),
        ]
        shape.close()
        self.win.canvas.shapes.append(shape)
        self.win.add_label(shape)
        self.win.reset_history()

        with patch('labelImg.QMessageBox.question',
                   return_value=QMessageBox.Yes):
            self.win.delete_label_class('tray')

        self.assertEqual([], self.win.canvas.shapes)
        self.assertNotIn('tray', self.win.label_hist)
        self.assertTrue(self.win.undo_action.isEnabled())

        self.win.undo()
        self.assertEqual(1, len(self.win.canvas.shapes))
        self.assertIn('tray', self.win.label_hist)
