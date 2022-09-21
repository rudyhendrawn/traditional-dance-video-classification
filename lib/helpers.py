import os
import glob

import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

DS = os.path.sep


def get_calculated_score(y_true, y_prediction_max):
  score_accuracy = accuracy_score(y_true, y_prediction_max)
  score_precision = precision_score(y_true, y_prediction_max, average="macro")
  score_recall = recall_score(y_true, y_prediction_max, average="macro")
  score_f1 = f1_score(y_true, y_prediction_max, average="macro")

  return score_accuracy, score_precision, score_recall, score_f1


def get_generated_class_names(dataset_dir):
  class_names = [fpath.split(DS)[-1] for fpath in glob.glob(os.path.join(dataset_dir, "*"))]
  class_names = sorted(class_names)

  return class_names


def get_generated_glob_pattern(dataset_dir):
  glob_pattern = os.path.join(dataset_dir, "{classname}", "*.mp4")
  return glob_pattern


def get_populated_y_data(generator, batch_size, model):
  y_prediction = []
  y_test = []

  for _ in range(generator.files_count // batch_size):
    x_next, y_next = generator.next()
    model_prediction = model.predict(x_next)

    y_test.extend(y_next)
    y_prediction.extend(model_prediction)

  y_prediction_max = np.argmax(y_prediction, axis=1)
  y_true = np.argmax(y_test, axis=1)

  return y_prediction_max, y_true


def get_visualized_graph(plots, title, x_label, y_label, legend):
  for plot in plots:
    plt.plot(plot)

  plt.title(title)
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.legend(legend, loc="upper left")

  return plt