<br>
<p align="center">
   <h3 align="center">Documentation</h3>
  
  <p align="center">
    Welcome to the QBall Documentation!
    <br />
    <a href="https://github.com/KingsleyDockerill/QBall/" rel="help"><strong>Home »</strong></a>
    ·
    <a href="https://github.com/KingsleyDockerill/QBall/issues" rel="next">Report Bug</a>
    ·
    <a href="https://github.com/KingsleyDockerill/QBall/issues" rel="next">Request Feature</a>
    ·
    <a href="https://trello.com/b/cJM6HsR3/qball" rel="external">Trello board</a>
    ·
    <a href="https://repl.it/@qballlang/QBall" rel="external">QBall Shell</a>
  </p>
  
   <p align="center">
    <a href="https://github.com/KingsleyDockerill/QBall/network/members">
      <img alt="Forks" src="https://img.shields.io/github/forks/KingsleyDockerill/QBall.svg?style=for-the-badge">
    </a>
    <a href="https://github.com/KingsleyDockerill/QBall/stargazers">
      <img alt="Stargazers" src="https://img.shields.io/github/stars/KingsleyDockerill/QBall.svg?style=for-the-badge">
    </a>
    <a href="https://github.com/KingsleyDockerill/QBall/issues">
      <img alt="Issues" src="https://img.shields.io/github/issues/KingsleyDockerill/QBall.svg?style=for-the-badge">
    </a>
    <a href="https://github.com/KingsleyDockerill/QBall/graphs/contributors">
      <img alt="Contributors" src="https://img.shields.io/github/contributors/KingsleyDockerill/QBall.svg?style=for-the-badge">
    </a>
    <a href="https://github.com/KingsleyDockerill/QBall/blob/master/LICENSE">
      <img alt="GPL-3.0 License" src="https://img.shields.io/github/license/KingsleyDockerill/QBall.svg?style=for-the-badge">
    </a>
  </p>
</p>

<!-- TOC -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="README.d">Welcome</a>
    </li>
    <li>
      <a href="examples.md">Examples</a>
      <ul>
        <li><a href="examples.md#hw">Hello World</a></li>
        <li><a href="examples.md#of">Output function</a></li>
        <li><a href="#ex-oe">Output Elements</a></li>
        <li><a href="#ex-rpy8bc">Run Python & 8Ball code</a></li>
      </ul>
    </li>
    <li><a href="#math">Math</a></li>
    <li><a href="#esc-char">Escape Characters</a></li>
    <li><a href="#comment">Comments</a></li>  
    <li><a href="#funct">Functions</a></li>
    <li><a href="#if-else">If / Else</a></li>
    <li><a href="#var">Varibles</a></li>
    <li>
      <a href="#io">Input and Output</a>
      <ul>
        <li><a href="#out">Outputting</a></li>
        <li><a href="#in">Input</a></li>
      </ul>
    </li>
    <li><a href="#data-type">Data types</a></li>
    <li><a href="#esc-char-tbl">Escape character table</a></li>
    <li><a href="#op-tbl">Operator table</a></li>
  </ol>
</details>

<!-- WELCOME-->
<h1 id="wel">Welcome</h1>

Welcome to the official QBall documentation! To start, click one of the links above!

<!-- EXAMPLES-->
<h2 id="ex">Examples</h2>

> __NOTE:__ Even though it looks similar, these are written in QBall <code>.qball</code>, not python <code>.py</code>.

<!-- HELLO WORLD-->
<h3 id="ex-hw">Hello World <small><a href="../examples/hello-world.qball">&#60;&#47;&#62;</a></small></h3>

<pre>
out 'Hello world!'
</pre>

<!-- OUTPUT FUNCTION -->
<h3 id="ex-of">Output function <small><a href="../examples/output-function.qball">&#60;&#47;&#62;</a></small></h3>

<pre>
((This will create a function that will output a single argut.))men

$ outarg function
_outarg a;
  out a;
end

$ Output floating points, strings, int, lists
outarg "Hello, world!"
outarg 5
outarg 5.5
outarg ["Hello, world!", "Hello, again!"]
</pre>

