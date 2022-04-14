# Best practices cpp (WORK IN PROGRESS)

This package containts a few practices considered good when developing in cpp. 

## Coding Style

Consider using the [Anybotics](https://anybotics.github.io/styleguide/cppguide.html) cpp coding style guide. It has been adopted from Google coding style guide. Google coding style guide has been crafted by expert software engineers dealing with large codebases over extended periods of time. Anybotics coding style guide adds a few modificatinos that make it more suitable for robotics and usage with ROS. 

## ROS integration

ROS should be used as the middle layer for nodes to communicate. For your main code, create standalone libraries and provide a ROS-interface. Don’t put ROS dependencies in the core of your algorithm! (From here)

A good example on how to properly do this is the grid_map package from Anybotics: [grid_map](https://github.com/ANYbotics/grid_map).

## Software design

There are plenty of resources about software design online, however they can all (give or take) be traced to a few simple princliples called SOLID design ([wiki](https://en.wikipedia.org/wiki/SOLID)). It is recommended to
familiarize yourself with those principles. You can find a quick overview with some examples [here](https://www.digitalocean.com/community/conceptual_articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design#single-responsibility-principle).


1. **The single-responsibility principle**  
  "There should never be more than one reason for a class to change."
   I.e. every class should have only one responsibility. This principle also applies to functions (non class members) [more](https://www.cs.utexas.edu/users/downing/papers/SRP-1996.pdf)
2. **The open–closed principle** 
   "Software entities should be open for extension, but closed for modification."
   I.e. If you want do add a new feature you should be able to do so without having to change the existing code (ideally). [more](https://courses.cs.duke.edu/fall07/cps108/papers/ocp.pdf)
3. **The Liskov substitution principle**  
  "Functions that use pointers or references to base classes must be able to use objects of derived classes without knowing it."   
  I.e. The derived function must not change function of the base class, it can only add more (specialized) functionality. [more](https://www.labri.fr/perso/clement/enseignements/ao/LSP.pdf)
4. **The interface segregation principle**  
   "Many client-specific interfaces are better than one general-purpose interface."
   I.e. The interface should be designed slim (ideally about 7 methods in the public interface). [more](https://www.cs.utexas.edu/users/downing/papers/ISP-1996.pdf)
5. **The dependency inversion principle**  
   "Depend upon abstractions, not concretions." 
   I.e. you should not expose the implementation details of your class in the public interface. [more](https://www.labri.fr/perso/clement/enseignements/ao/DIP.pdf)
   
 A decent book that shows how some of these princliples can be applied is *Clean Architecture: A Craftsman's Guide to Software Structure and Design* [link](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
 
 In addition consider reading a book about design patterns which basically show you how to apply these 5 principles in various situations. A decent, easy read on design patterns is *Head First Design Patterns*. It is written for Java, yes, however the principles are language agnostic. [link](https://www.amazon.com/Head-First-Design-Patterns-Brain-Friendly/dp/0596007124)
 
### Idioms

There are multiple useful idioms that you can find, however one that is particulary useful in terms of breaking dependencies is the PIMPL idiom.
You can find a brief explanation of what it does [here](https://cpppatterns.com/patterns/pimpl.html).


## Writing expressive code


### Naming
The code should convey the intent of the programmer. The best (and the easiest) way of writing expressive code starts with good naming. Choose names for you variables/functions that describe what the variable/function is doing. The price we have to pay is that our names will become slightly longer, yes, we will spend more time typing. However consider how much time you will save yourself if you have to look at the same code after a few months.

Consider this example:

```cpp
if( i >=0 && i < data.rows()){
    // do stuff
}
```
vs

```cpp
const bool isIndexValid =  i >=0 && i < data.rows()
if(isIndexValid){
    // do stuff
}
```
Which version do you find easier to understand?

In this exapmle we used an extra variable to better convey our intention. 

### Functions

Same as the classes, your functions should do one thing. A well written function is typically no longer than 30ish lines; a good thumb rule is that the whole function should be able to fit on your screen. If you have to scroll through it, most likely it can be broken down into multiple smaller functions.  

Structuring code into funtions allows you to improve resusability and avoid code copy-pasting. Even if you will not need to re-use the functinality by separating a chunk of code in a function, you can still (vastly) improve the readability of your code.

Consider a following example:

```cpp
int nElements = data.size();
for (int i = 0; i < nElements; ++i){
  for(int j = 0; j < nElements; ++j){
    if( j != i) {
      if (data.at(i) == data.at(j)){
        data.erase(data.begin() + j);
        nElements--;
        i = 0;
      }
    }
  }
}
```

vs 

```cpp

auto removeElementByIndex = [&](int idx) -> void {
  data.erase(data.begin() + idx);
};

auto getIndexOfFirstDuplicateElement = [&] (int *returnValue) -> bool {
  for (int i = 0; i < data.size(); ++i){
    for(int j = i+1; j < data.size(); ++j){
      if( data.at(i) == data.at(j)) {
        *returnValue = j;
        return true;
      }
    }
  }
  return false;
};

int duplicateIdx = -1;
while(getIndexOfFirstDuplicateElement(&duplicateIdx)){
  removeElementByIndex(duplicateIdx);
}
```

Which code block was easier to understand?  

As you might have guessed both variants remove the duplicate elements from a vector. Here we used lambda functions to convey our intent better, however one could also use regular functions or class methods.

A good book on how to write expressive code is *Clean Code: A Handbook of Agile Software Craftsmanship* [link](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882). This book explains well how to name your functions/variables.  

There is also a great blog on writing expressive code in cpp. It is easy to read and provides ample of examples to facilitate understanding. [link](https://www.fluentcpp.com/posts/)

## Using STL

If you can, you should use STL (Standard Template Library).

1. STL algorithms are correct and have been extensively tested. This allows you to gracefully handle corner cases, avoid off by one errors, implicit casting errors and all kinds of other nasty stuff that you might oversee in your quick and dirty implementation of a possibly-existing-in-stl algorithm.
2. STL is well documented. Indeed if you look what [std::min_element](https://en.cppreference.com/w/cpp/algorithm/min_element) (used in the example), you will find plenty of info with examples. This means that someone has done the annoying documentation writing for you and you can focus on getting your task done instead of worrying about commenting/documenting your implementation.
3. STL can help you write expressive code. Take a look at the example below:

STL example:

```cpp
double minElement = 1e8; // oops what will this snippet do if data containts numbers > 1e8 ???
for(int i=0; i < data.size(); ++i){
  if (minElement < data.at(i)){
    minElement = data.at(i);
  }
}
```
vs

```cpp
double minElement = *std::min_element(data.begin(), data.end());
```

Which snippet took less time to read and understand?  

Note that STL has many functinos implemented and you can often use it to easily convey your intent. A great resource for exploring various usages of STL is (again) the [fluentCPP](https://www.fluentcpp.com/STL/) blog.

