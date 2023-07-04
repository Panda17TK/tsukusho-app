from flask import Flask, render_template, request, jsonify, redirect
import sys
import json
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from SetData import setdata