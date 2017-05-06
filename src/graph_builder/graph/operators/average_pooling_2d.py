from graph_builder.graph.axis import Axis
from graph_builder.graph.operator import Operator
from graph_builder.graph.operators.attributes.post_axiswise import PostAxiswise
from graph_builder.graph.operators.attributes.post_elementwise import PostElementwise
from graph_builder.graph.operators.util import IntOrTuple, to_tuple
from graph_builder.graph.variable import Variable
from graph_builder.graph.variables.attributes.order import OrderNHWC


class AveragePooling2D(Operator):
    """Average pooling 2D operator

    Args:
        name (str): Operator name.
        ksize (int or tuple of int): Kernel size.
        stride (int or tuple of int): Stride size.
        padding (int or tuple of int): Padding size.
    """
    attributes = {PostElementwise,
                  PostAxiswise}

    def __init__(self, name: str, ksize: IntOrTuple, stride: IntOrTuple, padding: IntOrTuple):
        super().__init__(name)
        self.parameters["ksize"] = to_tuple(ksize)
        self.parameters["stride"] = to_tuple(stride)
        self.parameters["padding"] = to_tuple(padding)

    def __call__(self, x: Variable):
        """
        Args:
            x (:class:`~graph_builder.graph.variable.Variable`): Input

        Returns:
            tuple of :class:`~graph_builder.graph.variable.Variable`: Output
        """
        x_shape_dict = x.shape_dict
        N = x_shape_dict[Axis.N]
        H2 = (x_shape_dict[Axis.H] + 2 * self.parameters["padding"][0] - self.parameters["ksize"][0]) // \
             self.parameters["stride"][0] + 1
        W2 = (x_shape_dict[Axis.W] + 2 * self.parameters["padding"][1] - self.parameters["ksize"][1]) // \
             self.parameters["stride"][1] + 1
        C2 = x_shape_dict[Axis.C]

        y = Variable([N, H2, W2, C2], OrderNHWC)

        self.append_input("x", x)
        self.append_output("y", y)
        return y,
