+++
title = "Building an Image Processing App With Go, #0"
date = "2025-08-03T12:05:44-03:00"
author = "Douglas Domingos"
tags = ["parallelism", "image-processing", "go"]
keywords = ["concurrent-programming", "image-processing", "go", "golang"]
description = "How a CS50's problem set became one of the most interesting projects I've worked so far."
showFullContent = false
readingTime = true
hideComments = false
+++

It's been quite a while since my last post. I've been meaning to write something new here for some
time, but failed to find both an interesting topic and the patience to sit down and think about new
posts. It wouldn't be a understatement to say that, for the last few months, life has been running
on full auto-pilot. Regardless, I hope you are managing to stay afloat amidst the chaos.

Last semester, I completed the "Concurrent Programming" course - which, I must admit, was one of the
best courses I've taken so far in my degree - and was searching for some project idea to test out my
new set of skills (and a self-excuse to learn more about Go). Then I thought: "why not develop an
image processing app, without relying on third-party libraries?".

Well, here we are. In this series, I'll discuss the design choices, the challenges faced during
the development process and their solutions.

## The idea and inspirations

The core idea was to build an application that would meet the following requirements:

- Apply filters of different types (e.g., Point-based, Convolution-based) to PNG/JPEG images
- Benchmark performace under execution settings (e.g., image sizes, number of workers)
- Encourage the use of various concurrency patterns (e.g., mutual exclusion, barriers)
- Efficiency in memory consumption and CPU usage

The main inspiration goes back to 2021, when I enrolled into Harvard's CS50 online course. The
course is structured in weeks, each focused on a major topic in Computer Science - Data Structures,
Algorithms, Computer Architechture, Computational Logic, and much more. Each Week also includes a
Problem Set, which is a small set of code problems to practice the concepts presented in the class.
Each problem if offered in two versions - `less` or `more` -, which differ in difficulty.

The [Problem Set 4](https://cs50.harvard.edu/x/2021/psets/4/) included `Filter`: a problem where the
student is tasked to implement a set of different filter algorithms. Wanting a challenge, I chose
the `more` version and, without doubt, I was in for a journey. Amongst the required implementations
was `Sobel`: an edge-detection algorithm that calculates the gradient magnitude of a pixel based on
its neighboring pixels. I spent about 10 days dwelling in this problem, trying to understand the
constraints and logic behind the algorithm - which, also, was fully implemented in C.

Later, in my Concurrent Programming class, we faced a similar challenge: processing images with a
multithreaded approach in Java. Since then, I've been planning to implement the CS50's `Filter`
problem as a way to revisit the challenge and apply what I’ve learned about concurrency in a more
practical way.

## First of all, why Go?

Of all the languages I've worked with so far, I've chosen to develop the application using Go. _"But
why not use Python or Java?"_, you may ask. Well, here's why:

- **Python**: although simple, it does not allow true multithreading because of its Global
  Interpreter Lock (GIL), which prevents multiple threads from executing code in Python's
  Interpreter. Parallelism may be achieved using the `multiprocessing` package, but it brings a
  larger overhead when compared to thread-based parallelism.

- **Java**: supports multithreading, but lacks the simplicity of Python's syntax. Aside from that,
  the built-in packages for image manipulation - although richer in features - are complex and
  verbose, due to their higher level of abstraction.

- **C**: without a doubt, it would be the best choice for performance, as it has no garbage
  collector and allows direct manipulation of pixels. However, since C provides almost no
  abstractions for image manipulation, much of the development effort would be spent on creating
  a basic codebase just to apply a filter.

As for Go, it provides exactly what the project required:

- Support for multithreading, based on the **Communicating Sequential Processes (CSP)** model
- Direct pixel manipulation without giving up abstraction
- Flexible syntax and rich built-in libraries that boost development speed

## Shared-memory concurrency

Most modern, mainstream languages use the traditional shared-memory concurrency model, where threads
share memory directly to exchange state. This was the most straightforward way to enable concurrent
execution of multiple tasks, dating back to the earliest iterations of operating systems.

However, shared-memory models require developers to explicitly manage access to shared resources
between threads, in order to ensure correctness of programs. As systems grew more and more complex,
so did the challenge of building reliable, thread-safe solutions to synchronization problems. The
main issues when building shared-memory concurrent systems are:

- **Race conditions**: occurs when threads access the same region of memory at the same time, where
  the result depends on the order of their accesses. If the access to the shared memory is not
  properly managed amongst threads, it may lead to inconsistent results and unpredictable behavior.

- **Deadlocks**: occurs when threads wait on each other in a circular dependency, with none able to
  proceed unless the others release resources — which never happens. Preventing deadlocks requires
  careful synchronization strategies, and may cause the program to simply freeze indefinitely.

## CSP - The concurrency model of Go

The way Go handles concurrency is fundamentally different from most mainstream languages - and
that's no surprise: Go's concurrency model is based on **Communicating Sequential Processes (CSP)**,
whereas languages like **C**, **Java** and **Python** use thread-based concurrency through shared
memory.

Although CSP isn’t widely discussed in programming courses, it's been around for at least four
decades. CSP is a formal model that describes communication between concurrent processes, proposed
in 1978 by Tony Hoare - the creator of the QuickSort algorithm. If you want to go a bit deeper about
CSP, you might find [this article](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2008-09/tony-hoare/csp.html)
interesting.

The core idea of CSP is that processes should share state by exchanging messages, rather than
accessing shared variables or data structures directly. This protects the program from race
conditions and often yields more simple and elegant code, eliminating the need for explicit,
error-prone synchronization techniques.

> *Don't communicate by sharing memory; share memory by communicating* - Go Proverbs

## Where are we going from here?

Now that we have covered the *why* behind this project and some core concepts of the concurrent
paradigm, it's time we dive into the *how*.

We'll walk through the evolution of the image processing module, how convolution-based filters were
parallelized, the design of filter pipelines, and how the application was benchmarked under
different settings.

In the next post of this series, we'll dive into the heart of the application: the parallelism model
that powers the filters - and the challenges faced while designing and implementing it.