import networkx as nx
import os
import random

class computerplot(object):
	def __init__(self):
		self.graph = nx.Graph() # ze ram eater
		self.current = "/" # current path
		self.fucked = False
	
	def main(self):
		going = True
		self.folderScan = {} # where os.listdir() content goes
		fullpath = "/"
		
		while going == True:
			fullpath = self.CheckPopulate(fullpath) # check the fullpath, before populating to withstand errors.
		
			currentFolders, fucked = self.populate(fullpath)
			#print currentFolders
			
			if fucked == True: # did not have premission to scan the folder
				fullpath = fullpath[ 0: len( self.getFolderName(fullpath,1) )+1 ] # remove the upperfolder, +1 because of the backslash
			else: # if everything works
				if currentFolders: # if not empty
				
					if fullpath != "/": #see issue #1
						fullpath += "/" + random.choice( currentFolders ) # random next folder, continue going deeper
					else:
						fullpath += random.choice( currentFolders )
				
				else: # if empty
				
					self.deleteOccurance(fullpath) # delete it form folderscan
					
					files = self.folderScan[ self.GetKeyFolderScan(fullpath)]
					
					if files != []: # still not empty, go deeper 
						fullpath = self.RemoveCurrentFolder(fullpath) # removing first folder and "/"
						fullpath += "/" + random.choice( self.folderScan[ self.GetKeyFolderScan(fullpath)] ) 
					else:
						# need to loop upwards until it finds a folder with unplotted folders
						print "finding closest undone folder"
						fullpath = self.EmptyLoop(fullpath)
	
	def EmptyLoop(self, fullpath): # loop until folderscan list is not empty
		#print "entering EmptyLoop: " + fullpath + "		" +  self.GetKeyFolderScan(fullpath)
		files = self.folderScan[ self.GetKeyFolderScan(fullpath)]
		
		while files == []:
			del self.folderScan[ self.GetKeyFolderScan(fullpath)]
			
			fullpath = self.RemoveCurrentFolder(fullpath)
			files = self.folderScan[ self.GetKeyFolderScan(fullpath) ]
			print fullpath + " " + str( len(files) )
		return fullpath
		
	def RemoveCurrentFolder(self, fullpath): # remove the current folder from fullpath
		fullpath = fullpath[0: fullpath.find( self.getFolderName(fullpath, 2) )] + self.getFolderName(fullpath, 2)
		#notice that we remove the secound folder and then adds it back again.
		return fullpath
	
	def getFolderName(self, fullpath, backnum): # backnum 1 = folder currently in. 2= the folder where the folder we are currently are in is.
		folders = fullpath.split("/")
		toret = folders[ len(folders)-backnum ]
		
		if backnum > len(folders): # /selbulantimelapsv2 (backnum 2 = "/")
			toret = "/"
		return toret
	
	def graphFunc(self, x, y): # x is from (fullpath), y is to (filename)
		self.graph.add_edge( self.getFolderName(x,1), y) # last element in folders is the upper foldername
	
	def findOccurance(self, string, tofind): # does not work with letter of tofind more than 1. we dont need that either
		occs = 0
		for i in string:
			if i == tofind:
				occs += 1
		return occs
	
	def GetKeyFolderScan(self,fullpath): # get key for the FolderScan dictionary
		print
		print "geykeyfolderscan"
		print
		print fullpath
		self.upperfolder = self.getFolderName(fullpath,1)
		
		if self.findOccurance("/", fullpath) != 1: # if more than one "/" in fullpath
			key = self.RemoveCurrentFolder(fullpath) # remove current folder from fullpath, i.e we get the folder name where the folder we are in is, i.e the key.
		elif self.findOccurance("/", fullpath) == 1: # /selbulantimelapsv2, /xfoldername
			key = "/"
		
		if key == "":
			if "/" in self.folderScan.keys():
				key = "/"
			else:
				plt.savefig(platform.system()+".jpg")
				exit()
		if key not in self.folderScan.keys(): # if not valid key
			print "key not found in fullpath"
			print "key used: " + key
		
		return key
	def deleteOccurance(self, fullpath):# deleting the occurance of done folder in the folderscan entry of the Upperfolder. So that it wont be plotted twice
	
		key = self.GetKeyFolderScan(fullpath)
		
		if self.upperfolder in self.folderScan[ key]:
			self.folderScan[ key ].remove( self.upperfolder )
		
	
	def CheckPopulate(self, fullpath): # check if fullpath can be scanned and works.
		print "checkpopulate"
		if fullpath != "/":
			if fullpath.find("*.*") == -1:
				#fullpath = fullpath[ 0: len( self.getFolderName(fullpath,1) )+1 ]
				fullpath = self.EmptyLoop(fullpath)
			else: # contains *.*
				self.EmptyLoop(fullpath)
				
			try : # if it fails to scan i.e premission error
				files = os.listdir(fullpath)
			except:
				fullpath = self.EmptyLoop(fullpath)
			
		return fullpath
		
	def populate(self, fullpath): # scan the fullpath directory
		self.CheckPopulate(fullpath)
		print "populate"
		fucked = False
		files = []
		
		files = os.listdir(fullpath) # list all files and folders

		folders = []
		
		for file in files:
			if fullpath != "/": # if not first scan
				filepath = fullpath+"/"+file # path to the current file
			else: # if first scan, / + file
				filepath = fullpath+file
				
			self.graphFunc(fullpath, file) # network graph them
			
			if os.path.isfile(filepath): # if not directory
				files.remove(file)
			elif os.path.isdir(filepath):
				folders.append(file)
		
		if bool(folders): # if not empty
			self.folderScan[fullpath] = files
		
		if "System Volume Information" in folders: #acts like folder but is a file
			folders.remove("System Volume Information")
		return folders, fucked

#run it!
computerplot = computerplot()
computerplot.__init__()
computerplot.main()