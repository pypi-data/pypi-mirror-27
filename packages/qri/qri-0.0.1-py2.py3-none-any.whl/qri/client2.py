#!/usr/bin/python
import sys
import json
import argparse
from subprocess import Popen, PIPE
import pandas as pd
import re
import shlex
import sys
from collections import OrderedDict
import csv
import time

if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO


_HASH_PATTERN = re.compile("^\/\w+\/(\w*)\/dataset\.json")
_TMP_TABLE_PATH = "/tmp/tmp.csv"
_TMP_META_PATH = "/tmp/meta_tmp.json"
_MAX_ATTEMPTS = 10
_DELAY = .1

#------------------------------------------------------------------

def _shell_exec_once(command):
	proc = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE)
	stdoutdata, err = proc.communicate()
	if err != "":
		raise Exception(err)
	return stdoutdata

def _shell_exec(command):
	stdoutdata = _shell_exec_once(command)
	for _ in range(_MAX_ATTEMPTS - 1):
		if "error" not in stdoutdata[:15]:
			break
		time.sleep(_DELAY)
		stdoutdata = _shell_exec_once(command)
	return stdoutdata

#------------------------------------------------------------------

def _list_ds():
	""" helper function for getting a list of datasets on your qri node"""
	command = "qri list -f json"
	stdoutdata = _shell_exec(command)
	names_and_hashes = [(ds['name'], ds['path']) for ds in json.loads(stdoutdata)]
	return names_and_hashes

def _get_name_from_hash(_hash):
	""" helper function to get a dataset's name from its hash"""
	names_and_hashes = _list_ds()
	full_hash_lookup = {h: n for n, h in names_and_hashes}
	partial_hash_lookup = dict()
	for n, h in names_and_hashes:
		matches = re.findall(_H, h)
		if len(matches) == 1:
			partial_hash = matches[0]
			partial_hash_lookup[partial_hash] = n
	if _hash in full_hash_lookup:
		return full_hash_lookup[_hash]
	if _hash in partial_hash_lookup:
		return partial_hash_lookup[_hash]

def _get_hash_from_name(name):
	""" Utility function to get a dataset's hash from its name"""
	names_and_hashes = _list_ds()
	name_lookup = {n: h for n, h in names_and_hashes}
	if name in name_lookup:
		return name_lookup[name]

def _run_select_all(name):
	""" helper function for getting data from qri commandline"""
	command = """qri run -f csv "select * from {}" """.format(name)
	stdoutdata = _shell_exec(command)
	if stdoutdata[:3].lower() in ["csv", "txt"]:
		stdoutdata = stdoutdata[3:]
	return StringIO(stdoutdata)

def _get_ds_info(name):
	""" helper function for getting a dataset's info from qri node"""
	_hash = _get_hash_from_name(name)
	command = """qri info -f json {}""".format(_hash)
	stdoutdata = _shell_exec(command)
	info = json.loads(stdoutdata)
	return info

def _get_ds_fields(name, verbose=False):
	""" helper function for getting a dataset's fields from qri node"""
	info = _get_ds_info(name)
	if verbose:
		return info["structure"]["schema"]["fields"]
	else:
		return [f["name"] for f in info["structure"]["schema"]["fields"]]


#------------------------------------------------------------------
def ds_list(name_only=True):
	""" get a listing of datasets on a qri node"""
	names_and_hashes = _list_ds()
	if name_only:
		return [items[0] for items in names_and_hashes]
	else:
		return names_and_hashes


class QriDataFrame(pd.DataFrame):
	""" QriDataFrame is a pandas DataFrame with additional qri-related 
	attributes and methods

	Attributes:
		name (str): name of qri dataset
		title (str): title of qri dataset
		description (str): description of qri dataset
		path (str): hash of dataset representing its unique address 
			based on the file's content
		structure (str): metadata containing the dataset's fields and schema
		timestamp (str): timestamp indicating when the dataset was created
		df_table (:obj: pd.DataFrame): data table
	"""
	_metadata = [ "name",
								"title",
								"description",
								"path",
								"structure",
								"timestamp",
							]

	def __init__(self, *args, **kwargs):
		name = kwargs.pop("name", "")
		self.name = name
		self.title = kwargs.pop("title", "")
		self.description = kwargs.pop("description", "")
		self.path = kwargs.pop("data", "")
		self.structure = kwargs.pop("structure", None)
		df_table = kwargs.pop("df_table", None)
		if not df_table:
			df_table = self._load_data_table(name)
		super(QriDataFrame, self).__init__(df_table)
		del df_table

	@property
	def _constructor(self):
		return QriDataFrame

	# def __repr__(self):
	# 	return super(QriDataFrame, self).__repr__

	def _load_data_table(self, name):
		fields = _get_ds_fields(name)
		data_table = _run_select_all(name)
		return pd.read_csv(data_table, header=None, names=fields)

	def fields(self, verbose=False):
		""" get the fields of the dataset from the dataset object """
		if not self.structure:
			info = _get_ds(info)
			self.structure = info["structure"]
		if verbose:
			return self.structure["schema"]["fields"]
		else:
			return  [f["name"] for f in self.structure["schema"]["fields"]]


def load_ds(name):
	""" Loads a dataset from a qri node"""
	info = _get_ds_info(name)
	info["name"] = name
	return QriDataFrame(**info)


