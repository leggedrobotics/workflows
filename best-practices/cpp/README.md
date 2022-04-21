# Best practices cpp

This package containts a hints and examples for (more) effective cpp development.

## Coding Style

Consider using the [Anybotics](https://anybotics.github.io/styleguide/cppguide.html) cpp coding style guide. It has been adopted from Google coding style guide. Google coding style guide has been crafted by expert software engineers dealing with large codebases over extended periods of time. Anybotics coding style guide adds a few modifications that make it more suitable for robotics and usage with ROS.

The utility package [cmake_clang_tools](https://github.com/ANYbotics/cmake_clang_tools), available online, can be used to automatically run clang-tidy and clang-format on your code and helps you better adhere to the above mentioned guidelines.

No matter which coding style you choose, you should stick to it and be consistent. Each coding style comes with some tradeoffs and the only thing that matters in the end is consistency. Once you get used to the new coding style, you will save lots of time reading through the code.

## ROS integration

ROS should be used as the middle layer for nodes to communicate. For your main code, create standalone libraries and provide a ROS-interface. Don’t put ROS dependencies in the core of your algorithm!

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
 
### Example (encapsluation and dependency inversion principle)

Consider a mapping system with a `Submap` class,

```cpp
class Submap{
public:
  void doSomething();   
}
```

and two versions of `SubmapCollection` class, together with a client code that wants to erase a submap that 
is the the correct one (according to some criteria):

<table>
<tr>
<td> First version </td> <td> Second version </td>
</tr>
<tr>
<td>

```cpp
class SubmapCollection{
public:
  std::vector<Submap> &getSubmaps() { 
    return submaps_; 
  }
private:
  std::vector<Submap> submaps_;
}

//client code
  
SubmapCollection sc;
int theRightSubmapIdx;
// do stuff  
for(int i = 0; i < sc.getSubmaps().size(); ++i){
  // calculate theRightSubmapIndex
  sc.getSubmaps().at(i).doSomething();                   
}
auto startIt = sc.getSubmaps().begin();
sc.getSubmaps().erase(startIt + theRightSubmapIdx);
                                                        
  
```

</td>
<td>
    
```cpp
class SubmapCollection{
public:
  Submap &getSubmap(int submapId) { 
    return submaps_.at(submapId); 
  }
  void eraseSubmap(int id) {
    submaps_.erase(submaps_.begin() + id);
  }
  int size() const {
    return submaps_.size();
  }
private:
  std::vector<Submap> submaps_;
};

//client code
  
SubmapCollection sc;
int theRightSubmapIndex;
// do stuff  
for(int i = 0; i < sc.size(); ++i){
  // calculate theRightSubmapIndex
  sc.getSubmap(i).doSomething();
}
sc.eraseSubmap(theRightSubmapIndex); 
  
```
</td>
</tr>
</table>

Assume that erasing submaps can happen in many places in the client code. What happens if we for some reason have to use `std::vector<std::shared_ptr<Submap>>` inside `SubmapCollection`? What if we have to use `std::list`? In the first version, lots of  client code will break since we have exposed implementation details in the public interface.

### Idioms

There are multiple useful idioms that you can find, however one that is particulary useful in terms of breaking dependencies is the PIMPL idiom.
You can find a brief explanation of what it does [here](https://cpppatterns.com/patterns/pimpl.html).


## Writing expressive code


### Naming
The code should convey the intent of the programmer. The best (and the easiest) way of writing expressive code starts with good naming. Choose names for your variables/functions that describe what the variable/function is doing. The price we have to pay is that our names will become slightly longer, yes, we will spend more time typing. However consider how much time you will save yourself if you have to look at the same code after a few months.

Consider these two versions:
  
<table>
<tr>
<td> First version </td> <td> Second version </td>
</tr>
<tr>
<td>
  
```cpp
if (0 <= i && i < data.rows()){
    // do stuff
}
```

</td>
<td>
  
```cpp
const bool isIndexValid = 0 <= i && i < data.rows();
if ( isIndexValid ){
    // do stuff
}
``` 

</td>
</tr>
</table>

Which version do you find easier to understand?

In this example we used an extra variable to better convey our intention. 

### Functions

Same as the classes, your functions should do one thing. A well written function is typically no longer than 30ish lines; a good thumb rule is that the whole function should be able to fit on your screen. If you have to scroll through it, most likely it can be broken down into multiple smaller functions.  

Structuring code into funtions allows you to improve resusability and avoid code copy-pasting. Even if you will not need to re-use the functionality by separating a chunk of code in a function, you can still (vastly) improve the readability of your code.

Consider the following example:

<table>
<tr>
<td> First version </td> <td> Second version </td>
</tr>
<tr>
<td>
  
```cpp
for (int i = 0; i < data.size(); ++i){
  for(int j = i+1; j < data.size(); ++j){
    if (data.at(i) == data.at(j)){
      data.erase(data.begin() + j);
      j = i+1;
    }
  }
}
```

</td>
<td>
  
```cpp

// here we pass data by pointer but
// we could also use a reference
removeDuplicateElements(&data);
```

</td>
</tr>
</table>  

Which code block was easier to understand? As you might have guessed both variants remove the duplicate elements from a vector. Note that we don't really need to know how `removeDuplicateElements` is implemented, we only need to know what is it doing. You can find an (improved) implementation of `removeDuplicateElements` function below. You could also use the exact same implementation as in the first case.  
  
```cpp
void removeDuplicateElements(std::vector<int> *v){
    std::unordered_set<int> s;
    s.insert(v->begin(),v->end());
    v->resize(s.size());
    std::copy(s.begin(),s.end(),v->begin());
}
```

Yes, but I could just add a comment, why bother with functions?! Indeed, however, what would you find easier to debug? A big function with a comment stating what it does or a bunch of smaller functions with meaningful names and no comments? What happens if you update the code, but forget to update the comment?

A good book on how to write expressive code is *Clean Code: A Handbook of Agile Software Craftsmanship* [link](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882). This book explains well how to name your functions/variables.  

There is also a great blog on writing expressive code in cpp. It is easy to read and provides ample of examples to facilitate understanding. [link](https://www.fluentcpp.com/posts/)

## Using STL

If you can, you should use STL (Standard Template Library).

1. STL algorithms are correct and have been extensively tested. This allows you to gracefully handle corner cases, avoid off by one errors, implicit casting errors and all kinds of other nasty stuff that you might oversee in your quick and dirty implementation of a possibly-existing-in-stl algorithm.
2. STL is well documented. Indeed if you look what [std::min_element](https://en.cppreference.com/w/cpp/algorithm/min_element) (used in the example), you will find plenty of info with examples. This means that someone has done the annoying documentation writing for you and you can focus on getting your task done instead of worrying about commenting/documenting your implementation.
3. STL can help you write expressive code. Take a look at the example below:

STL example:
  
<table>
<tr>
<td> First version </td> <td> Second version </td>
</tr>
<tr>
<td>
  
```cpp
double minElement = 1e8; 
// oops
// what will this snippet do 
// if data containts only numbers > 1e8 ???
for(const auto &element : data){
  if (element < minElement){
    minElement = element;
  }
}
```

</td>
<td>
  
```cpp
double minElement = *std::min_element(data.begin(), data.end());
```

</td>
</tr>
</table>

Which snippet took less time to read and understand?  

Note that STL has many functions implemented and you can often use it to easily convey your intent. A great resource for exploring various usages of STL is (again) the [fluentCPP](https://www.fluentcpp.com/STL/) blog.

 ## Optimizing code
  
In general, it is a good idea to first make the code correct and then worry about the speed. Maybe it's fast enough; if it is, you're done and you save yourself valuable time that would have been spent optimizing otherwise. Note that optimizing the code often reduces readability and maintainability so you should have a good reason for doing so. This [blog](https://github.com/facontidavide/CPP_Optimizations_Diary) deals specifically with optimizations in cpp. Can you guess what is the No.1 rule that they list? 
  
 ## Other resources
 
**Online**  
  
[fluentCPP](https://www.fluentcpp.com/STL/) - Great blog that covers a wide variety of topics. Features short posts with exmaples that take only a few minutes to understand (daily cpp). You will definitely impress your friends at the bar with your vast knowledge.
  
[modernesCPP](https://www.modernescpp.com/index.php/modern-c) - Technical blog that covers some advanced concepts. Lots of resources on multithreading and modern cpp (C++17, C++20).
  
[optimizatinoDiary](https://github.com/facontidavide/CPP_Optimizations_Diary) - Funny blog that covers simple cpp optimizations. Mostly features stuff like: I change 3 lines of code and it runs 2x faster.
  
**Books**

*Clean Code: A Handbook of Agile Software Craftsmanship* [link](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882). Great book with examples on how to name your variables, functions and how to structure your code. If you can read only one, pick this one.
  
*Clean Architecture: A Craftsman's Guide to Software Structure and Design* [link](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164) - A comprehensive book on how to approach software design on a larger scale with examples and real-life stories.
 
*Head First Design Patterns*. [link](https://www.amazon.com/Head-First-Design-Patterns-Brain-Friendly/dp/0596007124) - Design patterns and how do they adhere to SOLID design principles. Comic style book. Easy to read.
  
*Effective C++: 55 Specific Ways to Improve Your Programs and Designs* [link](https://www.amazon.com/Effective-Specific-Improve-Programs-Designs/dp/0321334876) - Slightly older book that covers a wide variety of topics from memory management to templates and generic programming. It's divided into 55 easy-to-read items so you can skip what is not relevant for you.
  
*Effective Modern C++: 42 Specific Ways to Improve Your Use of C++11 and C++14* [link](https://www.amazon.com/Effective-Modern-Specific-Ways-Improve/dp/1491903996) - Same style as *Effective C++* but focuses on C++11 and C++14. Probably better to read the *Effective C++ first.
  

  