<!-- OUTPUT ELEMENTS-->
<h3 id="ex-oe">Output Elements <small><a href="../examples/output-elements.qball">&#60;&#47;&#62;</a></small></h3>

<pre>
((This will output every element in a string or list))

_iterarg a;
  for i in a;
    out i;
  end
end

iterarg ["Hello, world!" 5 ["Hello" "Hi"] 5.5]
</pre>

<!-- RUN PYTHON & 8BALL CODE-->
<h3 id="ex-rpy8bc">Run Python & 8Ball code <small><a href="../examples/output-function.qball">&#60;&#47;&#62;</a></small></h3>

<pre>
out "Enter some QBall code: " newline=0;
in a;
out "Enter some Python code: " newline=0;
in b;
qstr a;
py b
</pre>

<!-- MATH -->
<h2 id="math">Math</h2>

<p style="font-style: italic;"><em><small>Also see, <a href="#operator-table">operator table</a></small></em></p>

QBall has operators for all common arithmetic operations
such as addition and multiplication and also bit manipulation.
To do math do <code>out math 5 + 5;</code> the semicolon is necessary
or else the program will exit with <code><span style="color:#c80509">Illegal math operator!</span></code>.
Math will work as an argument for any function.

<!-- ESCAPE CHARACTERS-->
<h2 id="esc-char">Escape Characters</h2>

<p style="font-style: italic;"><em><small>Also see, <a href="#escape-character-table">escape character table</a></small></em></p>

One cool thing you can do with strings is using an escape character.
The escape character in QBall is a backslash.
If a certain character is behind the backslash the section will be replaced.

For example, you can turn this, <code>"Jack said, "Hello, world! ""</code>.
Into this <code>"Jack said \"Hello, world!\""</code>, or without escape characters,
<code>'Jack said "Hello, world!"'</code>.

<!-- COMMENTS -->
<h2 id="comment">Comments</h2>

Comments can be used to explain the code and make it more readable.
It can also be used to prevent execution of code.

Single line comments are started with the dollar sign <code>$</code> character.
Any text between <code>$</code> and the end of the line are marked as a comment.

Multi-line comments are started with <code>((</code> and ended with <code>))</code>.
Any text between <code>((</code> and <code>))</code> are marked as a comment.

<pre>
$ Ham

if 10 > 5;
  $ Eggs
else;
  $ Potato
end

$ out "Hello!"
out "3 + 3 is equal to 9"

((
  Hello
  I'm a
  multi
  line
  comment
))
</pre>

<!-- FUNCTIONS -->
<h2 id="funct">Functions</h2>

Functions are declared using the underscore <code>_</code> character

<pre>
_outarg a;
  out a;
end
</pre>

Now you can call this function from anywhere in your QBall program:

<pre>
outarg "Hello, world!" $ Output: Hello, world!
</pre>

<!-- IF / ELSE-->
<h2 id="if-else">If / Else</h2>

<p style="font-style: italic;"><em><small>Also see, <a href="#operator-table">operator table</a></small></em></p>

The syntax of an if...else block is slightly different in QBall from Python.
Notice how there's only an <code>end</code> at the ends of the if...else statment.

<pre>
x = 481
y = 0
if x < y;
  out "Less"
else;
  if x == y;
    out "Equal"
  else;
    out "Greater"
  end
end
</pre>

<pre>
x = 100
if x == 100;
  out x
end
</pre>

<!-- VARIABLES -->
<h2 id="var">Varibles</h2>

<p style="font-style: italic;"><em><small>Also see, <a href="#data-type">date types</a></small></em></p>

<pre>
<strong>global</strong> <em>name</em> = <em>value</em>
</pre>

Declares a variable named <code><em>name</em></code> with the value of <code><em>value</em></code>.

To declare variables, you use the <code><em>global</em></code> token,
and to assign <code><em>value</em></code> to variables you use an equal sign character <code>=</code>.

<pre>
global foo = 6;          $ Iteger
global bar = 22.4;       $ Float
global baz = "51";       $ String
global qux math 5 + 5;   $ Iteger
global quux = true;      $ Iteger

out foo;    $ 1
out bar;    $ 1.1
out baz;    $"1"
out qux;    $ 10
out quux;   $ true
</pre>

