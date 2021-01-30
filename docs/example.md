<br>
<p align="center">
   <h3 align="center">Documentation</h3>
  
  <p align="center">
    Welcome to the QBall Documentation!
    <br>
    <a href="https://github.com/KingsleyDockerill/QBall/" rel="help"><strong>Home »</strong></a>
    ·
    <a href="https://github.com/KingsleyDockerill/QBall/issues" rel="next">Report Bug</a>
    ·
    <a href="https://github.com/KingsleyDockerill/QBall/issues" rel="next">Request Feature</a>
    ·
    <a href="https://trello.com/b/cJM6HsR3/qball" rel="external">Trello board</a>
    ·
    <a href="https://repl.it/@qballlang/QBall" rel="external">QBall Shell</a>
   <br>
   <a href="README.md#wel" rel="prev">« Back</a>
   ·
   <a href="math.md#math" rel="next">Next »</a>
   <br>
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
      <a href="README.md#wel">Welcome</a>
    </li>
    <li>
      <a href="example.md#ex">Examples</a>
      <ul>
        <li><a href="example.md#hw">Hello World</a></li>
        <li><a href="example.md#of">Output function</a></li>
        <li><a href="exmaple.md#oe">Output Elements</a></li>
        <li><a href="example.md#rpy8bc">Run Python & 8Ball code</a></li>
      </ul>
    </li>
    <li><a href="math.md#math">Math</a></li>
    <li><a href="escape-character.md#esc-char">Escape Characters</a></li>
    <li><a href="comment.md#comment">Comments</a></li>  
    <li><a href="function.md#funct">Functions</a></li>
    <li><a href="if-else.md#if-else">If / Else</a></li>
    <li><a href="variables.md#var">Variables</a></li>
    <li>
      <a href="input-output.md#io">Input and Output</a>
      <ul>
        <li><a href="input-output.md#out">Outputting</a></li>
        <li><a href="input-output.md#in">Input</a></li>
      </ul>
    </li>
    <li><a href="data-type.md#data-type">Data types</a></li>
    <li><a href="escape-character-table.md#esc-char-tbl">Escape character table</a></li>
    <li><a href="operator-table.md#op-tbl">Operator table</a></li>
  </ol>
</details>

<!-- EXAMPLES-->
<h2 id="ex">Examples</h2>

> __NOTE:__ Even though it looks simular, these are written in QBall <code>.qball</code>, not python <code>.py</code>.

<!-- HELLO WORLD-->
<h3 id="hw">Hello World</h3>

<pre>
out 'Hello world!'
</pre>

<!-- OUTPUT FUNCTION -->
<h3 id="of">Output function</h3>

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
<h3 id="oe">Output Elements</h3>

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
<h3 id="rpy8bc">Run Python & 8Ball code</h3>

<pre>
out "Enter some QBall code: " newline=0;
in a;
out "Enter some Python code: " newline=0;
in b;
qstr a;
py b
</pre>

