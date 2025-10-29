import json
import logging
import torch
import re
import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util
import os
import random