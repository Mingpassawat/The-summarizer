summary = """
Bash, a command language interpreter for interacting with a computer from the command line. It's also called a shell because it surrounds the operating system kernel to hide its intricate details, while allowing you, the programmer, to do important stuff like access data and write files by typing simple commands.

This was a revolutionary concept when it was developed in the early 70s, back when programmers were still using punch cards. The shell concept evolved over the years, with the Bourne shell being the most popular version. That is, until 1989, when the BourneAgain shell, or Bash, came about.

When you open up the terminal on a Unix machine, like Mac OS and most Linux distros, the default shell is usually Bash. It provides a prompt where you can type a command, which will then be interpreted by the shell and executed on the operating system. To find out if you're running Bash, type in which $shell from the command line. It's like any other application that lives in the binaries directory.

But Bash is also a programming language that allows us to write scripts, which means anything we type manually into the command line can be automated with code. When you first launch the shell, it actually runs a startup script that's defined in the bash profile or bashrc file on your system. This allows you to customize the behavior and appearance of the shell whenever you start a new session.

You can add your own custom Bash scripts to any project by creating a file that ends in.sh, or no file extension at all. The first line in that file should always be a shebang, followed by the path to the application that should run it. Below that, we can start writing commands, like echo to print something, and they'll be interpreted line by line.

To create a variable, type a name in all caps, followed by the equal sign, then reference it later in the script using a dollar sign in front of the name. Now to execute the script, simply type the file name into the shell.

That was easy, but what if we want to pass in some arguments when we run the script? Positional arguments will automatically be assigned variable names of 1, 2, 3, and so on. Now in other cases, you may need additional user input in the middle of a script. You can create loops in Bash, like a do while loop here, that will prompt the user to continue the script on a yes answer or exit on a no answer. From there we can implement conditional logic with an if statement, which will test if the value on the left side is less than the value on the right side. If true, then run this command, otherwise run the else command.

Another cool feature is that if you have multiple long running processes, you can run them in parallel in the background by adding an ampersand after the command.

This has been Bash, the born again shell, in 100 seconds. If you want to see more short videos like this, make sure to hit the like button and subscribe. Thanks for watching, and I will see you in the next one.
"""

# Print the formatted summary
print(summary)
