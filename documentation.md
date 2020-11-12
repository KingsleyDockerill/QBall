# QBall Documentation

## Hello, world! Program

By the end of this you will be able to print multiple values and decide what seperates them. First thing you should learn is how to create a string. To declare a string, either type one single quote or one double quote. Then type the value you want your string to be equal to. Finally, end it with a single quote (if you used one at the start) or double quote (if you used one at the start). Creating that on it's own won't do anything, but it can be put in a variable or passed as an arguement. Try typing this string into the shell:

```
"Hello, world!"
```

## Escape Characters

One cool thing you can do with strings is use an escape character. The escape character in QBall is a backslash. If a certain character is behind the backslash the section will be replaced. These are examples of everthing you can do with escape characters.

```
/"  /':
```

> This simple inserts the quote you put behind the backslash into the string. Normally a quote of the same type of the start breaks the string and reads the rest as a function. For instance:

:x:

```
   "Jack said "Hello, world!""
```

:white_check_mark:

```
"Jack said \"Hello, world\""
```

**OR**

```
'Jack said "Hello, world!"'
```

| Syntax  | Description                                                                                            | Example                            |
| ------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------- |
| \t      | Replaces with a tab                                                                                    | `\t `                              |
| \n      | Replaces with a new line                                                                               | `This is Line 1 \n This is Line 2` |
| \b      | Gets rid of the character before it                                                                    | `I like codinge\b`                 |
| \ + num | Inserts an amount of spaces equal to the number.                                                       | `We are\5five spaces apart`        |
| \\      | Inserts a backward slash                                                                               | `This is a backward slash -> \\`   |
| \char   | As long as the \ is not beside one of the characters above, it'll output the \ and the next character. | `\:D`                              |

> Now it's time for the interesting part; outputting a string into the console. In QBall, the command to output information is called `out`. It takes an unlimited amount of arguements, meaning you can output an infinite number of data. This is how you log Hello, world! in the console:

```
 out "Hello, world!"
```

But what if you want to output multiple strings combined? Well you just have to pass more than one arguement. For instance `out "Hello," "world!"` will put Hello, world! in the console. But what if you don't want a space? What if you want to insert a newline between each string? Well you can just add this line:

```
 out "Hello," "world!" sep="\n"
```

> Sep is short for seperator, and can be replaced with any string.
> You can also output numbers like shown below:

```
 out 5 5.5 #5
```

**Note:** Instead of a - for negatives you use a #. It can be any number, it doesn't matter. Numbers can also be joined together.

## Math

Math in QBall is quite simple. It has all your average operators (`+, -, *, /, **, //`) along with operators for bit manipulation (`&, |, ^, <, >`).
This is a guide to all bit manipulation in QBall:

```
 < = leftshift, formatted # < #
 > = rightshift, formatted # > #
 & = AND, formatted # & #
 | = OR, formatted # | #
 ^ = XOR, formatted # ^ #
```

But how do you use these in QBall? Like this:

```
out math 5 + 5;
```

You can do any mathematical eqution. Make sure you include the semicolon. This is so you can do this:

```
out math 5 + 5; "Hello, world!"
```

Without the semicolon you will get a error:
`"Illegal math operator!"`

Math will work as an argument for any function.

## Variables

Variables in QBall are simple. For now you only have to worry about global variables.
A variable points to a value. For instance you could create a variable x that is equal to 5.
`out x` is the same as `out 5`.

You declare variables using the following:

```
global a = 5;
```

This would create a variable named `a` with the value `5`. You can set a variable equal to an type, such as an int, floating point, string, and more.
Here are more examples:

```
global a = 1;
global b = 1.1;
global c = "1";
global d = math 5 + 5;
```

## Input

To get input in QBall you use the builtin "in". It takes one argument, a variable name, and stores it in that variable. If the variable doesn't exists, it creates it.
```
in a;
out a
```
This would take in input, store it in a new variable a, and then output it. Keep in mind you can run all of these programs in one line 
> For the shell you would use this; in a; out a unless you do each on seperate lines of input

## Functions

To declare functions in QBall you have to use the `_` token. Then you type the function name and then each argument until a semicolon. The following is an example of a function outarg that takes one argument, `a`
```
_outarg a;
```
Next you declare the body of the function:
```
_outarg a;
out a;
```
Then, finally, you end it off with the end keyword
```
_outarg a;
out a;
end
```

Now you can call this function from anywhere in your program like this:
```
outarg "Hello, world!"
would output
Hello, world!
if and else statements:
If statement's syntax in QBall are similiar to functions. An example:
if "Hi" == "Hi";
$ Code
    end
  To use an else statement:
    if "Hi" != "Hi";
      $ Code
else;
\$ Code
end
```

Notice there's only one end in that, after the else statement.
These are the operators you can use:
- :
- ==
- !=
- <=
- \> =
- \>
- \> <
- \> in
- \> !in
- \> !
---
QBall Documentation 
---
