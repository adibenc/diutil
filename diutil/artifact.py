#!/usr/bin/python3
# MIT
from DateTime import DateTime
import uuid
import os

# Simple Artifact class
class Artifact:
	"""
	A class to represent an artifact with various features and metadata.

	Usage:
	builder = Artifact()
	artifact = (builder
				.set_id(1)
				.set_feature_brief(["Brief description"])
				.set_feature_sample(["Sample feature"])
				.set_data_dim((3, 3))  # data dimension (feat col x row)
				.set_result_val(0.95)
				.set_result_metric("accuracy")
				.set_result_err_val(0.05)
				.set_result_conf_matrix([[50, 2], [1, 47]])
				.set_result_infer_sample([1, 0])
				.set_err_metric("mean_squared_error")  # New err_metric attribute
				.build())
	artifact.to_file()

	returns

	{'created_at': '2024-10-10 17:45:38', 'id': 1, 'feature_brief': ['Brief description'], 'feature_sample': ['Sample feature'], 'data_dim': (3, 3), 'result_val': 0.95, 'result_metric': 'accuracy', 'result_err_val': 0.05, 'result_conf_matrix': [[50, 2], [1, 47]], 'result_infer_sample': [1, 0], 'err_metric': 'mean_squared_error'}
	"""

	def __init__(self, id=None) -> None:
		dt = DateTime()
		self.created_at = dt.ISO()
		if id is None:
			self.id = uuid.uuid4()
		else:
			self.id = id
		
		self.feature_brief = []
		self.feature_sample = []
		self.data_dim = (3, 3)
		self.result_val = None
		self.result_metric = None
		self.result_err_val = None
		self.result_conf_matrix = None
		self.result_infer_sample = None
		self.err_metric = None  # New attribute for error metric

	# Getters and setters
	def get_id(self):
		return self.id

	def set_id(self, id):
		self.id = id
		return self  # Return self for chaining

	def get_feature_brief(self):
		return self.feature_brief

	def set_feature_brief(self, brief):
		self.feature_brief = brief
		return self  # Return self for chaining

	def get_feature_sample(self):
		return self.feature_sample

	def set_feature_sample(self, sample):
		self.feature_sample = sample
		return self  # Return self for chaining

	def get_data_dim(self):
		return self.data_dim

	def set_data_dim(self, dim):
		self.data_dim = dim
		return self  # Return self for chaining

	def get_result_val(self):
		return self.result_val

	def set_result_val(self, val):
		self.result_val = val
		return self  # Return self for chaining

	def get_result_metric(self):
		return self.result_metric

	def set_result_metric(self, metric):
		self.result_metric = metric
		return self  # Return self for chaining

	def get_result_err_val(self):
		return self.result_err_val

	def set_result_err_val(self, err_val):
		self.result_err_val = err_val
		return self  # Return self for chaining

	def get_result_conf_matrix(self):
		return self.result_conf_matrix

	def set_result_conf_matrix(self, conf_matrix):
		self.result_conf_matrix = conf_matrix
		return self  # Return self for chaining

	def get_result_infer_sample(self):
		return self.result_infer_sample

	def set_result_infer_sample(self, infer_sample):
		self.result_infer_sample = infer_sample
		return self  # Return self for chaining

	def get_err_metric(self):
		return self.err_metric  # Getter for err_metric

	def set_err_metric(self, err_metric):  # Setter for err_metric
		self.err_metric = err_metric
		return self  # Return self for chaining

	def to_file(self):
		dt = self.created_at
		with open(f"{dt}-pipeline.md", "w") as f:
			# Writing the string representation of the artifact's dictionary to the file
			f.write(str(self.__dict__))
		return self


# Usage example

# builder = Artifact()
# artifact = (builder
# 			.set_id(1)
# 			.set_feature_brief(["Brief description"])
# 			.set_feature_sample(["Sample feature"])
# 			.set_data_dim((3, 3))  # data dimension (feat col x row)
# 			.set_result_val(0.95)
# 			.set_result_metric("accuracy")
# 			.set_result_err_val(0.05)
# 			.set_result_conf_matrix([[50, 2], [1, 47]])
# 			.set_result_infer_sample([1, 0])
# 			.set_err_metric("mean_squared_error")  # New err_metric attribute
# 			)
# artifact.to_file()
