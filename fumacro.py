# TODO
# - Command to pause for human interaction
# - Bell at end of long sequence

import subprocess
import time
import argparse

# number of seconds between commands
delay = 100/1000

# catch user input
parser = argparse.ArgumentParser(description='Executes a list of xdotool key commands.')
parser.add_argument("-c", "--commands", nargs="+", help='list of commands')
parser.add_argument("-f", "--file", help="location of plain text file to draw commands from instead of -c. commands in -c will be ignored if this is specified.")
parser.add_argument("-i", "--iterate", help='number of times to loop the commands', type=int)
parser.add_argument('-l', '--list', help='list special commands', action='store_true') 
parser.add_argument('--varassignment', help='if called, let command will run every iteration, instead of only the first', action='store_true') 

args = parser.parse_args()
sequence = args.commands

iterate = 1
if args.iterate:
	iterate = args.iterate

if args.file:
	try:
		file = open(args.file)
		sequence = file.read().rstrip().split(" ")
		# iel sequence[-1]
	except FileNotFoundError:
		print("command file not found. Aborting.")
		exit()

# list mode
if args.list:
	print("""
	add:var:int			adds int to var.	
	call:var			calls variable.
	//comment			comment, ie no command.
	let:var:int 			set a variable. must be an int. Only runs first iteration unless varassignment is specified.
	repeat:int:command		repeat a command int times.
	repeat:var:command		repeat a command int times.
	sleep:int			waits int milliseconds.
	type:string			presses each letter key in order.
	"type:string with spaces"	same as type.
	""")
	exit()

# dictionary used for typing strings, of characters whose xdo command is not just the letter. ex "hello world" becomes [h, e, l, l, o, space, w, o, r, l, d]
specialChar = {
	" ": "space",
	"!": "exclam",
	"@": "at",
	"#": "numbersign",
	"$": "dollar",
	"-": "minus"
}

# dictionary used for user variable.
userVars = {}

def printExit(msg=""):
	print(msg)
	exit()

def pressKey(key):
	subprocess.run(["xdotool", "key", key])

def typeString(string):
	for letter in string:
		if letter in specialChar:
			letter = specialChar[letter]
		pressKey(letter)

def sleep(value):
	try:
		time.sleep(int(value)/1000) 
	except ValueError:
		printExit("Error: bad sleep number. Are you sleeping for an interger?")

def repeatPressKey(num, key):
	try:
		num = int(num)
	except ValueError:
		printExit("Error: repeat amount is not int.")
	for i in range(num):
		pressKey(key)

def repeatCommand(instruction):
	ls = instruction.split(":")
	# Normal int mode
	try:
		int(ls[1])
		repeatPressKey(ls[1], ls[2])
		return()	
	except:
		pass
	# Variable mode
	if ls[1] in userVars:
		num = userVars[ls[1]] 
		try:
			int(num)
			repeatPressKey(num, ls[2])
			return()	
		except ValueError:
			printExit("Error: repeat command reciverd non int variable. Aborting.")
	# Else
	printExit("Error: repeat command recieved invalid value. Aborting.")
	

def main(): 
	for instruction in sequence:
#		print(instruction)
		time.sleep(delay)
		#check for specaial commands
		if instruction.startswith("type:"):
			typeString(instruction[5:])
			continue

		if instruction.startswith("sleep:"):
			sleep(instruction[6:])
			continue

		if instruction.startswith("//"):
			continue

		if instruction.startswith("repeat:"):
			repeatCommand(instruction)
			continue

		if instruction.startswith("let:"):
			if iteration != 0: 
				continue
			ls = instruction.split(":")
			userVars[ls[1]] = ls[2]
			continue

		if instruction.startswith("call:"):
			ls = instruction.split(":")
			if ls[1] not in userVars:
				printExit("unrecognized variable. Aborting")
			
			typeString( userVars["num"])
			continue

		if instruction.startswith("add:"):
			ls = instruction.split(":")
			try: 
				total = int(userVars[ls[1]]) + int(ls[2])
				userVars[ls[1]] = str(total)
			except TypeError:
				printExit("add command is trying to add a int to a str. Aborting")
			continue

		#else just push the button
		pressKey(instruction)

# start
# print(sequence)
for iteration in range(iterate):
	main()
