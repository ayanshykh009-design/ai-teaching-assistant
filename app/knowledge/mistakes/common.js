// Common Student Mistakes in JavaScript

// 1. Using == instead of ===
if (score == "10") { }  // Bad: type coercion
if (score === "10") { } // Good: strict equality

// 2. Forgetting to declare variables with let/const
for (i = 0; i < 10; i++) { }  // Bad: global i
for (let i = 0; i < 10; i++) { } // Good: block-scoped i

// 3. Off-by-one errors in arrays
arr[arr.length]  // Bad: undefined, indices go 0 to length-1
arr[arr.length - 1] // Good: last element

// 4. Misspelling property names
arr.lenght  // Bad: undefined
arr.length  // Good

// 5. Type confusion with mixed-type arrays
["95", 88]  // Bad: string and number mixed

// 6. Not returning from functions
function add(a, b) { a + b }  // Bad: returns undefined
function add(a, b) { return a + b } // Good

// 7. Using var instead of let/const (scope issues)

// 8. Forgetting to handle edge cases (empty arrays, negative numbers)
