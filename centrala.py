import subprocess

# List of programs to start
programs = ['clicker.py', 'show_gif.py', 'nagraj_ekran.py']

for program in programs:
  # Start the program
  subprocess.Popen(['python', program])

print('All programs started')