<!-- INPUT AND OUTPUT -->
<h2 id="io">Input and Output</h2>
This section will discuss  methods of getting input from the user and log
data to the terminal.

<!-- OUTPUT -->
<h3 id="out">Outputting</h3>

<pre>
<strong>out</strong> <em>data</em>, sep=<em>" "</em>
</pre>

Logs <code><em>data</em></code> to the terminal, separated by using <code><em>sep</em></code>.
If <code><em>sep</em></code> is present,it must be given an argument.

All non-string data from <code><em>data</em></code> are automatically converted to a string.

<pre>
out "Hello, world!"; $ Hello, world!
out "Hello," "world!" sep=" "; $ Hello, world!
out "Hello," "world!" sep="\n"; $ Hello,
                               $ world!
</pre>

<!-- INPUT -->
<h3 id="in">Input</h3>

<pre>
<strong>in</strong> <em>prompt</em>
</pre>

Get's user input and returns it as a string. <code><em>prompt</em></code>
is displayed when the user is prompted to input data.

<pre>
out "You entered " input "Enter something: ";
$ Enter something: <strong><em>ham cheese eggs</em></strong>
$ You entered ham cheese eggs

global a = "ham"
in a;
out a
$ <strong><em>egg!</em></strong>
$ egg!
</pre>

<!-- DATE TYPES -->
<h2 id="data-type">Data types</h2>

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Example</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Iteger</td>
    <td><code>Numeric</code></td>
    <td><code>532</code></td>
  </tr>
  <tr>
    <td>Float</td>
    <td><code>Numeric</code></td>
    <td><code>3.14</code></td>
  </tr>
  <tr>
    <td>String</td>
    <td><code>Text</code></td>
    <td><code>"Hello, World!"</code></td>
  </tr>
  <tr>
    <td>Bool</td>
    <td><code>Boolean</code></td>
    <td><code>true</code></td>
  </tr>
</tbody>
</table>

<!-- ESCAPE CHARACTER TABLE-->
<h2 id="esc-char-tbl">Escape character table</h2>

<table>
<thead>
  <tr>
    <th>Character</th>
    <th>Name</th>
    <th>Example</th>
    <th>Result</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><code>\t</code></td>
    <td>Tab</td>
    <td><code>Hello \t world!</code></td>
    <td><code>Hello&nbsp;&nbsp;&nbsp;&nbsp;world!</code></td>
  </tr>
  <tr>
    <td><code>\n</code></td>
    <td>New Line</td>
    <td><code>Line 1\nLine 2</code></td>
    <td><code>Line 1<br>Line 2</code></td>
  </tr>
  <tr>
    <td><code>\b</code></td>
    <td>Backspace</td>
    <td><code>Hello World!!\b</code></td>
    <td><code>Hello World!</code></td>
  </tr>
  <tr>
    <td><code>\{num}</code></td>
    <td>Spacer</td>
    <td><code>We are\5 five spaces apart</code></td>
    <td><code>We are&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;five spaces apart</code></td>
  </tr>
  <tr>
    <td><code>\\</code></td>
    <td>Backslash</td>
    <td><code>\\</code></td>
    <td><code>\</code></td>
  </tr>
</tbody>
</table>

<h2 id="op-tbl">Operator table</h2>

<table>
<thead>
  <tr>
    <th>Operator</th>
    <th>Name</th>
    <th>Syntax</th>
    <th>Associativity</th>
    <th>Example</th>
    <th>Result</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><code>+</code></td>
    <td>Add</td>
    <td><code>x + y</code></td>
    <td>Left to right</td>
    <td><code>8 + 3</code></td>
    <td><code>11</code></td>
  </tr>
  <tr>
    <td><code>-</code></td>
    <td>Subtract</td>
    <td><code>x - y</code></td>
    <td>Left to right</td>
    <td><code>10 - 3</code></td>
    <td><code>7</code></td>
  </tr>
  <tr>
    <td><code>*</code></td>
    <td>Multiply</td>
