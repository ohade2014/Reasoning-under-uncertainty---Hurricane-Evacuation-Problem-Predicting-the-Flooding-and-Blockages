# Reasoning-under-uncertainty---Hurricane-Evacuation-Problem-Predicting-the-Flooding-and-Blockages
Probabilistic reasoning using Bayes networks, wrote in python.
We have a binary random variable Fl(v,t) standing in for "flooding" at vertex v at time t, 
and a binary variable B(e,t) standing in for "blocked" for each edge e at time t. The flooding events are assumed independent, 
with known distributions. The blockages are noisy-or distributed given the flooding at incident vertices at the same time t, 
with pi =(1-qi)= 0.6*1/w(e). All noisy-or node have a leakage probability of 0.001, that is, 
they are true with probability 0.001 when all the causes are inactive. 
The leakage may be ignored for the cases where any of the causes are active.

Flooding probabilities P(Fl(v,0)=true) at vertices for time 0 are provided in the input. 
For subesquent times (t=1,2, etc.) they are dependent only on the occurence of flooding at the previous time slice, 
we will have: P(Fl(v,t+1)=true |Fl(v,t)=true))=Ppersistence, where Ppersistence is a user-determined constant (usually between 0.7 and 0.99),
and P(Fl(v,t+1)=true |Fl(v,t)=false))=P(Fl(v,0)=true). Such a network of variables indexed by time, 
that aims at modeling the dynamics of the world, is sometimes called a Dynamic Bayes Network (DBN).

There are 2 types of variables (BN nodes): blockages (one for each edge and time unit) flooding (one for each vertex, and time unit).

A file specifies the geometry (graph), and parameters such as P(Fl(v)=true)). 
Then, enter some locations where flooding and blockages are reported either present or absent (and the rest remain unknown). 
This is the evidence in the problem. Once evidence is instantiated, we perform reasoning about the likely locations of flooding, blockages,
and evacuees (all probabilities below "given the evidence"):

What is the probability that each of the vertices is flooded?
What is the probability that each of the edges is blocked?
What is the probability that a certain path (set of edges) is free from blockages? (Note that the distributions of blockages in edges are NOT necessarily independent.)
What is the path between 2 given vertices that has the highest probability of being free from blockages at time t=1 given the evidence? (bonus)
