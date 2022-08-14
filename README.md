# IEEE 754 floating-point addition for neuromorphic architecture
Arun M.George, Rahul Sharma, Shrisha Rao

## Abstract
Neuromorphic computing is looked at as one of the promising alternatives to the traditional von Neumann architecture. In this paper, we consider the problem of doing arithmetic on neuromorphic systems and propose an architecture for doing IEEE 754 compliant addition on a neuromorphic system. A novel encoding scheme is also proposed for reducing the inter-neural ensemble error. The complex task of floating point addition is divided into sub-tasks such as exponent alignment, mantissa addition and overflow-underflow handling. We use a cascaded approach to add the two mantissas of the given floating-point numbers and then apply our encoding scheme to reduce the error produced in this approach. Overflow and underflow are handled by approximating on XOR logic. Implementation of sub-components like right shifter and multiplexer are also specified.

Link to full paper: https://doi.org/10.1016/j.neucom.2019.05.093

**Note:** Source code is available for usage under GNU GPL v. 3
