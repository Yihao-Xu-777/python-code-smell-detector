# Code Smell Rule Definitions

This document describes the detection rules used in the first version of the Python Code Smell Detector.

## 1. Long Method

A function is reported as a Long Method if its length is greater than 30 lines.

Reason: Long functions are usually harder to understand, test, and maintain.

## 2. Too Many Parameters

A function is reported as having Too Many Parameters if it has more than 5 parameters.

Reason: Too many parameters may indicate that the function has too many responsibilities.

## 3. Deep Nesting

A function is reported as having Deep Nesting if the nesting depth of if, for, or while statements is greater than 3.

Reason: Deeply nested code is usually harder to read and more difficult to debug.

## 4. Magic Number

A number is reported as a Magic Number if it appears directly in the source code and is not -1, 0, or 1.

Reason: Unnamed numeric constants may reduce code readability.

## 5. Broad Exception

An exception handler is reported as Broad Exception if it catches Exception directly.

Reason: Catching broad exceptions may hide real errors and make debugging more difficult.