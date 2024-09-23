# $ git init <path/to/dir>
import math
import os
from string import Template
from git import Repo
import pandas as pd
from DateTime import DateTime

# dt = DateTime()
# dt.ISO()

"""
repo = git.Repo(repo_root.as_posix())
commit_dev = repo.commit("dev")
commit_origin_dev = repo.commit("origin/dev")
diff_index = commit_origin_dev.diff(commit_dev)

for diff_item in diff_index.iter_change_type('M'):
    print("A blob:\n{}".format(diff_item.a_blob.data_stream.read().decode('utf-8')))
    print("B blob:\n{}".format(diff_item.b_blob.data_stream.read().decode('utf-8'))) 

A = Added
D = Deleted
R = Renamed
M = Modified
T = Changed in the type
"""

class Gitter:
	excel_file_fname = ""
	reponame = ""
	setupPrompt = False
	df = None
	prompts = {}
	children = []

	def __init__(self, path_to_dir) -> None:
		if path_to_dir is None or path_to_dir == "." or path_to_dir == "":
			raise Exception("cant init with gitter")
		
		self.repo = Repo.init(path_to_dir)
		self.reponame = self.get_repo_name()
		dt = DateTime()
		dtiso = dt.ISO()
		dtiso = dtiso.replace(":", "-")

		self.excel_file_fname = f'{self.reponame}_{dtiso}.xlsx'

	def init(self, path_to_dir):
		# path_to_dir = "/media/data1/project1/si/tpdock/src/tilang-stage"
		self.repo = Repo.init(path_to_dir)

		return self
	
	def setSetupPrompt(self, sp):
		self.setupPrompt = True if sp else False

		return self

	def getPrompts(self):
		return self.prompts
	
	def exportPrompts(self):
		for k,v in self.prompts.items():
			f = open(f'/media/data1/confidential/codes/utils/report/2024-09/{k}-prompt.md', "w")
			f.write("\n".join(v))
		
		return self.prompts

	def setup_commits(self, max_count=10):
		self.commits = list(
			self.repo.iter_commits(all=True, max_count=max_count)
		)

		return self
	
	def to_excel(self):
		df = self.to_df()
		return df.to_excel(self.excel_file_fname)
	
	"""
	from string import Template
	s = Template('$who likes $what')
	s.substitute(who='tim', what='kung pao')

	d = dict(who='tim')
	Template('Give $who $100').substitute(d)

	Template('$who likes $what').substitute(d)
	Template('$who likes $what').safe_substitute(d)
	"""
	def create_prompt(self, c):
		# c.author
		# c.summary
		# c.stats.files
		s = Template(open("prompt-gm1.md", "r").read())
		return s.substitute(
			repo=c['repo'],
			date=c['date'],
			stats=c['stats'],
			diffs=c['diff'],
			summary=c['summary'],
			commits=c['commit'],
		)
	
	def wrap_prompt(self, c):
		# c.author
		# c.summary
		# c.stats.files
		s = Template(open("prompt-gm1-full.md", "r").read())
		return s.substitute(
			sub=c['sub'],
		)
	
	def wrap_prompts(self, asstring=False):
		wrappeds = []
		for k, p in self.prompts.items():
			wrapped = self.wrap_prompt({
				"sub": "\n".join(p)
			})

			if not asstring:
				f = open(f"./report/wrapped/{k}-wrapped.md", "w")
				f.write(wrapped)
		
		self.wrappeds = wrappeds
		return wrappeds
	
	def wrap_children_prompts(self):
		for c in self.children:
			c.wrappeds

	def to_df(self):
		df = pd.DataFrame({
			"no": [],
			"repo": [],
			"commit": [],
			"author": [],
			"summary": [],
			"stats": [],
			"diff": [],
			"difflen": [],
			"datetime": [],
			"date": [],
			"prompt": [],
			"promptlen": [],
		})

		for i, c in enumerate(self.commits):
			if i < 1:
				lc = c
				continue
			dt = DateTime(c.committed_date)
			dtiso = dt.ISO()
			# repo.git.diff("2bbc41116c2179c1e1879d63eaa0e5ea050edea3", "c050954255ece04c41a4933eca7346659f462dff")

			prompt = ""
			promptlen = len(prompt)
			diffStr = self.repo.git.diff(lc, c)
			difflen = len(diffStr)

			if difflen > 128:
				diffStr = diffStr[:128]
			
			date = pd.to_datetime(dtiso).strftime('%Y-%m-%d')
			mdict = {
				"no": [i],
				"repo": [self.reponame],
				"commit": [c.hexsha],
				"author": [c.author],
				"summary": [c.summary],
				"stats": [c.stats.files],
				"diff": [diffStr],
				"difflen": [difflen],
				"datetime": [dtiso],
				"date": [ date ],
				"prompt": [ prompt ],
				"promptlen": [ promptlen ],
			}
			
			if self.setupPrompt:
				prompt = self.create_prompt(mdict)
				promptlen = len(prompt)
			
			mdict['prompt'] = prompt
			mdict['promptlen'] = promptlen

			key = f"{self.reponame}-{date}"

			if not self.prompts.get(key):
				self.prompts[key] = []
			
			self.prompts[key].append(prompt)

			df = pd.concat(
				[ pd.DataFrame(mdict, columns=df.columns), df,], ignore_index=True
			)
			lc = c
		# 	df.append(, ignore_index=True)
		self.df = df
		
		return df
	
	def get_repo_name(self):
		return os.path.basename(self.repo.working_tree_dir)
	
	def get_repo_info(self):
		try:
			# Getting repository name
			repo_name = os.path.basename(self.repo.working_tree_dir)

			# Getting repository size (if available)
			repo_size = sum(os.path.getsize(os.path.join(root, f)) for root, _, files in os.walk(self.repo.working_tree_dir) for f in files)

			# Getting repository author (from first commit)
			author = None
			if self.repo.heads:
				first_commit = next(self.repo.iter_commits(self.repo.heads[0], max_count=1))
				author = first_commit.author.name

			# Getting contributors
			contributors = list(set(c.author.name for c in self.repo.iter_commits()))

			# Packaging info into a dictionary
			repo_info = {
				"repo_name": repo_name,
				"repo_author": author,
				"repo_size": repo_size,  # Size in bytes
				"contributors": contributors
			}
		except Exception as e:
			# Packaging info into a dictionary
			repo_info = {
				"repo_name": repo_name,
				"repo_author": 1,
				"repo_size": 2,  # Size in bytes
				"contributors": 3
			}

		return repo_info
