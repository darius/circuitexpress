Circuit Express
===============

Introduction
============

In this book we'll build a computer in simulation, starting simple and
continuing until we've made a system able to run this very book. I say
'run', because this is best read at a computer, with the examples
performing as you read about them. Further, you're meant to read
actively: you'll solve problems by editing the code, which will appear
inline in the text.

[enticing example here. what could it be?]

In completing this you'll understand by example how a very complex
thing can work. You'll understand it deeply, dispelling the
magic. (*Do* computers work? Often they're great at annoying us. But
at the hardware level it's not just the often-emphasized speed that's
astonishing: beyond that, every visible result comes from millions of
operations, or more, in series, *all* of which must complete without
error. How can this be? On a pool table I can't even direct the cue
ball to hit a ball to hit a ball into the pocket, not reliably. One
second of computing is like a billion-carom shot.)

[reword? -- yes, when a computer performs millions of operations just
to pop up an ad, it's done in a blink; but it should astonish you that
*all* those operations must complete without error. How can this be?]
[i feel like in editing these things down i keep making them more
stilted...]

[Raise Kragen's claim that with the principles we're going to learn, a
useful computer could have been built at any time since the
Neolithic. It was not electronics that was missing. Maybe defer this
point until the reader can judge it.]

Other complex things: life, the universe, and Euclid. Some themes seem
applicable to all. Complex behavior the reliable outcome of
suitably-organized simple rules. Layers of abstraction. Specification
and implementation.

[while these connections should be drawn, there's a real danger of
intimidating and appearing to overpromise]

Also an example of recursion: a self-explaining system. This is a
self-centered book. (Thus the working title.)

[To spell it out:
  * an express intro to digital circuits (but how 'express' is it
    really?)
  * circuits as a way to express some neat ideas
  * a circuit of expression in which the book metacircularly explains
    itself and stands as one example of such a loop
Is this at all evident? Too cute? Maybe "Circuit, express"?]

[redundant] Try the examples out as you read: they are live, and the
code implementing them will be there in the text for you to read,
understand, and edit. Edit them, solve problems, go in your own
direction. I will show my answers too, but you should try to do things
yourself first. Math reading protocol; but computers can support it in
many ways better than paper can.


Prerequisites and alternatives
==============================

You should be able to program and willing to work. We will code in
Javascript [or whatever]. A book on these topics could teach
programming along the way, I believe, but this is not that book.

This isn't just a self-centered book -- I'm a self-centered author,
trying to write what I'd like to read. [specifics] I am a programmer,
and my hardware designs are not meant to be competitive.

_Eloquent Javascript_, is very good for improving your Javascript and
as another example of a dynabook. (This book will use the author's
CodeMirror editor.)

Maybe the Khan Academy CS program too / instead.

_The Elements of Computing Systems_ also builds a complete, simple
computer in simulation from the bottom up. It's also excellent. It's
on paper with accompanying software in Java. Their design has many
layers to keep each layer simple, making the system as a whole less
simple and powerful than I'm hubristically aiming for. They keep a
tighter focus than mine, as well. Their computer does not simulate
itself or the book about it.

_Structure and Interpretation of Computer Programs_, one of the great
books in computing, also develops a computer design in simulation, as
one topic among many, not quite connecting the layers from the gates
to the compiler.

_Computation Structures_, an older and less well-known book, aims for
a course like TECS but in greater depth. It looks really good, but I
have not read it so far.

Wirth's _Digital Circuit Design_.

_The Pattern on the Stone_. _Code_. _Feynman Lectures on Computation_.

There are several books that use programming to teach a subject
deeply, like _Structure and Interpretation of Classical Mechanics_.
(Most programming books are about programming.)

There's also a new genre of online video courses using programming
exercises in the browser, especially at Udacity.

[streamline?]


A fancy lock
============

    From coupler-flange to spindle-guide I see Thy Hand, O God --
    Predestination in the stride o' yon connectin'-rod.
    John Calvin might ha' forged the same -- enorrmous, certain, slow --

      -- Kipling, "McAndrew's Hymn"

[self-indulgent quote. delete?]

[better first example? well, i wonder if locks were in fact the
earliest machines to make discrete decisions -- that'd deserve
mention.]

To learn to design machines with arbitrarily fancy behavior, we'll
start on the only slightly fancy. Let's make a robot doorkeeper. It
will slide a bolt to the right, unlocking the door, under these
conditions:

  * when it's daytime and the members' key is turned;
  * or at any time when the owner's key is turned.

