# The Pi Calculus

The pi calculus is a process algebra innovated by Robin Milner. It provides an encoding for parallel computations via passing messages over channels.

This is a very bare-bones interpreter that implements the output and input prefix operators, as defined in [the Wikipedia page.](https://en.wikipedia.org/wiki/%CE%A0-calculus)

Currently, I only have a lexer, the process object, and the two reducible expression objects (SequentialRedex, ParallelRedex) necessary for carrying out basic computations, along with a test suite.

## Syntax & Example

As previously stated, only the input and output prefixes are currently implemented. The syntax looks like this:
```
z transits_over x.
y receives_from x; x transits_over y; y receives_from x.
v receives_from z; v transits_over v.
v receives_from x; x transits_over x.
```

Or, in general:

```
%value transits_over/receives_from %channel
```

The transits_over keyword is output prefixing. The receives_from keyword is input prefixing. Semicolons denote process prefixing; periods denote termination.

The interpreter will yield the following stacktrace for this example program:
```
"{'x': {'TRANSMITTING': ['z'], 'LISTENING': [||[<z TRANSMITTING y>, <y LISTENING x>, □]||, ||[<z TRANSMITTING x>, □]||]}, 'z': {'TRANSMITTING': [], 'LISTENING': [||[<v TRANSMITTING v>, □]||]}}", 

"{'y': {'TRANSMITTING': ['z'], 'LISTENING': []}, 'v': {'TRANSMITTING': ['v'], 'LISTENING': []}, 'x': {'TRANSMITTING': ['z'], 'LISTENING': []}}", 

"{'x': {'TRANSMITTING': [], 'LISTENING': [||[□]||]}}"
```
(I cleaned it up a bit for the readme)

## Why Do This?

This is purely a weekend-only passion project for an undergrad that expects to graduate soon.

I'm interested in programming language design :) I also think the pi calculus is really cool!

## What's Next?

In no particular order:
* Improve the lexer
* Improve the execution tactics + make the stacktrace more readable
* Introduce actual parallelism & concurrency by leveraging python's standard [multiprocessing module](https://docs.python.org/3/library/multiprocessing.html)

## Related Readings

* [Pattern Matching (Peters, Yonova-Karbe, Nestmann)](https://arxiv.org/pdf/1408.1454.pdf)
* [Functions as Processes (Milner)](https://hal.inria.fr/file/index/docid/75405/filename/RR-1154.pdf)
* [Applied Pi Calculus (Sewell)](https://www.cl.cam.ac.uk/~pes20/apppi.pdf)
* [Polyadic Pi Calculus (Milner)](https://courses.cs.vt.edu/~cs5204/fall09-kafura/Papers/PICalculus/Pi-Calculus-Tutorial.pdf)