<td><code>x* y</code></td>
    <td>Left to right</td>
    <td><code>3 * 4</code></td>
    <td><code>12</code></td>
  </tr>
  <tr>
    <td><code>/</code></td>
    <td>Divide</td>
    <td><code>x / y</code></td>
    <td>Left to right</td>
    <td><code>10 / 2</code></td>
    <td><code>5</code></td>
  </tr>
  <tr>
    <td><code>**</code></td>
    <td>Power</td>
    <td><code>x ** y</code></td>
    <td>Right to left</td>
    <td><code>11 ** 3</code></td>
    <td><code>1331</code></td>
  </tr>
  <tr>
    <td><code>//</code></td>
    <td>Floor Divide</td>
    <td><code>x // y</code></td>
    <td>Left to right</td>
    <td><code>10 // 3</code></td>
    <td><code>3</code></td>
  </tr>
  <tr>
    <td><code>&amp;</code></td>
    <td>Bitwise and</td>
    <td><code>x &amp; y</code></td>
    <td>None</td>
    <td><code>8 &amp; 1</code></td>
    <td><code>0</code></td>
  </tr>
  <tr>
    <td><code>^</code></td>
    <td>Bitwise xor</td>
    <td><code>x ^ y</code></td>
    <td>Left to right</td>
    <td><code>19 ^ 21</code></td>
    <td><code>6</code></td>
  </tr>
  <tr>
    <td><code>|</code></td>
    <td>Bitwise or</td>
    <td><code>x | y</code></td>
    <td>Left to Right</td>
    <td><code>5 | 6</code></td>
    <td><code>7</code></td>
  </tr>
  <tr>
    <td><code>&gt;</code></td>
    <td>Larger</td>
    <td><code>x &gt; y</code></td>
    <td>Left to right</td>
    <td><code>10 &gt; 7</code></td>
    <td><code>true</code></td>
  </tr>
  <tr>
    <td><code>&lt;</code></td>
    <td>Smaller</td>
    <td><code>x &lt; y</code></td>
    <td>Left to right</td>
    <td><code>9 &lt; 4</code></td>
    <td><code>false</code></td>
  </tr>
  <tr>
    <td><code>#</code></td>
    <td>Unary minus</td>
    <td><code>-x</code></td>
    <td>Right to left</td>
    <td><code>-10</code></td>
    <td><code>-10</code></td>
  </tr>
  <tr>
    <td><code>:</code></td>
    <td>???</td>
    <td><code>???</code></td>
    <td>???</td>
    <td><code>???</code></td>
    <td><code>???</code></td>
  </tr>
  <tr>
    <td><code>==</code></td>
    <td>Equals</td>
    <td><code>x == y</code></td>
    <td>None</td>
    <td><code>10 == 10</code></td>
    <td><code>true</code></td>
  </tr>
  <tr>
    <td><code>!=</code></td>
    <td>Unequal</code></td>
    <td><code>x != y</code></td>
    <td>None</td>
    <td><code>15 != 15</code></td>
    <td><code>true</code></td>
  </tr>
  <tr>
    <td><code>&lt;=</code></td>
    <td>Less than or equal to</td>
    <td><code>x &lt;= y</code></td>
    <td>Left to right</td>
    <td><code>7 &lt;= 6</code></td>
    <td><code>false</code></td>
  </tr>
  <tr>
    <td><code>&gt;=</code></td>
    <td>Greater than or equal to</td>
    <td><code>x &gt;= y</code></td>
    <td>Left to right</td>
    <td><code>63 &gt;= 63</code></td>
    <td><code>true</code></td>
  </tr>
  <tr>
    <td><code>in</code></td>
    <td>In</td>
    <td><code>x in y</code></td>
    <td>Left to right</td>
    <td><code>"foo" in "foo bar baz"</code></td>
    <td><code>true</code></td>
  </tr>
  <tr>
    <td><code>!in</code></td>
    <td>Not in</td>
    <td><code>x !in y</code></td>
    <td>Left to right</td>
    <td><code>"foo" !in "foo bar baz"</code></td>
    <td><code>false</code></td>
  </tr>
  <tr>
    <td><code>!{condition}</code></td>
    <td>Not</td>
    <td><code>!x</code></td>
    <td>Left to right</td>
    <td><code>!true</code></td>
    <td><code>false</code></td>
  </tr>
</tbody>
</table>
