import os
import sys
import pandas as pd
from typing import List, Tuple, Dict, Any
from ortoolpy import addvar, addvars, addbinvars
import pandas as pd
import pulp
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GetData.setdata import SetData

class CalcProb(SetData):
	def __init__(self) -> None:
		self.data_instance = setdata.SetData()
		self.all_data:pd.DataFrame = self.data_instance.data_user_frame["全員"].replace("", pd.NA).set_index(["日付", "時間帯"]).dropna(how='all', axis=0)
		self.user_list:list = list(self.all_data.columns)
		self.time_list:list = list(self.all_data.index)

	def calc_prob(self) -> pd.DataFrame:
		# 問題を作る
		prob = pulp.LpProblem("PracticeTimeOptimization", pulp.LpMaximize)
		# モデルの定義
		self.x = pulp.LpVariable.dicts("x", [(i,j) for i in self.user_list for j in self.time_list], cat="Binary")


