import random

import numpy
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from tqdm import tqdm


class Node:

    def __init__(self, data_attributes: numpy.ndarray,
                 data_classes: numpy.ndarray, gini: float):
        self.data_attributes: numpy.ndarray = data_attributes
        self.data_classes: numpy.ndarray = data_classes
        self.gini: float = gini
        self.dimension: int = 0
        self.threshold: float = 0
        self.left: Node | None = None
        self.right: Node | None = None
        self.information_gain: float = float('-inf')


class MyDecisionTreeClassifier:

    def __init__(self, max_depth: int):
        self.max_depth: int = max_depth
        self.tree = None

    def build_tree(self, cur_node: Node, depth: int):
        if depth > self.max_depth or cur_node is None:
            return
        attrs = cur_node.data_attributes
        classes = cur_node.data_classes

        points_amount = attrs.shape[0]
        dimensions_count = attrs.shape[1]

        for dim in range(dimensions_count):
            for value in attrs[:, dim]:
                less_mask = attrs[:, dim] < value
                left_gini = calculate_gini(classes[less_mask])
                greater_mask = attrs[:, dim] >= value
                right_gini = calculate_gini(classes[greater_mask])

                left_length = sum(less_mask)
                right_length = points_amount - left_length
                if left_length == 0 or right_length == 0:
                    continue
                left_probability = left_length / points_amount
                right_probability = right_length / points_amount

                info_gain = (cur_node.gini -
                             left_probability * left_gini -
                             right_probability * right_gini)

                if info_gain > cur_node.information_gain:
                    cur_node.information_gain = info_gain
                    cur_node.dimension = dim
                    cur_node.threshold = value
                    cur_node.left = Node(attrs[less_mask],
                                         classes[less_mask],
                                         left_gini)
                    cur_node.right = Node(attrs[greater_mask],
                                          classes[greater_mask],
                                          right_gini)
        if cur_node.left is not None and cur_node.left.gini > 0:
            self.build_tree(cur_node.left, depth + 1)
        if cur_node.right is not None and cur_node.right.gini > 0:
            self.build_tree(cur_node.right, depth + 1)

    def fit(self, data_attributes: numpy.ndarray,
            data_classes: numpy.ndarray):
        self.tree = Node(data_attributes, data_classes,
                         calculate_gini(data_classes))
        self.build_tree(self.tree, 0)

    def predict(self, data_piece: numpy.ndarray):
        answer_arr = []
        for entry in data_piece:
            answer_arr.append(self.get_class(entry, self.tree))
        return answer_arr

    def get_class(self, data_unit: numpy.ndarray, node: Node):
        if node.left is None or node.right is None:
            return random.choice(node.data_classes)
        if data_unit[node.dimension] < node.threshold:
            return self.get_class(data_unit, node.left)
        else:
            return self.get_class(data_unit, node.right)


def calculate_gini(data_classes: numpy.ndarray) -> float:
    gini = 1.0
    length = len(data_classes)
    classes = {}
    for cls in data_classes:
        if cls in classes:
            classes[cls] += 1
        else:
            classes[cls] = 1
    for amount in classes.values():
        gini -= (amount / length) ** 2
    return gini


iris = load_iris()
data = iris.data[:, :2]
target = iris.target
summary = 0
for i in tqdm(range(100)):
    tree_object = MyDecisionTreeClassifier(1000)
    X, X_test, y, y_test = train_test_split(data,
                                            target,
                                            test_size=0.20)
    tree_object.fit(X, y)
    summary += (sum(tree_object.predict(X_test) == y_test) / len(y_test))
print(summary / 100)
