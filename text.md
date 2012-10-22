Introduction
============

In this book we'll build a computer in simulation, starting simple and
continuing until we've made a system able to run this very book. I say
'run', because this is best read at a computer, with the examples
acting out as you read about them. Beyond that, you're meant to read
actively: to solve problems by editing the code, which will appear
inline in the text.

Understand by example how a very complex thing can work. Understand it
deeply, dispelling the magic.
  Other complex things: life, the universe, and Euclid.

Also example of recursion: a self-explaining system.

[while these connections should be drawn, there's a real danger of
intimidating and appearing to overpromise]

[redundant] Try the examples out as you read: they are live, and the
code implementing them will be there in the text for you to read,
understand, and edit. Edit them, solve problems, go in your own
direction. I will show my answers too, but you should try to do things
yourself first. Math reading protocol; but computers can support it in
many ways better than paper can.


Prerequisites and alternatives
==============================

You should be able to program and willing to work. [And smart enough
to be fun to write for, but I can't say that, can I? Anyway enough
work makes up for a lot.] A book on these topics could teach
programming along the way, I believe, but this is not that book.

_Eloquent Javascript_, is very good for improving your Javascript and
as another example of a dynabook. (This book will use the author's
CodeMirror editor.)

Maybe the Khan Academy CS program too / instead.

_The Elements of Computing Systems_ also builds a complete, simple
computer in simulation from the bottom up. It's also excellent. It's
in paper + Java. Their design has many layers to keep each layer
simple, making the system as a whole less simple and powerful than I'm
hubristically aiming for. They keep a tighter focus than mine, as
well.

_Structure and Interpretation of Computer Programs_, one of the great
books in computing, also develops a computer design in simulation, as
one topic among many, not quite connecting all the layers from the
gates to the compiler.

_Computation Structures_, an older and less well-known book, aims for
a course like TECS but in greater depth. It looks really good, but I
have not read it so far.

There are several books that use programming to teach a subject
deeply, like _Structure and Interpretation of Classical Mechanics_.
(Most programming books are about programming.)

There's also a new genre of online video courses using programming
exercises in the browser, especially at Udacity.

[ok, I spent too much time on that]


Composing decisions
===================

[better first example? come on? um... nuclear launch codes?]

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

How might you accomplish this? Let's not worry about evildoers
actively subverting our mechanism [see, not best example]. We have
three rods each pushed back or forth, and another we wish to connect
to them somehow so they drive it left or right as listed above.

(Please stop and think how you'd do this. Maybe make a really sketchy
sketch on paper. If you're handy and feel like cobbling an actual
linkage together, I'd like to see it.)

[ad-hoc solution here. knob on owner's shaft pushes output shaft;
spring pushes back left when owners' not turned. another spring
pushing shaft right is unblocked when both daytime and member shafts
are at right (there's a blocking knob on each). maybe could be a bit
simpler. make a diagram, oh joy? first question too hard? we're not
going to stay mechanical, you know. but hell, i'm sure not
mechanical. i don't know. it is important however to start at a
super-concrete level or people will engage their instructing-homunculi
thought-set instead of inanimate-causality. homunculi are useful but
magical.]

Let's put this in a more general setting. Here's our problem in
table form:

    owner key | member key | daytime || door bolt
    ---------------------------------------------
       left   |  left      |  left   ||  left    
       left   |  left      |  right  ||  left
       left   |  right     |  left   ||  left    
       left   |  right     |  right  ||  right   
       right  |  left      |  left   ||  right   
       right  |  left      |  right  ||  right   
       right  |  right     |  left   ||  right   
       right  |  right     |  right  ||  right   

To specify an arbitrarily complicated decision, we could just make a
bigger table with more variables and fill in the output columns as
appropriate. Given such a table, how can we design a machine to
realize it? Is there a general method? (This is a good moment to pause
again. I'm not going to keep marking them, though soon there will be
affordances for coding at such points.)

One way is very direct: physically inscribe the table as pits and
raised spots for the output variable, addressed by an arm that's moved
by different amounts or directions by the input signals. An electronic
form of this is bound to be in the computer you're reading this with
(the ROMs).

However, for tables with a nonrandom pattern (like the one above --
see the door-bolt column), a ROM gets less and less economical as the
number of inputs increases. (If you add another input variable, how
big must the table become?)

So here's another way, discovered by George Boole in the 19th
century. He thought of his discovery overoptimistically as the laws of
thought; it took till the 20th century for Claude Shannon to think of
the same ideas as a general way to compose decisions.
