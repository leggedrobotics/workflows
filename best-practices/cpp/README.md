# Best practices cpp

This package containts a few practices considered good when developing in cpp. 



## ROS integration

ROS should be used as the middle layer for nodes to communicate. For your main code, create standalone libraries and provide a ROS-interface. Don’t put ROS dependencies in the core of your algorithm! (From here)

A good example on how to properly do this is the grid_map package from Anybotics: [grid_map](https://github.com/ANYbotics/grid_map).

## Software design

There are plenty of resources about software design online, however they can all (give or take) be traced to a few simple princliples called SOLID design [wiki](https://en.wikipedia.org/wiki/SOLID). It is recommended to
familiarize yourself with those principles. You can ind a quick overview with examples [here](https://www.digitalocean.com/community/conceptual_articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design#single-responsibility-principle).


1. **The single-responsibility principle**  
  "There should never be more than one reason for a class to change."
   I.e. every class should have only one responsibility. [more](https://www.cs.utexas.edu/users/downing/papers/SRP-1996.pdf)
2. **The open–closed principle** 
   "Software entities should be open for extension, but closed for modification."
   I.e. If you want do add a new feature you should be able to do so without having to change the existing code (ideally). [more](https://courses.cs.duke.edu/fall07/cps108/papers/ocp.pdf)
3. **The Liskov substitution principle**  
  "Functions that use pointers or references to base classes must be able to use objects of derived classes without knowing it." [more](https://www.labri.fr/perso/clement/enseignements/ao/LSP.pdf)
   I.e. The derived function must not change function of the base class, it can only add more (specialized) functionality.
4. **The interface segregation principle**  
   "Many client-specific interfaces are better than one general-purpose interface."
   I.e. The interface should be designed slim (ideally about 7 methods in the public interface). [more](https://www.cs.utexas.edu/users/downing/papers/ISP-1996.pdf)
5. **The dependency inversion principle**  
   "Depend upon abstractions, not concretions." 
   I.e. you should not expose the implementation details of your class in the public interface. [more](https://www.labri.fr/perso/clement/enseignements/ao/DIP.pdf)