For concreteness we'll think of a real mechanical automaton that
signals this overall decision -- moving the bolt left or right --
given mechanical signals for the basic decisions: a rod that's pushed
right/left when it's daytime/nighttime, another going right/left when
the members' key is turned or not, and likewise for the owner's key.
In Javascript:

    function bolt(ownerKey, memberKey, daytime) {
        if (daytime === 'right' && memberKey === 'right')
            return 'right';
        else if (ownerKey === 'right')
            return 'right';
        else
            return 'left';
    }

How might you accomplish this? Let's not worry about evildoers
actively subverting our mechanism [see, not best example]. We have
three rods each pushed back or forth, plus another we wish to connect
to them somehow so they drive it left or right as listed above.

(Please stop and think how you'd do this. Maybe make a really sketchy
sketch on paper. If you're handy and feel like cobbling an actual
linkage together, I'd like to see it.) [with lego?]

[ad-hoc solution here. knob on owner's shaft pushes output shaft;
spring pushes back left when owner's not turned. another spring
pushing shaft right is unblocked when both daytime and member shafts
are at right (there's a blocking knob on each). maybe could be a bit
simpler. make a live diagram, oh joy? first question too hard? we're
not going to stay mechanical, you know. but hell, i'm sure not
mechanical. i don't know. it is important however to start at a
super-concrete level or people will engage their instructing-homunculi
thought-set instead of inanimate-causality. homunculi are useful but
magical.]

Let's put this in a more general setting. Here's our problem in
table form:

    owner key | member key | daytime   || door bolt
    ---------------------------------------------
     left     |  left      |  left     ||  left    
     left     |  left      |  right    ||  left
     left     |  right     |  left     ||  left    
     left     |  right     |  right    ||  right   
     right    |  left      |  left     ||  right   
     right    |  left      |  right    ||  right   
     right    |  right     |  left     ||  right   
     right    |  right     |  right    ||  right   

[format the columns without repeating the left left left left etc]
[code table in javascript?]

To specify an arbitrarily complicated decision depending on
arbitrarily many variables, we could just make a bigger table with
more columns and fill in the output columns as appropriate. Given such
a table, how can we design a machine to realize it? Is there a general
method? (Here's a good moment to pause again. I'm not going to keep
marking them, though soon there will be affordances for coding at such
points.)

One way is very direct: physically inscribe the table's output column
as pits and raised spots, addressed by an arm that's moved by
different amounts or directions by the input signals. An electronic
form of this can surely be found in the computer you're reading this
on (the ROMs).

[also like an old-fashioned music-box, except that's read sequentially]

For small tables or tables with no particular logic to them, this is
economical. However, a table quickly grows monstrous as the number of
inputs increases. (If you add another input column, how many rows must
be added?) For tables following some pattern (like the one above --
see the door-bolt column), we can hope to do much better by reflecting
the pattern somehow in the structure of the machine we design.

So here's another way, found by George Boole in the 19th century. He
published his discovery as _An Investigation Into the Laws of
Thought_; but in the 20th century Claude Shannon reapplied it as
'merely' a general way to compose decisions.

[note Stoic logic scooped Boole by two millennia yet fell into
near-oblivion in late antiquity. IIRC Russo traces some influence from
them to Boole. look into this enough to say something.]


Composing decisions
===================

[on second thought: this business of writing out a table and then
reducing it to muxes, isn't it dwelling too much on the obvious for a
reader who already can program? so, do it as exercises instead:
  * convert a particular small table to if-then-elses
  * write a function to convert any table to muxes]

Following Boole, our table

    owner key | member key | daytime   || door bolt
    ---------------------------------------------
     left     |  left      |  left     ||  left    
     left     |  left      |  right    ||  left
     left     |  right     |  left     ||  left    
     left     |  right     |  right    ||  right   
     right    |  left      |  left     ||  right   
     right    |  left      |  right    ||  right   
     right    |  right     |  left     ||  right   
     right    |  right     |  right    ||  right   

can be written as an if-then-else choosing between two smaller tables:

    if (ownerKey === 'left') {

                member key | daytime   || door bolt
                ---------------------------------
                 left      |  left     ||  left    
                 left      |  right    ||  left
                 right     |  left     ||  left    
                 right     |  right    ||  right   

    } else { // (we take 'left' and 'right' to be the only choices)

                member key | daytime   || door bolt
                ---------------------------------
                 left      |  left     ||  right   
                 left      |  right    ||  right   
                 right     |  left     ||  right   
                 right     |  right    ||  right   

    }

We can do the same to the first remaining table:

    if (ownerKey === 'left') {
        if (memberKey === 'left') {

                             daytime   || door bolt
                             --------------------
                              left     ||  left    
                              right    ||  left

        } else {

                             daytime   || door bolt
                             --------------------
                              left     ||  left    
                              right    ||  right   

        }
    } else {

                member key | daytime   || door bolt
                ---------------------------------
                 left      |  left     ||  right   
                 left      |  right    ||  right   
                 right     |  left     ||  right   
                 right     |  right    ||  right   

    }

continuing until they're all gone:

    if (ownerKey === 'left') {
        if (memberKey === 'left') {
            return 'left';
        } else {
            if (daytime === 'left') {
                return 'left';
            } else {
                return 'right';
            }
        }
    } else {
        return 'right';
    }

So with enough copies of one device, which functions like
if-then-else, we could realize any table. This device is called a
multiplexer -- 'mux' for short.

We've been writing Javascript statements declaring our desire: what
decision we want our machine to make. Now we'll write code to
implement it: to build (a model of) a machine.

    bolt = mux(ownerKey, mux(memberKey, left,
                                        mux(daytime, left,
                                                     right)),
                         right);


A machine to compel assent
==========================

These ideas came out of logic. true/false or 1/0 for right/left.

  and(a, b) = mux(a, false, b), etc.

  De Morgan's theorem corresponds to swapping left and right:
  the mirror image of a working machine also works.

In logic the point was to build and analyze arguments; a sound
argument corresponds to a machine that outputs 'true', oblivious to
its inputs. Equiv. to SAT.

(Write a program to test for this.)

We can apply logic to specify and check our designs.


Tic-tac-toe
===========

Now that we can build circuits, let's make a nontrivial one: a
tic-tac-toe player. I supply a minimax program, you turn it into a
circuit.

[other ideas? what's fun to do with just combinational circuits? if i
supply the program, does that make it too easy? well, that's good!
but my favorite reader would like to be offered some challenges too.]


OK, but...
==========

We just built quite a large circuit, in human terms. Can the same
methods scale up from a simple lock?

Hillis's tic-tac-toe in Lego. It barely worked.

Noise margins, restoring signals, and the digital abstraction. Error
correction. Rough correspondence to verbal vs. written culture and
inferring original texts.

Problems for the reader: simulate crappy components. How cheap can we
get away with? Given a circuit designed for perfect components,
synthesize an equiv one in crappy components using majority voting to
improve reliability.

Power dissipation.

Some other substrates, briefly: electronics, fluidics, biomolecular
reaction networks. (Electronics: practical. Fluidics: similar logic
but using physics more familiar to people. Reaction networks: cool
cutting-edge stuff.)

The cost of abstraction. A few alternatives.


Cheaper logic
=============

circuit efficiency. BDDs as ordered tests + chunking.

Problems for reader: Smaller tic-tac-toe player computed via BDD?
Use BDD to verify a design?


Simulation and simulacra
========================

simulating logic with logic. PLAs/FPGAs. universal machines.

[Is it possible to sketch out NP-completeness of SAT in the language
we've built up so far? Because that would make a great capstone to
this first section of the book.]


State machines
==============

Candidate examples/projects: combination lock. coin matching
game. tic-tac-toe by reinforcement learning. mouse in a
maze. something like Agre & Chapman's Pengo agent?

Extend/rewrite our HDL and simulator.

Are regular expressions worth bringing up here?


An impractical computer
=======================

A 1-bit 1-instruction universal computer. (OK, the addresses are >1
bit.) Compiling our tic-tac-toe program for it.

Computability.


A slightly less impractical computer
====================================

The lambda calculus as a core subset of Javascript. A CEK-machine
call-by-value interpreter like Scheme-79 chip.


Scheme (or equivalent)
======================

Extending the lambda calculus. Expanding out vs. adding core forms.


Parsing
=======

PEGs


A subset of Javascript
======================

(or whatever the hell language we decide to use for this book)


Once around the circuit
=======================

Running this book (very slowly) in simulation, with rather abstract
I/O.


Compiling
=========


Arithmetic and RISC machines
============================


A compiling logic simulator
===========================
