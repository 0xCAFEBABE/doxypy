#!/usr/bin/env python

""" @namespace doxypy
doxypy is an input filter for Doxygen. It preprocesses python
files so that docstrings of classes and functions are reformated
into Doxygen-conform documentation blocks. It can be found at
<http://code.foosel.net/doxypy>.

In order to make Doxygen preprocess files through doxypy, simply
add the following lines to your Doxyfile:
	FILTER_SOURCE_FILES = YES
	INPUT_FILTER = "python /path/to/doxypy.py"

Copyright (C) 2006:
	Gina Haeussge (gina at foosel dot net),
	Philippe Neumann (demod at gmx dot net)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import sys
import re
from optparse import OptionParser, OptionGroup

def makeCommentBlock(commentLines, indent=""):
	"""	Converts "commentLines" into a comment block
		
		@param   commentLines  The lines of the block comment
		@param   indent        The indentation of the block
		
		@returns an indented doxygen comment block
	"""

	doxyStart = "%s##" % indent
	joinStr = "\n%s# " % indent
	
	if options.strip:
		commentLines = map(str.strip, commentLines)
	
	lines = joinStr + joinStr.join(commentLines)
	
	return doxyStart + lines

def parse(input):
	"""	Searches for function and class definitions in "input", then moves
		existing docstrings (as doxygen block comments) in front of the
		definitions
		
		@param   input	A string containing the sourcecode to process
		
		@returns the processed input
	"""
	
	output = []
	
	# split input into lines
	lines = input.split("\n")
	
	### regexes
	
	# comment delimiters of a docstring
	commentDelimRe = "\"\"\"|'''"
	
	# docstring triggering keywords
	triggerRe = re.compile("^(\s*)(def .+:|class .+:)")
	
	# comment start
	commentStartRe = re.compile('^\s*(%s)' % commentDelimRe)
	
	# comment end
	commentEndRe = re.compile('(%s)\s*$' % commentDelimRe)
	
	# empty line (nothing but whitespaces)
	emptyRe = re.compile("^\s*$")
	
	# hashline
	hashLineRe = re.compile("^\s*#.*$")
	
	# import lines
	importLineRe = re.compile("^\s*(import |from .+ import)")
	
	### flags, buffers, ...
	
	# are we at the beginning of the file?
	fileHeadFlag = True
	
	# did we come across a trigger word (def or class)?
	triggerWordFlag = False
	
	# current comment lines
	comment = []
	
	# indentation for the current comment block
	triggerWs = ""
	
	# lines that triggered the docstring search
	triggerLines = []
	
	# contains current commentdelimiter if in active comment
	activeCommentDelim = None
	
	### main processing routine
	
	# process each line
	for line in enumerate(lines):
		if not triggerWordFlag:
			match = re.search(triggerRe, line[1])
			if match:
				if triggerWordFlag and triggerLines:
					output.append("\n".join(triggerLines))

				triggerWordFlag = True
				triggerWs = match.group(1)
				fileHeadFlag = False
				triggerLines = [line[1]]
				continue

		# file header or active keyword trigger?
		if fileHeadFlag or triggerWordFlag:
			commentStartMatch = re.search(commentStartRe, line[1])
			commentEndMatch = re.search(commentEndRe, line[1])
			
			# comment end of current multiline comment found
			if commentEndMatch and activeCommentDelim and \
			   commentEndMatch.group(1) == activeCommentDelim:
				comment.append( line[1][ : line[1].rfind(activeCommentDelim) ] )
				output.append(makeCommentBlock(comment, triggerWs))
				if triggerLines:
					output.append("\n".join(triggerLines))
				comment = []
				triggerWs = ""
				triggerLines = None
				triggerWordFlag = False
				activeCommentDelim = None
				
			# comment start found
			elif commentStartMatch:
				# get the used comment delimiter
				activeCommentDelim = commentStartMatch.group(1)
				
				if re.search(commentEndRe, line[1][line[1].find(activeCommentDelim)+len(activeCommentDelim) :]):
					# singleline comment
					comment.append(line[1][line[1].find(activeCommentDelim)+len(activeCommentDelim) : line[1].rfind(activeCommentDelim)])
					output.append(makeCommentBlock(comment, triggerWs))
					
					if triggerLines:
						output.append("\n".join(triggerLines))
					
					comment = []
					triggerWs = ""
					triggerLines = None
					triggerWordFlag = False
					activeCommentDelim = None
					
				else:
					# multiline comment begin
					comment.append(
						line[1][line[1].find(activeCommentDelim)+len(activeCommentDelim):]
					)
			
			# active multiline comment => append comment
			elif activeCommentDelim:
				comment.append(line[1])
				
			# still searching for comments
			elif re.search(emptyRe, line[1]):
				if triggerLines:
					triggerLines.append(line[1])
				else:
					output.append(line[1])
			
			# searching for file header
			elif fileHeadFlag:
				if not (re.search(hashLineRe, line[1]) or re.search(emptyRe, line[1]) or re.search(importLineRe, line[1])):
					# fileheader over => disable search
					fileHeadFlag = False
				output.append(line[1])
			
			# no comment => disable comment search mode
			else:
				triggerWordFlag = False
				if triggerLines:
					output.append("\n".join(triggerLines))
				triggerLines = None
				output.append(line[1])
		
		# just append the line
		else:
			output.append(line[1])
	
	# return output
	return "\n".join(output)

def loadFile(filename):
	"""	Loads file "filename" and returns the content.
		
		@param   filename	The name of the file to load
		@returns the content of the file.
	"""
	
	f = open(filename, 'r')
	
	try:
		content = f.read()
		return content
	finally:
		f.close()

def optParse():
	"""parses commandline options"""
	
	parser = OptionParser(prog="doxypy", version="%prog 0.2.2")
	
	parser.set_usage("%prog [options] filename")
	parser.add_option("--trim", "--strip",
		action="store_true", dest="strip",
		help="enables trimming of docstrings, might be useful if you get oddly spaced output"
	)
	
	## parse options
	global options
	(options, filename) = parser.parse_args()
	
	if not filename:
		print >>sys.stderr, "No filename given."
		sys.exit(-1)
	
	return filename[0]

def main():
	"""	Opens the file given as first commandline argument and processes it,
		then prints out the processed file.
	"""
	
	filename = optParse()
	
	try:
		input = loadFile(filename)
	except IOError, (errno, msg):
		print >>sys.stderr, msg
		sys.exit(-1)
	
	print parse(input)

if __name__ == "__main__":
	main()
