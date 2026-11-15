"""Additional language-specific lessons for FelixForge Academy.
Each entry is (title, detailed lesson body, runnable/example code).
"""

TOPICS = {
'python': [
('Branching with if, elif and else', '''LEARNING OBJECTIVE
Choose different actions based on data, and understand truth values and comparison operators.

CORE CONCEPT
A conditional statement lets a program make a decision. Python evaluates the expression after if and treats its result as true or false. If it is true, the indented block runs. Otherwise Python checks the next elif branch, if one exists, and finally runs else when no earlier branch matched. Only the first matching branch runs.

HOW TO BUILD A GOOD CONDITION
Use comparison operators such as ==, !=, <, <=, > and >=. Combine tests with and, or and not. Use == to compare values; a single = assigns a value. Python also has truthy and falsy values: empty strings, empty collections, zero and None are falsy, while most other values are truthy.

READ THE EXAMPLE
The score is checked from highest band to lowest. The order matters: if the broad condition came first, a score of 92 could match it before reaching the A grade branch. The final else handles values below the listed ranges.

COMMON MISTAKES
• Using = instead of == in a comparison.
• Forgetting the colon at the end of if/elif/else lines.
• Using separate if statements when only one branch should run.
• Forgetting to validate that input is numeric before comparing it.

PRACTICE
Ask the user for a temperature and print whether it is below freezing, cool, warm or hot. Test negative values and values exactly on each boundary.''', '''score = 86

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "Needs more practice"

print(f"Score: {score}; grade: {grade}")'''),
('Repeating work with for and while loops', '''LEARNING OBJECTIVE
Repeat instructions without copying the same statements many times, and select the correct loop type.

FOR LOOPS
A for loop visits each item in an iterable such as a list, string, tuple or range. range(stop) produces numbers from zero up to, but not including, stop. range(start, stop, step) gives more control. A for loop is usually best when you know the collection or sequence to process.

WHILE LOOPS
A while loop repeats as long as its condition remains true. It is useful when the number of repetitions depends on an event or user input. Make sure something inside the loop can eventually make the condition false; otherwise the loop may never finish.

CONTROL STATEMENTS
break exits the nearest loop. continue skips the rest of the current iteration and starts the next one. Avoid using these unnecessarily because clear loop conditions are easier to understand.

PRACTICE
Create a multiplication table using a for loop, then write a number-guessing loop that stops when the correct answer is entered.''', '''number = 7

for multiplier in range(1, 6):
    product = number * multiplier
    print(f"{number} x {multiplier} = {product}")

attempts = 0
while attempts < 3:
    print("Practice attempt", attempts + 1)
    attempts += 1'''),
('Writing reusable functions', '''LEARNING OBJECTIVE
Design functions that accept input, perform one clear task and return useful results.

FUNCTION STRUCTURE
Use def followed by a function name, parentheses and a colon. Parameters are names that receive values when the function is called. return sends a result back to the caller and ends that function call. print displays information but does not replace returning a value.

PARAMETERS AND ARGUMENTS
A function can have multiple parameters, default values and keyword arguments. Choose descriptive names and keep each function focused. A function that calculates a value should normally return it; the caller can decide whether to print, save or reuse that result.

SCOPE
Variables created inside a function are local to that function unless returned or otherwise shared. Passing data in and returning data out makes functions easier to test than relying on global variables.

PRACTICE
Write a function that receives a price and tax rate, returns the final price, and test it with several values including zero.''', '''def calculate_total(price, tax_rate=0.075):
    """Return a price after adding the supplied tax rate."""
    if price < 0 or tax_rate < 0:
        raise ValueError("Price and tax rate cannot be negative")
    return price + (price * tax_rate)

bill = calculate_total(1200)
print(f"Total: {bill:.2f}")'''),
('Working with lists, tuples, sets and dictionaries', '''LEARNING OBJECTIVE
Choose a collection based on whether order, mutability, uniqueness or named lookup matters.

LISTS
Lists are ordered and mutable. Use append to add an item, remove to delete a matching item, and indexing to access an item. Indexing starts at zero; negative indexes count from the end. A slice such as items[1:3] returns a portion without changing the original list.

TUPLES AND SETS
Tuples are ordered but immutable, making them useful for fixed groups of values. Sets store unique values and are useful for membership tests and removing duplicates; they do not provide ordinary positional indexing.

DICTIONARIES
Dictionaries map keys to values. Use a meaningful key to retrieve a value, get(key, default) when a key might be absent, and items() to loop through key-value pairs.

PRACTICE
Store student names and scores in a dictionary. Calculate the class average and use a set to display each distinct score only once.''', '''students = {"Ada": 92, "Tunde": 78, "Mina": 92}

for name, score in students.items():
    print(f"{name}: {score}")

average = sum(students.values()) / len(students)
unique_scores = set(students.values())
print("Class average:", round(average, 1))
print("Distinct scores:", sorted(unique_scores))'''),
('Handling errors and validating input', '''LEARNING OBJECTIVE
Anticipate invalid data, handle expected failures and keep error messages useful.

WHY VALIDATION MATTERS
Programs receive data from users, files, networks and other systems. Never assume that input has the type, range or format you expect. Validate at the boundary where data enters your program, then use clear internal assumptions.

EXCEPTIONS
Python raises exceptions when an operation cannot be completed. Use try for code that may fail and except for specific expected exception types. ValueError commonly occurs when converting text to a number; ZeroDivisionError occurs when dividing by zero. Use else for code that should run only when no exception occurred and finally for cleanup that must happen either way.

GOOD PRACTICE
Do not catch every exception without a reason. A broad except can hide programming bugs. Give users a corrective message, while logging technical details privately when appropriate.

PRACTICE
Ask for two numbers, handle non-numeric input and prevent division by zero.''', '''try:
    first = float(input("First number: "))
    second = float(input("Second number: "))
    result = first / second
except ValueError:
    print("Please enter valid numbers.")
except ZeroDivisionError:
    print("The second number must not be zero.")
else:
    print("Result:", result)
finally:
    print("Calculation finished.")'''),
('Organising code into modules', '''LEARNING OBJECTIVE
Split a program into reusable files and understand imports and the main-program guard.

MODULES
A Python file is a module. Moving related functions into a separate file keeps a project organised and allows the same code to be reused. import module gives access through the module name; from module import name imports a selected object. Prefer explicit imports over wildcard imports because they make dependencies easier to see.

PACKAGES
A package groups related modules in a directory. Larger projects often separate application logic, data access, tests and user-interface code into different packages.

THE MAIN GUARD
The condition if __name__ == "__main__" checks whether a file is being run directly. It prevents demonstration or startup code from running automatically when another module imports it.

PRACTICE
Create a file named calculations.py containing an add function, then import and call it from main.py.''', '''# calculations.py
def add(first, second):
    return first + second


# main.py
from calculations import add

if __name__ == "__main__":
    answer = add(14, 9)
    print("Answer:", answer)'''),
('Testing and debugging a Python program', '''LEARNING OBJECTIVE
Find defects systematically and write small tests that protect expected behaviour.

DEBUGGING PROCESS
First reproduce the problem. Read the complete traceback from the bottom upward: the final line usually names the exception, while earlier lines show where it travelled. Inspect the values and types involved. Reduce the problem to the smallest example that still fails, fix the cause, and run the test again.

ASSERTIONS AND UNIT TESTS
An assert statement checks an assumption during development, but it is not a replacement for validating user input. For repeatable tests, use the unittest or pytest framework. Test ordinary values, boundary values and invalid values.

TESTABLE DESIGN
Small functions with clear inputs and outputs are easier to test. Avoid making a test depend on network access, current time or unrelated global state unless the test is specifically about those behaviours.

PRACTICE
Write tests for a function that converts minutes to seconds. Include zero, a normal value and a negative value.''', '''def minutes_to_seconds(minutes):
    if minutes < 0:
        raise ValueError("Minutes cannot be negative")
    return minutes * 60


assert minutes_to_seconds(0) == 0
assert minutes_to_seconds(5) == 300

try:
    minutes_to_seconds(-1)
except ValueError:
    print("Negative input was rejected as expected")'''),
],
'javascript': [
('Making decisions with conditional statements', '''LEARNING OBJECTIVE
Control which JavaScript statements run by evaluating Boolean conditions.

CONDITIONALS
Use if to run a block when a condition is true, else if to test another condition when earlier conditions failed, and else as the final fallback. JavaScript comparisons include === and !== for strict equality, and relational operators such as < and >=. Prefer strict equality because it does not silently convert values of different types.

TRUTHINESS
Conditions can use Boolean values directly or values converted to Boolean. Empty strings, zero, NaN, null, undefined and false are falsy; most other values are truthy. Use explicit comparisons when they make the intention clearer.

TERNARY OPERATOR
The conditional expression condition ? valueA : valueB is useful for choosing between two simple values. Avoid deeply nested ternaries because they become difficult to read.

PRACTICE
Write a function that returns a shipping message based on whether an order total reaches a free-shipping threshold.''', '''const orderTotal = 8500;
const freeShippingLimit = 10000;

if (orderTotal >= freeShippingLimit) {
  console.log("Shipping is free.");
} else {
  const remaining = freeShippingLimit - orderTotal;
  console.log(`Spend ${remaining} more for free shipping.`);
}

const status = orderTotal > 0 ? "Valid order" : "Empty order";
console.log(status);'''),
('Repeating tasks with loops', '''LEARNING OBJECTIVE
Process repeated work using for, while, for...of and array iteration methods.

LOOP CHOICES
A traditional for loop is useful when you need an index or a controlled counter. A while loop repeats while a condition is true. for...of visits values in an iterable such as an array or string. for...in visits enumerable property names and is more commonly used with objects; it is not the preferred way to loop through array values.

ARRAY METHODS
map transforms each item and returns a new array. filter keeps items that pass a test. reduce combines items into one result. These methods are often clearer than manually building a new array, provided the callback remains easy to understand.

PRACTICE
Given an array of prices, create a new array with tax added, filter prices above a chosen amount and calculate the total.''', '''const prices = [1200, 2500, 800, 4300];
const withTax = prices.map(price => price * 1.075);
const expensive = withTax.filter(price => price >= 2000);
const total = withTax.reduce((sum, price) => sum + price, 0);

console.log("Prices with tax:", withTax);
console.log("Higher-priced items:", expensive);
console.log("Total:", total.toFixed(2));'''),
('Creating reusable functions and arrow functions', '''LEARNING OBJECTIVE
Write functions that accept parameters, return values and can be passed to other functions.

FUNCTION DECLARATIONS
A function declaration uses the function keyword and a name. It can be called before its declaration in the same scope because declarations are hoisted. Function expressions assign a function to a variable. Arrow functions use => and are concise for callbacks; they do not create their own this value, arguments object or constructor behaviour.

PARAMETERS AND RETURNS
Parameters receive arguments. A return statement sends a value back and stops that function call. If a function has no return statement, it returns undefined. Default parameters provide a value when an argument is omitted or undefined.

SCOPE
let and const are block-scoped. Avoid accidental global variables. Keep functions focused and pass required data as parameters instead of relying on hidden external state.

PRACTICE
Write a function that receives a list of scores and returns the average, including a safe result for an empty list.''', '''function average(scores) {
  if (scores.length === 0) return null;
  const total = scores.reduce((sum, score) => sum + score, 0);
  return total / scores.length;
}

const result = average([70, 85, 95]);
console.log(result === null ? "No scores yet" : result.toFixed(1));'''),
('Working with arrays, objects, Map and Set', '''LEARNING OBJECTIVE
Represent groups of values and select a data structure that matches the task.

ARRAYS
Arrays are ordered collections. Access an item by index, use push to append, and use methods such as map, filter, find, some and every to process values. Methods such as sort mutate the original array, so copy first when you need to preserve it.

OBJECTS
Objects store named properties. Use dot notation for known property names and bracket notation for dynamic keys. Object.keys, Object.values and Object.entries help inspect an object's contents.

MAP AND SET
Map stores key-value pairs and allows keys of different types. Set stores unique values and is useful for membership checks and removing duplicates. Use the structure that communicates your intent rather than forcing everything into an array.

PRACTICE
Build a small inventory object, update stock, and use a Set to track unique product categories.''', '''const inventory = [
  { name: "Notebook", stock: 12, category: "Stationery" },
  { name: "Pen", stock: 30, category: "Stationery" },
  { name: "Mouse", stock: 5, category: "Electronics" }
];

const lowStock = inventory.filter(item => item.stock < 10);
const categories = new Set(inventory.map(item => item.category));
const stockByName = new Map(inventory.map(item => [item.name, item.stock]));

console.log(lowStock);
console.log([...categories]);
console.log(stockByName.get("Mouse"));'''),
('Handling errors with try, catch and finally', '''LEARNING OBJECTIVE
Handle operations that can fail and provide useful recovery behaviour.

EXCEPTIONS
JavaScript throws an Error when an operation fails or when code deliberately uses throw. Wrap code that may throw in try. A matching catch block receives the error. finally runs whether the try block succeeds or fails and is useful for cleanup.

CUSTOM ERRORS
Throw an Error with a clear message when a function's input violates its contract. Do not expose private implementation details to end users. Validate data before using it, especially when it comes from forms or external services.

ASYNC ERRORS
For promises, use catch or try/catch inside an async function with await. A rejected promise that is not handled can become an unhandled rejection.

PRACTICE
Create a safe number parser that rejects blank text and non-numeric input, then display a friendly message.''', '''function parseQuantity(text) {
  if (text.trim() === "") throw new Error("Quantity is required");
  const value = Number(text);
  if (!Number.isInteger(value) || value < 0) {
    throw new Error("Enter a non-negative whole number");
  }
  return value;
}

try {
  console.log("Quantity:", parseQuantity("12"));
} catch (error) {
  console.log("Input problem:", error.message);
} finally {
  console.log("Validation finished.");
}'''),
('Working with JSON and browser storage', '''LEARNING OBJECTIVE
Convert structured JavaScript data to JSON and understand safe browser-side persistence.

JSON
JSON is a text format for exchanging structured data. JSON.stringify converts supported JavaScript values into JSON text; JSON.parse converts valid JSON text back into JavaScript values. JSON does not represent functions, undefined values or circular object references in the same way as ordinary JavaScript objects.

LOCAL STORAGE
localStorage stores string values for a website origin and keeps them after a tab closes. Store objects by serialising them with JSON.stringify, then parse them when reading. Treat stored data as untrusted and handle malformed JSON. Do not store passwords, session tokens or sensitive personal information in localStorage.

PRACTICE
Save a simple list of completed topics in localStorage and safely handle the case where no saved list exists yet.''', '''const completedTopics = ["variables", "conditions", "loops"];
localStorage.setItem("completedTopics", JSON.stringify(completedTopics));

let savedTopics = [];
try {
  savedTopics = JSON.parse(localStorage.getItem("completedTopics") || "[]");
  if (!Array.isArray(savedTopics)) savedTopics = [];
} catch {
  savedTopics = [];
}

console.log("Completed:", savedTopics.join(", "));'''),
('Testing JavaScript functions', '''LEARNING OBJECTIVE
Use repeatable checks to detect mistakes before code reaches users.

TESTING LEVELS
A unit test checks a small function or module. Integration tests check that components work together. Browser or end-to-end tests exercise a complete user journey. Choose the smallest test level that can reliably detect the defect.

ASSERTIONS
An assertion compares an actual result with an expected result. Test ordinary input, edge cases, empty values and invalid input. A function with deterministic inputs and outputs is usually easier to test than one that directly reads global state or makes network requests.

DEBUGGING
Use browser developer tools: Console shows errors and logs, Sources allows breakpoints and step-through debugging, and Network helps inspect requests. Remove temporary debug logs before release.

PRACTICE
Test a function that calculates a discount, including zero price, no discount and an invalid percentage.''', '''function discountedPrice(price, percent) {
  if (price < 0 || percent < 0 || percent > 100) {
    throw new RangeError("Invalid price or discount");
  }
  return price * (1 - percent / 100);
}

console.assert(discountedPrice(100, 10) === 90, "10% discount");
console.assert(discountedPrice(50, 0) === 50, "No discount");
console.assert(discountedPrice(0, 20) === 0, "Zero price");
console.log("Basic checks finished");'''),
],
'html': [
('Building semantic page structure', '''LEARNING OBJECTIVE
Use HTML elements according to the meaning of their content rather than choosing elements only for their default appearance.

SEMANTIC LANDMARKS
A page can use header for introductory content, nav for major navigation, main for the unique central content, section for a thematic group, article for independently meaningful content, aside for related information and footer for closing information. A page should normally have one main landmark. Use headings in a logical hierarchy so people can understand the page outline.

WHY SEMANTICS MATTER
Browsers, search engines, assistive technologies and other tools can interpret semantic elements more accurately than generic div elements. A heading should describe the section that follows it. Do not choose a heading level just because its default font size looks right; style it with CSS instead.

PRACTICE
Create a small course page with a header, navigation, main lesson article, related-links aside and footer. Check that the heading order makes sense.''', '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Course lesson</title>
</head>
<body>
  <header><h1>FelixForge Academy</h1></header>
  <nav aria-label="Main navigation"><a href="/courses">Courses</a></nav>
  <main>
    <article>
      <h2>HTML structure</h2>
      <p>Learn to organise meaningful page content.</p>
    </article>
  </main>
  <footer><p>Learning resources</p></footer>
</body>
</html>'''),
('Creating accessible forms', '''LEARNING OBJECTIVE
Build forms whose controls have clear labels, useful types and understandable validation.

FORM BASICS
The form element groups controls that submit information. A label should be associated with its control using for and id, or by wrapping the control. Use input types such as email, number, date and password to communicate the expected kind of data and help browsers provide appropriate keyboards and validation.

VALIDATION
required marks a field as mandatory; min, max, minlength, maxlength and pattern add constraints. Browser validation improves usability but does not replace server-side validation. A user can bypass browser checks, so the server must verify every submitted value again.

ACCESSIBILITY
Explain what information is expected. Do not rely on colour alone to indicate errors. Connect help and error text with aria-describedby when needed, and provide clear feedback after submission.

PRACTICE
Build a course registration form with name, email, course selection and a checkbox for terms. Add labels and sensible constraints.''', '''<form action="/register" method="post">
  <label for="student-name">Full name</label>
  <input id="student-name" name="name" autocomplete="name" required>

  <label for="student-email">Email address</label>
  <input id="student-email" name="email" type="email" autocomplete="email" required>

  <label for="course">Choose a course</label>
  <select id="course" name="course" required>
    <option value="">Select one</option>
    <option value="python">Python</option>
    <option value="javascript">JavaScript</option>
  </select>

  <button type="submit">Register</button>
</form>'''),
('Adding images, links and media responsibly', '''LEARNING OBJECTIVE
Use links and media with meaningful alternatives and sensible loading behaviour.

LINKS
The a element creates a hyperlink and its href identifies the destination. Link text should describe the destination or action; avoid vague phrases such as click here when a more descriptive label is possible. Use target="_blank" only when a new tab is genuinely helpful, and add rel="noopener" when appropriate.

IMAGES
The img element uses src for the image resource and alt for a text alternative. If an image conveys information, describe its purpose. If it is purely decorative and adds no information, use an empty alt attribute. Set width and height when possible to reduce layout shifts. Lazy-load below-the-fold images when appropriate.

MEDIA
Audio and video elements can provide controls and fallback text. Captions and transcripts make media more accessible. Do not autoplay sound unexpectedly.

PRACTICE
Create a resource card with a descriptive link, a meaningful image alternative and a video with captions.''', '''<article>
  <h2>Learn page layout</h2>
  <img src="layout-example.png" alt="A diagram showing header, navigation, main content and footer" width="640" height="360" loading="lazy">
  <p>Study the structure of a well-organised page.</p>
  <a href="/courses/html">Open the HTML course</a>
</article>

<video controls width="640" preload="metadata">
  <source src="lesson.mp4" type="video/mp4">
  <track src="lesson-captions.vtt" kind="captions" srclang="en" label="English">
  Your browser does not support this video.
</video>'''),
('Tables and structured information', '''LEARNING OBJECTIVE
Represent genuinely tabular data with accessible table markup.

TABLE STRUCTURE
Use table for data arranged in rows and columns. thead groups headings, tbody groups the main data, and tfoot can group totals. Use th for header cells and td for data cells. The scope attribute helps identify whether a header applies to a row or column.

WHEN NOT TO USE TABLES
Do not use tables to position page sections or create a visual grid. CSS Grid and Flexbox are layout tools; tables are for relationships between data values.

ACCESSIBILITY
Provide a caption that explains the table. Keep headings clear and avoid complex merged cells unless they are necessary. On narrow screens, make sure users can still access the full table, for example by placing it in a labelled horizontal scrolling region.

PRACTICE
Create a course results table with a caption, column headers and three learner rows.''', '''<table>
  <caption>Programming assessment results</caption>
  <thead>
    <tr><th scope="col">Learner</th><th scope="col">Course</th><th scope="col">Score</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">Ada</th><td>Python</td><td>92%</td></tr>
    <tr><th scope="row">Mina</th><td>HTML</td><td>87%</td></tr>
    <tr><th scope="row">Tunde</th><td>CSS</td><td>81%</td></tr>
  </tbody>
</table>'''),
('Using data attributes and accessible interactive controls', '''LEARNING OBJECTIVE
Attach small pieces of custom data to elements and create controls with clear names and states.

DATA ATTRIBUTES
Attributes beginning with data- let authors associate custom information with an element. JavaScript can read them through element.dataset. Data attributes are not a secure storage location; users can inspect and change them, so never trust them for permissions, prices or other authoritative decisions.

BUTTONS AND CONTROLS
Use button for actions and a for navigation. A button should have an accessible name. For a disclosure control, aria-expanded can communicate whether a panel is open, and aria-controls can identify the panel it controls. The attribute must be kept in sync with the actual interface state.

PRACTICE
Create a details button that reveals a lesson summary. Use data attributes to identify the panel, and update aria-expanded when the panel opens or closes.''', '''<button type="button" data-panel="lesson-summary" aria-expanded="false" aria-controls="lesson-summary">
  Show lesson summary
</button>
<section id="lesson-summary" hidden>
  <h2>Summary</h2>
  <p>Semantic HTML gives page content meaning.</p>
</section>

<script>
  const button = document.querySelector('[data-panel]');
  const panel = document.getElementById(button.dataset.panel);
  button.addEventListener('click', () => {
    const opening = panel.hidden;
    panel.hidden = !opening;
    button.setAttribute('aria-expanded', String(opening));
  });
</script>'''),
('Organising HTML documents and validating markup', '''LEARNING OBJECTIVE
Create maintainable HTML documents and use validation to catch structural mistakes.

DOCUMENT FOUNDATION
A modern HTML document begins with doctype, then html with a language attribute. The head contains metadata, the page title and links to stylesheets. The body contains the visible document content. Character encoding should be declared early and the viewport metadata helps mobile browsers size the page correctly.

VALIDATION
Close elements correctly, nest them according to HTML rules and avoid duplicate id values. Some elements have special content models; for example, a button should not contain another interactive button. Use a standards-based HTML validator to identify invalid nesting, missing attributes and structural errors.

MAINTAINABILITY
Use consistent indentation, meaningful ids and classes, and separate presentation into CSS. Comments should explain decisions that are not obvious, rather than repeat what the markup already says.

PRACTICE
Create a complete HTML page with metadata, navigation, a main heading, an article and a footer. Validate it and fix every warning you understand.''', '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="A beginner guide to HTML documents">
  <title>HTML document checklist</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <main>
    <h1>HTML document checklist</h1>
    <p>Use a validator to check your markup.</p>
  </main>
</body>
</html>'''),
],
'css': [
('Understanding the cascade, specificity and inheritance', '''LEARNING OBJECTIVE
Predict which CSS declaration applies when multiple rules target the same element.

THE CASCADE
The browser considers origin, importance, cascade layer, specificity and source order when resolving competing declarations. A later rule does not always win: a more specific selector can outrank a less specific one, and important declarations change the cascade priority. Avoid using !important as a routine fix because it makes future overrides harder.

SPECIFICITY
A practical way to compare selectors is to consider IDs, classes/attributes/pseudo-classes, and element selectors. Inline styles also have special priority. Keep selectors as simple as possible so components remain easy to customise.

INHERITANCE
Some properties, such as color and font-family, are inherited by descendants. Others, such as margin and border, normally are not. Use inherit, initial, unset or revert only when you understand the effect.

PRACTICE
Create two conflicting rules for a paragraph. Predict the result, inspect it in developer tools, then simplify the selectors.''', '''/* Element selector: low specificity */
p { color: #334155; }

/* Class selector: more specific */
.notice { color: #b45309; }

/* ID selector: more specific still */
#urgent-notice { color: #b91c1c; }

/* The paragraph inherits font-family from body */
body { font-family: system-ui, sans-serif; }'''),
('Responsive layouts with Flexbox', '''LEARNING OBJECTIVE
Arrange items in one dimension and allow a layout to adapt to available space.

FLEX CONTAINER
Set display: flex on a parent to create a flex formatting context. flex-direction controls the main axis, justify-content distributes items along that axis, and align-items aligns them on the cross axis. gap creates consistent spacing without adding margins to every child.

FLEX ITEMS
flex-grow controls how items share extra space; flex-shrink controls how they shrink; flex-basis sets the initial main size. The shorthand flex combines these values. flex-wrap allows items to move onto another line when space is limited.

RESPONSIVE THINKING
Start with the content and available space. Use min-width: 0 where long content must be allowed to shrink, and use media queries only when the layout needs a meaningful change.

PRACTICE
Build a row of three course cards that wraps into multiple rows on narrow screens.''', '''.course-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: stretch;
}

.course-card {
  flex: 1 1 15rem;
  min-width: 0;
  padding: 1.25rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.75rem;
}

.course-card h2 { margin-top: 0; }'''),
('Responsive layouts with CSS Grid', '''LEARNING OBJECTIVE
Build two-dimensional layouts with rows and columns that adapt to different screen sizes.

GRID CONTAINER
Set display: grid to create a grid formatting context. grid-template-columns defines columns, grid-template-rows defines rows, and gap sets spacing between tracks. The repeat() function avoids repeating the same track definition. The minmax() function sets a minimum and maximum size.

AUTO-FIT AND AUTO-FILL
repeat(auto-fit, minmax(16rem, 1fr)) creates as many columns as fit and allows tracks to grow. auto-fit collapses empty tracks; auto-fill preserves them. Choose based on the visual result you want.

PLACEMENT
Use grid-column and grid-row to place important items across tracks. Avoid overcomplicating placement for ordinary card grids; a simple responsive repeat pattern is often enough.

PRACTICE
Create a dashboard with a sidebar and main content area, then change it to one column on narrow screens.''', '''.dashboard-layout {
  display: grid;
  grid-template-columns: minmax(12rem, 1fr) 3fr;
  gap: 1.25rem;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
  gap: 1rem;
}

@media (max-width: 700px) {
  .dashboard-layout { grid-template-columns: 1fr; }
}'''),
('Designing typography, spacing and visual hierarchy', '''LEARNING OBJECTIVE
Use type scale, line length and consistent spacing to make interfaces easier to read.

TYPOGRAPHY
Choose readable font families and set a comfortable line-height. Body text often benefits from a line-height around 1.5, while headings may use a tighter value. Limit very long lines because they make it harder to track from one line to the next. Use font-weight and size to create hierarchy rather than relying on colour alone.

SPACING SYSTEM
Choose a small spacing scale and reuse it. CSS custom properties make shared values easier to maintain. Consistency is usually more important than choosing a particular number of pixels.

UNITS
rem scales relative to the root font size and is useful for text and component spacing. em is relative to the current element's font size. Percentages and viewport units are useful for fluid sizing, but avoid forcing content into fixed heights.

PRACTICE
Create a readable article layout with a constrained content width, consistent spacing and clear heading levels.''', ''':root {
  --space-1: 0.5rem;
  --space-2: 1rem;
  --space-3: 1.5rem;
  --text-main: #1e293b;
  --content-width: 68ch;
}

.article {
  max-width: var(--content-width);
  margin-inline: auto;
  padding: var(--space-3);
  color: var(--text-main);
  font-family: system-ui, sans-serif;
  line-height: 1.65;
}

.article h1, .article h2 { line-height: 1.2; }
.article p + p { margin-top: var(--space-2); }'''),
('CSS variables, themes and reusable components', '''LEARNING OBJECTIVE
Define design tokens once and reuse them across components and themes.

CUSTOM PROPERTIES
A custom property begins with two hyphens and is read with var(). Defining variables on :root makes them available throughout the document. A fallback value can be supplied inside var() in case the custom property is missing.

THEMES
A theme can override a set of custom properties on a class or data attribute. Components that use those variables automatically adopt the new values. This is usually cleaner than writing a separate colour rule for every component.

SCOPE
Custom properties follow the cascade and inherit through the element tree. Define them at the narrowest sensible scope when a value is component-specific.

PRACTICE
Create a light theme and a dark theme by changing only a small group of CSS variables.''', ''':root {
  --surface: #ffffff;
  --text: #172033;
  --accent: #2563eb;
}

[data-theme="dark"] {
  --surface: #111827;
  --text: #f8fafc;
  --accent: #93c5fd;
}

.card {
  background: var(--surface);
  color: var(--text);
  border: 1px solid color-mix(in srgb, var(--text) 20%, transparent);
}

.card a { color: var(--accent); }'''),
('Transitions, transforms and motion preferences', '''LEARNING OBJECTIVE
Add restrained interface motion while respecting users who prefer reduced motion.

TRANSITIONS
transition controls how changes between property values animate. Specify the properties you want to animate, a duration and a timing function. Avoid transition: all when only one or two properties need animation because it can animate unexpected changes.

TRANSFORMS
transform can translate, rotate, scale or skew an element without changing the normal document flow. Transforms are useful for subtle hover feedback, but excessive motion can distract or cause discomfort.

ACCESSIBILITY
Use the prefers-reduced-motion media query to reduce or remove non-essential motion for users who have requested less motion in their operating system settings.

PRACTICE
Add a small hover lift to a card, then disable that movement when reduced motion is preferred.''', '''.course-card {
  transition: transform 160ms ease, box-shadow 160ms ease;
}

.course-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.75rem 1.5rem rgb(0 0 0 / 12%);
}

@media (prefers-reduced-motion: reduce) {
  .course-card { transition: none; }
  .course-card:hover { transform: none; }
}'''),
],
'sql': [
('Filtering and sorting query results', '''LEARNING OBJECTIVE
Return only the rows needed and order them in a predictable way.

WHERE
WHERE filters rows using conditions. Combine conditions with AND and OR, and use parentheses to make complex logic clear. Use IS NULL or IS NOT NULL to test missing values; comparisons such as = NULL do not work as intended because NULL represents an unknown or missing value.

ORDER BY
ORDER BY sorts results by one or more columns. ASC is ascending and DESC is descending. If you need stable pagination, sort by a unique column as a final tie-breaker.

LIMIT
LIMIT restricts how many rows are returned in systems that support it. Syntax differs between database engines, so consult the documentation for the database you use.

PRACTICE
Select active learners who scored at least 70, sort from highest score to lowest, and return only the first ten.''', '''SELECT username, score, created_at
FROM assessment_results
WHERE is_active = TRUE
  AND score >= 70
ORDER BY score DESC, created_at ASC
LIMIT 10;'''),
('Combining related tables with JOIN', '''LEARNING OBJECTIVE
Retrieve related information stored in separate relational tables.

WHY JOINS EXIST
Relational databases often separate entities into tables to reduce duplication. A foreign key connects a row in one table to a related row in another. JOIN combines matching rows using a relationship condition.

JOIN TYPES
INNER JOIN returns rows with a match on both sides. LEFT JOIN keeps every row from the left table and supplies NULL for missing right-side matches. RIGHT and FULL joins exist in some database systems, but support differs. Always qualify column names when more than one table has a column with the same name.

AVOID ACCIDENTAL DUPLICATION
A one-to-many relationship can produce multiple result rows for one parent. Understand the relationship cardinality before interpreting totals.

PRACTICE
List each learner with their course title, including learners who have not enrolled in a course.''', '''SELECT
  learners.username,
  courses.title AS course_title
FROM learners
LEFT JOIN enrolments
  ON enrolments.learner_id = learners.id
LEFT JOIN courses
  ON courses.id = enrolments.course_id
ORDER BY learners.username;'''),
('Summarising data with GROUP BY and aggregate functions', '''LEARNING OBJECTIVE
Calculate totals, averages and counts across groups of rows.

AGGREGATES
COUNT counts rows or non-NULL values depending on its argument. SUM adds numeric values, AVG calculates an average, MIN returns the smallest value and MAX returns the largest. COUNT(*) counts rows, including rows where some columns are NULL.

GROUP BY
GROUP BY creates groups that share the same values in selected columns. Aggregate functions calculate a result for each group. Every selected expression that is not aggregated generally needs to be included in GROUP BY, subject to the database's rules.

HAVING
WHERE filters rows before grouping. HAVING filters groups after aggregation. Use WHERE for ordinary row conditions and HAVING for conditions involving aggregate results.

PRACTICE
Calculate the number of assessments and average score for each course, then show only courses with at least five attempts.''', '''SELECT
  course_slug,
  COUNT(*) AS attempt_count,
  ROUND(AVG(score), 1) AS average_score
FROM quiz_results
WHERE total > 0
GROUP BY course_slug
HAVING COUNT(*) >= 5
ORDER BY average_score DESC;'''),
('Using subqueries and common table expressions', '''LEARNING OBJECTIVE
Break complex queries into understandable steps and use one query inside another.

SUBQUERIES
A subquery is a query nested inside another SQL statement. It can appear in a WHERE condition, a FROM clause or a SELECT expression. Use EXISTS when the question is whether at least one related row exists. IN is useful for matching a value against a set of returned values.

COMMON TABLE EXPRESSIONS
A WITH clause defines a named query expression for the statement that follows. A CTE can make a long query easier to read by separating it into logical stages. A CTE is not automatically a permanent table.

CORRELATED QUERIES
A correlated subquery refers to values from the outer query and may be evaluated in relation to each outer row. Understand the data size and query plan when performance matters.

PRACTICE
Find learners whose average score is above the overall average score.''', '''WITH learner_averages AS (
  SELECT user_id, AVG(score) AS average_score
  FROM quiz_results
  WHERE total > 0
  GROUP BY user_id
),
overall_average AS (
  SELECT AVG(score) AS value
  FROM quiz_results
  WHERE total > 0
)
SELECT learner_averages.user_id, learner_averages.average_score
FROM learner_averages
CROSS JOIN overall_average
WHERE learner_averages.average_score > overall_average.value
ORDER BY learner_averages.average_score DESC;'''),
('Changing data safely with INSERT, UPDATE and DELETE', '''LEARNING OBJECTIVE
Add, modify and remove records while protecting data integrity.

DATA MODIFICATION
INSERT adds rows. UPDATE changes values in existing rows. DELETE removes rows. An UPDATE or DELETE without a WHERE clause can affect every row in the table, so inspect the condition carefully before running it.

CONSTRAINTS
Primary keys uniquely identify rows. Foreign keys preserve relationships. NOT NULL, UNIQUE and CHECK constraints prevent invalid states at the database level. Application validation is useful, but database constraints provide an important final layer of protection.

SAFE WORKFLOW
Before a large update, run a SELECT using the same WHERE condition to see which rows will be affected. Use a transaction when a group of changes must succeed or fail together. Back up important data before risky maintenance.

PRACTICE
Insert a sample course, update its description using its primary key, then delete only that sample row.''', '''BEGIN;

INSERT INTO courses (slug, title, is_published)
VALUES ('intro-data', 'Introduction to Data', FALSE);

UPDATE courses
SET title = 'Introduction to Data Analysis'
WHERE slug = 'intro-data';

-- Inspect the row before removing it.
SELECT slug, title FROM courses WHERE slug = 'intro-data';

-- Run only when you intend to remove this sample record.
DELETE FROM courses WHERE slug = 'intro-data';

COMMIT;'''),
('Transactions and database consistency', '''LEARNING OBJECTIVE
Group related database changes so that they remain consistent.

ACID OVERVIEW
Atomicity means a transaction is all-or-nothing. Consistency means constraints remain satisfied. Isolation describes how concurrent transactions interact. Durability means committed changes survive failures according to the database's guarantees.

TRANSACTION COMMANDS
BEGIN starts a transaction in systems that use explicit transaction control. COMMIT makes its changes permanent. ROLLBACK discards uncommitted changes. Exact transaction behaviour and syntax vary by database engine and configuration.

WHEN TO USE TRANSACTIONS
Use a transaction when several writes represent one logical operation, such as transferring funds between two accounts or creating a record and its related rows. Keep transactions reasonably short to reduce locking and contention.

PRACTICE
Create a transaction that inserts a course and its first lesson. Roll it back and confirm that neither record remains.''', '''BEGIN;

INSERT INTO courses (slug, title)
VALUES ('transaction-demo', 'Transaction Demo');

INSERT INTO lessons (course_slug, title)
VALUES ('transaction-demo', 'First lesson');

-- Choose COMMIT to keep both changes, or ROLLBACK to undo both.
ROLLBACK;'''),
('Designing tables, keys and indexes', '''LEARNING OBJECTIVE
Design relational tables that reduce duplication and support common queries.

TABLE DESIGN
Give each table one clear responsibility. Use a primary key to identify a row and foreign keys to represent relationships. Choose data types that match the values stored. Normalisation helps reduce duplicated facts and update anomalies; do not split data into unnecessary tables without understanding the relationships.

INDEXES
An index can speed up searches, joins and sorting when its columns match common query patterns. Indexes also use storage and make inserts, updates and deletes more expensive because the index must be maintained. Add indexes based on measured query needs, not guesswork.

CONSTRAINTS
Use NOT NULL, UNIQUE, CHECK and FOREIGN KEY constraints to express rules that must always hold. Application code should still validate input and give helpful messages.

PRACTICE
Design learners, courses and enrolments tables with primary keys and foreign keys. Decide which columns need indexes based on likely queries.''', '''CREATE TABLE learners (
  id INTEGER PRIMARY KEY,
  username VARCHAR(40) NOT NULL UNIQUE,
  email VARCHAR(254) NOT NULL UNIQUE
);

CREATE TABLE enrolments (
  learner_id INTEGER NOT NULL,
  course_id INTEGER NOT NULL,
  enrolled_at TIMESTAMP NOT NULL,
  PRIMARY KEY (learner_id, course_id),
  FOREIGN KEY (learner_id) REFERENCES learners(id)
);

CREATE INDEX idx_enrolments_course ON enrolments(course_id);'''),
],
}

LANGUAGE_LESSONS = {
'c': [
('Conditions and switch statements','''LEARNING OBJECTIVE
Make decisions using comparisons, logical operators and switch selection.

C evaluates an expression in an if statement as false when it equals zero and true when it is non-zero. Use braces even for short blocks to avoid accidental control-flow errors. else if handles additional conditions. switch is useful when one expression is compared with several constant case labels; remember to use break when you do not want execution to fall through into the next case.

Use == for equality and = for assignment. Combine conditions with &&, || and !. Parentheses improve clarity when combining several tests. Validate values before using them as array indexes or division operands.

PRACTICE
Ask for a menu choice from 1 to 3 and use switch to display the selected action. Handle all other values with default.''','''#include <stdio.h>
int main(void) {
    int choice = 2;
    switch (choice) {
        case 1: puts("View lessons"); break;
        case 2: puts("Take practice"); break;
        case 3: puts("View results"); break;
        default: puts("Unknown option");
    }
    return 0;
}'''),
('Loops and repetition','''LEARNING OBJECTIVE
Repeat statements with for, while and do-while loops.

A for loop groups initialisation, condition and update in one header. A while loop checks its condition before each iteration, so its body may run zero times. A do-while loop checks after its body, so it runs at least once. Make sure loop variables change in a way that eventually makes the condition false.

Use break to exit and continue to skip to the next iteration. Avoid modifying the loop counter in several places because it makes the loop harder to reason about. Be careful with unsigned values: decrementing zero can wrap to a very large value.

PRACTICE
Print a multiplication table and calculate the sum of integers from 1 through 100.''','''#include <stdio.h>
int main(void) {
    int total = 0;
    for (int value = 1; value <= 100; value++) {
        total += value;
    }
    printf("Sum: %d\\n", total);

    int countdown = 3;
    while (countdown > 0) {
        printf("%d\\n", countdown);
        countdown--;
    }
    return 0;
}'''),
('Functions, parameters and return values','''LEARNING OBJECTIVE
Divide a C program into functions with clear responsibilities.

A function declaration (prototype) tells the compiler a function's name, return type and parameter types. The definition contains the body. C passes arguments by value, meaning a function receives a copy. To let a function change a caller's variable, pass its address using a pointer and modify the pointed-to object carefully.

Use void when a function has no return value. Choose parameter and return types that represent the data accurately. Keep functions short enough to understand and test. Avoid relying on global variables when parameters and return values make the relationship clearer.

PRACTICE
Write a function that returns the larger of two integers, then test equal and negative values.''','''#include <stdio.h>

int larger(int first, int second) {
    return first > second ? first : second;
}

int main(void) {
    printf("Larger: %d\\n", larger(-4, 9));
    return 0;
}'''),
('Arrays and strings','''LEARNING OBJECTIVE
Store sequences of values and work safely with C strings.

An array stores elements of one type in contiguous memory. Its valid indexes run from zero to length minus one. C does not automatically check array bounds, so the programmer must track the length and ensure every index is valid. Passing an array to a function does not automatically pass its length; pass the length separately.

A C string is a character array terminated by the null character '\\0'. Reserve space for that terminator. Use standard string functions carefully and avoid unbounded input functions. For formatted input, limit string width or use safer line input and validate the result.

PRACTICE
Calculate the average of a fixed array and print a name stored in a bounded character array.''','''#include <stdio.h>
#include <string.h>

int main(void) {
    int scores[] = {70, 85, 95};
    size_t count = sizeof scores / sizeof scores[0];
    int total = 0;
    for (size_t i = 0; i < count; i++) total += scores[i];
    printf("Average: %.1f\\n", (double) total / count);

    char name[32] = "Ada";
    printf("Name: %s (length %zu)\\n", name, strlen(name));
    return 0;
}'''),
('Pointers and dynamic memory basics','''LEARNING OBJECTIVE
Understand addresses, pointer dereferencing and the responsibilities of dynamic allocation.

A pointer stores an address. The address-of operator & obtains an object's address; the dereference operator * accesses the object at a valid pointer. A pointer must point to a live object or be NULL before it is dereferenced. Invalid, uninitialised or freed pointers cause undefined behaviour.

malloc requests a block of memory and returns NULL if allocation fails. The caller is responsible for eventually releasing successful allocations with free. Do not use a pointer after freeing its memory, and do not free the same allocation twice. Prefer automatic storage for simple local data and allocate dynamically only when the lifetime or size requires it.

PRACTICE
Allocate space for five integers, check for failure, initialise them, print them and free the memory.''','''#include <stdio.h>
#include <stdlib.h>

int main(void) {
    size_t count = 5;
    int *values = malloc(count * sizeof *values);
    if (values == NULL) {
        fputs("Allocation failed\\n", stderr);
        return 1;
    }
    for (size_t i = 0; i < count; i++) values[i] = (int)(i * 10);
    for (size_t i = 0; i < count; i++) printf("%d\\n", values[i]);
    free(values);
    values = NULL;
    return 0;
}'''),
('Header files and separate compilation','''LEARNING OBJECTIVE
Split a C program into source and header files and compile them together.

A header file usually contains declarations that other source files need, such as function prototypes, type definitions and constants. A source file contains function definitions. Include guards prevent a header from being processed more than once in a translation unit. Keep implementation details private when callers do not need them.

Compile each source file into an object file, then link the object files into an executable. Compiler warnings help reveal suspicious conversions and missing declarations. Enable useful warnings during development and fix them rather than ignoring them.

PRACTICE
Move a simple add function into math_utils.c and its prototype into math_utils.h, then compile both files with main.c.''','''#include <stdio.h>

/* In a multi-file project, put this declaration in math_utils.h. */
int add(int left, int right);

/* The definition can live in math_utils.c. */
int add(int left, int right) { return left + right; }

int main(void) {
    printf("%d\\n", add(4, 6));
    return 0;
}
/* Example multi-file build: cc -Wall -Wextra main.c math_utils.c -o app */'''),
('Testing and debugging C programs','''LEARNING OBJECTIVE
Use compiler diagnostics, a debugger and boundary tests to locate defects.

Compile with warnings enabled, for example -Wall -Wextra, and treat warnings as useful information. During development, sanitizers can detect classes of memory and undefined-behaviour errors. A debugger can pause execution at breakpoints and inspect variables and the call stack.

Test normal inputs, empty input, boundary indexes, maximum sizes and invalid values. Check return values from library functions and system calls. A program that compiles successfully can still have logic errors, so run it with representative test cases.

PRACTICE
Write a function that searches an array, then test the first element, last element, missing value and empty array.''','''#include <stdio.h>

int find_value(const int values[], size_t count, int target) {
    for (size_t i = 0; i < count; i++) {
        if (values[i] == target) return (int)i;
    }
    return -1;
}

int main(void) {
    int data[] = {4, 8, 12};
    printf("Index: %d\\n", find_value(data, 3, 12));
    printf("Missing: %d\\n", find_value(data, 3, 99));
    return 0;
}'''),
],
'cpp': [
('Branching and loops in C++','''LEARNING OBJECTIVE
Choose control-flow statements that express decisions and repetition clearly.

C++ supports if, else if, else and switch for decisions, along with for, range-based for, while and do-while loops. Use braces consistently. A range-based for loop is especially useful when processing every item in a container. Use const references when you want to inspect larger objects without copying them.

A loop should have a clear stopping condition. Be careful when mixing signed and unsigned integer types in comparisons. Use break and continue sparingly and keep the loop's intent visible.

PRACTICE
Loop through a vector of scores, count how many pass a threshold and print the count.''','''#include <iostream>
#include <vector>
int main() {
    const std::vector<int> scores{55, 72, 91, 68};
    int passes = 0;
    for (const int score : scores) {
        if (score >= 70) ++passes;
    }
    std::cout << "Passes: " << passes << '\\n';
}'''),
('Functions, references and const correctness','''LEARNING OBJECTIVE
Write reusable functions and choose when to pass values, references or pointers.

Passing by value creates a copy, which is simple for small types such as int. Passing by const reference avoids copying a larger object while promising not to modify it. A non-const reference allows a function to modify the caller's object. Use pointers when a value may be absent or when pointer semantics are required.

A function's return type describes the result. Prefer returning a value for ordinary calculations. Use overloads only when the same conceptual operation naturally supports different parameter types. const communicates intent and prevents accidental changes.

PRACTICE
Write a function that calculates the average of a vector passed by const reference and handles an empty vector.''','''#include <iostream>
#include <vector>
#include <optional>

std::optional<double> average(const std::vector<int>& values) {
    if (values.empty()) return std::nullopt;
    long total = 0;
    for (int value : values) total += value;
    return static_cast<double>(total) / values.size();
}

int main() {
    const std::vector<int> scores{70, 80, 90};
    if (auto result = average(scores)) std::cout << *result << '\\n';
}'''),
('Classes, objects and encapsulation','''LEARNING OBJECTIVE
Model data and behaviour together while protecting an object's valid state.

A class defines a type. An object is an instance of that type. public members form the interface; private members hide implementation details. Constructors initialise objects, and member functions define behaviour. Encapsulation means callers use the public interface rather than directly changing internal fields.

Keep invariants inside the class. If a balance cannot be negative, the class should reject operations that would violate that rule. Use const member functions when they do not modify the object's observable state.

PRACTICE
Create a BankAccount class with a private balance, a deposit method and a balance-reading method. Reject negative deposits.''','''#include <iostream>

class BankAccount {
private:
    double balance{0};
public:
    bool deposit(double amount) {
        if (amount <= 0) return false;
        balance += amount;
        return true;
    }
    double get_balance() const { return balance; }
};

int main() {
    BankAccount account;
    account.deposit(2500);
    std::cout << account.get_balance() << '\\n';
}'''),
('Vectors, maps and sets from the standard library','''LEARNING OBJECTIVE
Use standard containers instead of manually managing common data structures.

std::vector is a dynamic array with indexed access and efficient append at the end. std::map stores ordered key-value pairs; std::unordered_map provides hash-based lookup without sorted key order. std::set stores unique sorted values; std::unordered_set stores unique values with hash-based lookup. Select a container based on ordering, lookup and insertion needs.

Prefer standard containers because they manage memory and expose well-tested operations. Use iterators or range-based loops to visit items. Understand that inserting into some containers may invalidate iterators or references.

PRACTICE
Count how many times each word occurs using unordered_map, then display the counts.''','''#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    const std::vector<std::string> words{"code", "learn", "code"};
    std::unordered_map<std::string, int> counts;
    for (const auto& word : words) ++counts[word];
    for (const auto& [word, count] : counts)
        std::cout << word << ": " << count << '\\n';
}'''),
('Exceptions and resource safety','''LEARNING OBJECTIVE
Report exceptional conditions and manage resources safely.

C++ exceptions use throw to signal an exceptional condition and try/catch to handle it. Catch exceptions by const reference when possible to avoid copying and slicing. Do not use exceptions for ordinary control flow. A function should document the kinds of failure callers may need to handle.

RESOURCE MANAGEMENT
Prefer RAII: acquire a resource in an object's constructor and release it in its destructor. Standard library containers and smart pointers manage many resources automatically. unique_ptr expresses exclusive ownership; shared_ptr expresses shared ownership when shared lifetime is genuinely needed. Avoid raw owning pointers in ordinary application code.

PRACTICE
Write a function that validates a percentage and throws invalid_argument when the value is outside 0 to 100.''','''#include <iostream>
#include <stdexcept>

int main() {
    auto validate_percentage = [](int value) {
        if (value < 0 || value > 100)
            throw std::invalid_argument("Percentage must be 0 to 100");
        return value;
    };
    try {
        std::cout << validate_percentage(85) << '\\n';
    } catch (const std::invalid_argument& error) {
        std::cerr << error.what() << '\\n';
    }
}'''),
('Separating code into headers and source files','''LEARNING OBJECTIVE
Organise a C++ project into declarations, implementations and a build process.

A header normally declares a class or function that other files need. A source file contains the definitions. Use #pragma once or traditional include guards to prevent duplicate inclusion. Keep implementation details out of headers when they do not need to be visible to callers.

A project may have several translation units that are compiled separately and linked together. A build system such as CMake can manage targets and dependencies as the project grows. Avoid defining non-inline global objects in headers because multiple source files may create duplicate definitions.

PRACTICE
Declare a calculator function in calculator.hpp, define it in calculator.cpp and call it from main.cpp.''','''#include <iostream>

// In a multi-file project, put this declaration in calculator.hpp.
int multiply(int left, int right);

// Put the definition in calculator.cpp in a real multi-file project.
int multiply(int left, int right) { return left * right; }

int main() {
    std::cout << multiply(4, 6) << '\\n';
}
// Build example: c++ -std=c++17 -Wall -Wextra main.cpp calculator.cpp -o calculator'''),
('Testing and debugging C++','''LEARNING OBJECTIVE
Use compiler warnings, a debugger and tests to improve reliability.

Compile with warnings enabled and choose a language standard explicitly. Use a debugger to inspect the call stack and variables. Sanitizers can help detect memory errors and undefined behaviour during development. A unit test should check one behaviour and include ordinary, boundary and invalid inputs.

Use assertions for development invariants, not for validating untrusted user input. Separate business logic from input/output so functions can be tested without interactive input.

PRACTICE
Test a function that finds the largest value in a vector. Include empty, one-element and repeated-maximum cases.''','''#include <cassert>
#include <vector>
#include <optional>

std::optional<int> largest(const std::vector<int>& values) {
    if (values.empty()) return std::nullopt;
    int result = values.front();
    for (int value : values) if (value > result) result = value;
    return result;
}

int main() {
    assert(largest({2, 9, 4}) == 9);
    assert(largest({}) == std::nullopt);
}'''),
],
'java': [
('Conditions and loops in Java','''LEARNING OBJECTIVE
Control program flow with if, switch and Java loop statements.

Use if/else for Boolean decisions and switch when selecting among several cases. Modern Java supports switch expressions in current language versions, but traditional switch statements are still common. Use for when the number of iterations is controlled, enhanced for to visit each item in an array or collection, and while when repetition depends on a condition.

Java conditions must evaluate to boolean. Unlike some languages, Java does not treat numbers as true or false. Use == for primitive values, but use equals for comparing the contents of most objects such as String. Make sure loops make progress toward their stopping condition.

PRACTICE
Count passing scores in an array and display a message based on the count.''','''public class Main {
    public static void main(String[] args) {
        int[] scores = {55, 72, 91, 68};
        int passes = 0;
        for (int score : scores) {
            if (score >= 70) passes++;
        }
        System.out.println("Passes: " + passes);
    }
}'''),
('Methods, parameters and return values','''LEARNING OBJECTIVE
Create methods that perform one task and return a useful result.

A method belongs to a class and has a return type, name and parameter list. void means it does not return a value. Java passes arguments by value; for object references, the copied value is a reference to the same object, which is why a method can modify an object's state but cannot replace the caller's reference variable itself.

Use static for behaviour that does not depend on a particular object's state. Use instance methods when the operation belongs to an object. Give methods descriptive names and avoid long parameter lists that make calls difficult to understand.

PRACTICE
Write a static method that calculates a tax-inclusive price and test it with several values.''','''public class Main {
    static double totalWithTax(double price, double rate) {
        if (price < 0 || rate < 0) throw new IllegalArgumentException("Invalid input");
        return price * (1 + rate);
    }

    public static void main(String[] args) {
        System.out.printf("Total: %.2f%n", totalWithTax(1200, 0.075));
    }
}'''),
('Classes, objects and constructors','''LEARNING OBJECTIVE
Represent real program concepts with classes and objects.

A class defines fields and methods. An object is created from a class. A constructor runs when an object is created and is used to establish a valid initial state. Encapsulation keeps fields private and exposes methods that enforce rules. Use this to refer to the current object when needed.

Prefer immutable fields when values should not change after construction. Use getters only when callers need to read a value; avoid generating setters for every field automatically if they would allow invalid states.

PRACTICE
Create a Course class with a title and capacity. Validate the title in the constructor and provide a method to check whether a seat remains.''','''class Course {
    private final String title;
    private final int capacity;
    private int enrolled;

    Course(String title, int capacity) {
        if (title == null || title.isBlank() || capacity < 1)
            throw new IllegalArgumentException("Invalid course details");
        this.title = title;
        this.capacity = capacity;
    }

    boolean hasSpace() { return enrolled < capacity; }
    String getTitle() { return title; }
}

public class Main {
    public static void main(String[] args) {
        Course course = new Course("Java", 30);
        System.out.println(course.getTitle() + ": " + course.hasSpace());
    }
}'''),
('Collections: List, Set and Map','''LEARNING OBJECTIVE
Choose Java collection types that match the data you need to store.

List preserves element order and allows duplicates. Set stores unique elements. Map associates keys with values. ArrayList is a common resizable list implementation; HashSet and HashMap provide hash-based lookup, while sorted variants preserve ordering. Use generics such as List<String> so the compiler can check element types.

Use enhanced for loops or collection methods to process items. Do not modify a collection in an unsafe way while iterating over it. Choose immutable collection views when callers should not be able to change the collection.

PRACTICE
Count the frequency of words using a Map and use a Set to display unique words.''','''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> words = List.of("code", "learn", "code");
        Map<String, Integer> counts = new HashMap<>();
        for (String word : words) {
            counts.put(word, counts.getOrDefault(word, 0) + 1);
        }
        Set<String> uniqueWords = new HashSet<>(words);
        System.out.println(counts);
        System.out.println(uniqueWords);
    }
}'''),
('Exceptions and input validation','''LEARNING OBJECTIVE
Handle invalid operations and communicate failures through Java exceptions.

Java has checked and unchecked exceptions. Checked exceptions must be caught or declared in a method signature. RuntimeException and its subclasses are unchecked. Use try/catch for failures you can handle, and try-with-resources for objects that should be closed automatically, such as streams.

Validate method arguments early and throw an appropriate exception when a caller violates the method's contract. Do not catch Exception just to hide a failure. Include useful context in error messages without revealing secrets.

PRACTICE
Parse a whole number from text, handle NumberFormatException and reject negative values.''','''public class Main {
    static int parseQuantity(String text) {
        int value = Integer.parseInt(text);
        if (value < 0) throw new IllegalArgumentException("Quantity cannot be negative");
        return value;
    }

    public static void main(String[] args) {
        try {
            System.out.println(parseQuantity("12"));
        } catch (IllegalArgumentException error) {
            System.out.println("Please enter a valid non-negative whole number.");
        }
    }
}'''),
('Packages, imports and project structure','''LEARNING OBJECTIVE
Organise Java classes into packages and understand the role of imports.

A package groups related classes and helps avoid naming conflicts. The package declaration appears at the beginning of a source file. import allows a class to be referenced by its simple name rather than its fully qualified name. Organise source files to match the package structure.

Keep classes cohesive and use access modifiers deliberately. public makes a type or member accessible wherever its containing type is accessible; private restricts access to the declaring class; package-private is the default when no access modifier is written. Avoid making every field public.

PRACTICE
Create a package named academy.math with a Calculator class, then import it from a Main class in another package.''','''package academy.math;

// In a real project, place Calculator in Calculator.java and import
// academy.math.Calculator from a class in another package.
class Calculator {
    int add(int a, int b) { return a + b; }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(new Calculator().add(4, 6));
    }
}'''),
('Testing Java methods','''LEARNING OBJECTIVE
Write repeatable tests and use debugging tools to understand failures.

A unit test checks one unit of behaviour with controlled inputs. JUnit is a widely used Java testing framework. A test should arrange its inputs, act by calling the method and assert the expected result. Include edge cases such as empty collections, zero and invalid arguments.

Use the IDE debugger to set breakpoints, step through code and inspect variables. Keep logic separate from console input and output so it can be tested without simulating an entire user session.

PRACTICE
Write unit tests for a method that converts minutes into seconds, including zero and invalid negative input.''','''public class Main {
    static int toSeconds(int minutes) {
        if (minutes < 0) throw new IllegalArgumentException("Negative minutes");
        return minutes * 60;
    }

    static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }

    public static void main(String[] args) {
        check(toSeconds(5) == 300, "Five minutes should be 300 seconds");
        check(toSeconds(0) == 0, "Zero should remain zero");
        try {
            toSeconds(-1);
            throw new AssertionError("Negative input should fail");
        } catch (IllegalArgumentException expected) {
            System.out.println("All checks passed");
        }
    }
}
// JUnit 5 is a common framework for larger Java test suites.'''),
],
'csharp': [
('Decisions and loops in C#','''LEARNING OBJECTIVE
Control execution using if, switch, for, foreach and while.

C# conditions require a bool expression. Use if/else for decisions and switch for matching a value against several cases. A for loop is useful when you need a counter; foreach visits each item in a collection and is usually clearer when you do not need an index. while repeats as long as its condition is true.

Use break to leave a loop and continue to skip to the next iteration. Prefer braces consistently, even for a one-line body. Make loop termination obvious and avoid changing the same counter in several places.

PRACTICE
Count the number of passing scores in an array using foreach.''','''using System;

class Program {
    static void Main() {
        int[] scores = { 55, 72, 91, 68 };
        int passes = 0;
        foreach (int score in scores) {
            if (score >= 70) passes++;
        }
        Console.WriteLine($"Passes: {passes}");
    }
}'''),
('Methods, parameters and optional arguments','''LEARNING OBJECTIVE
Create reusable methods and understand how values are passed.

A method declares a return type, name and parameter list. Use void when there is no result. C# passes ordinary parameters by value; ref and out allow a method to work with a caller variable by reference, but should be used only when that behaviour improves the design. Optional parameters provide default values.

Use descriptive method names and keep methods focused. Prefer returning a result over changing many unrelated variables. Static methods do not require an instance; instance methods can use the state of the object they belong to.

PRACTICE
Write a method that calculates a total after tax, using an optional tax-rate parameter.''','''using System;

class Program {
    static decimal Total(decimal price, decimal taxRate = 0.075m) {
        if (price < 0 || taxRate < 0) throw new ArgumentOutOfRangeException();
        return price * (1 + taxRate);
    }

    static void Main() {
        Console.WriteLine(Total(1200).ToString("F2"));
    }
}'''),
('Classes, properties and encapsulation','''LEARNING OBJECTIVE
Create classes that protect their data and expose clear public behaviour.

A class defines a reference type. Properties provide controlled access to data and can validate values in setters or constructors. Constructors establish the initial state. Use private fields when a value should not be changed directly by outside code.

Encapsulation protects invariants. If an account balance must never become negative, methods should enforce that rule. Prefer auto-properties for simple data when no additional logic is required, but do not expose unrestricted setters for values that need protection.

PRACTICE
Create a Course class with a title and a capacity, and reject invalid values in its constructor.''','''using System;

class Course {
    public string Title { get; }
    public int Capacity { get; }
    public Course(string title, int capacity) {
        if (string.IsNullOrWhiteSpace(title) || capacity < 1)
            throw new ArgumentException("Invalid course details");
        Title = title;
        Capacity = capacity;
    }
}

class Program {
    static void Main() => Console.WriteLine(new Course("Python", 30).Title);
}'''),
('Collections and LINQ','''LEARNING OBJECTIVE
Store groups of values and query them with collection methods and LINQ.

List<T> is a resizable ordered collection. HashSet<T> stores unique values. Dictionary<TKey,TValue> maps keys to values. Use generic types so the compiler can check which values belong in a collection.

LINQ provides query operations such as Where, Select, OrderBy, Any, Count and Sum. Many LINQ operations are deferred: the query runs when it is enumerated. Materialise a query with ToList when you need a snapshot or repeated access.

PRACTICE
Filter a list of scores to passing values, order them and calculate their average.''','''using System;
using System.Linq;
using System.Collections.Generic;

class Program {
    static void Main() {
        var scores = new List<int> { 55, 72, 91, 68 };
        var passes = scores.Where(score => score >= 70).OrderByDescending(score => score).ToList();
        Console.WriteLine(string.Join(", ", passes));
        Console.WriteLine(passes.Average());
    }
}'''),
('Exceptions and safe resource handling','''LEARNING OBJECTIVE
Handle exceptional situations and release resources reliably.

Use try/catch to handle exceptions you can meaningfully recover from. finally runs whether an exception occurs or not. Use using declarations or using statements for objects that implement IDisposable, such as file streams, so resources are disposed even when an exception occurs.

Validate input and throw ArgumentException or ArgumentOutOfRangeException when method arguments violate the contract. Do not use exceptions for routine decisions that can be expressed with ordinary conditions. Avoid exposing stack traces or private data in messages shown to users.

PRACTICE
Read a text file with a using statement and handle the case where the file does not exist.''','''using System;
using System.IO;

class Program {
    static void Main() {
        try {
            using var reader = new StreamReader("notes.txt");
            Console.WriteLine(reader.ReadToEnd());
        } catch (FileNotFoundException) {
            Console.WriteLine("The notes file was not found.");
        } catch (IOException) {
            Console.WriteLine("The file could not be read.");
        }
    }
}'''),
('Namespaces and reusable project structure','''LEARNING OBJECTIVE
Organise related classes and avoid naming conflicts with namespaces.

A namespace groups types under a logical name. Use using directives to make types easier to reference. Split a project into files based on responsibility and use access modifiers to control the public API. A class library project can expose reusable code to other applications.

Keep names consistent and avoid placing unrelated types into one large file. For larger applications, organise folders and namespaces around features or layers that have clear responsibilities.

PRACTICE
Create a namespace called Academy.Math with a Calculator class and use it from the main application.''','''// Calculator.cs
namespace Academy.Math;

public class Calculator {
    public int Add(int first, int second) => first + second;
}

// In another file:
// using Academy.Math;
// var calculator = new Calculator();
// Console.WriteLine(calculator.Add(4, 6));'''),
('Testing C# code with unit tests','''LEARNING OBJECTIVE
Test methods with predictable inputs and assertions.

Unit tests verify small behaviours independently. xUnit, NUnit and MSTest are common .NET testing frameworks. A test should arrange the input, act by calling the method and assert the result. Include boundary cases and expected exceptions.

Keep business logic separate from console input, file access and network requests so it can be tested easily. Use the debugger to inspect state and step through execution when a test fails.

PRACTICE
Write tests for a method that calculates a discount and rejects percentages outside the range 0 to 100.''','''// Example using xUnit
using Xunit;

public class DiscountTests {
    static decimal PriceAfterDiscount(decimal price, decimal percent) {
        if (percent < 0 || percent > 100) throw new ArgumentOutOfRangeException();
        return price * (1 - percent / 100);
    }

    [Fact]
    public void AppliesTenPercentDiscount() {
        Assert.Equal(90m, PriceAfterDiscount(100m, 10m));
    }
}'''),
],
'php': [
('Decisions and loops in PHP','''LEARNING OBJECTIVE
Choose branches and loops to control a PHP program.

Use if, elseif and else to select a block. PHP also has switch and match expressions for multiple alternatives. Use === for strict comparisons when type conversion is not intended. for is useful for counter-controlled repetition, foreach for arrays and iterable objects, and while for condition-controlled repetition.

The foreach loop can access values or key-value pairs. Avoid changing a collection unexpectedly while iterating. Validate request data before using it and do not assume that form values have the type you expect.

PRACTICE
Loop through an associative array of learners and display only those whose scores meet a threshold.''','''<?php
$learners = ["Ada" => 92, "Tunde" => 68, "Mina" => 81];
foreach ($learners as $name => $score) {
    if ($score >= 70) {
        echo htmlspecialchars($name) . ": " . $score . "<br>";
    }
}
?>'''),
('Functions and type declarations','''LEARNING OBJECTIVE
Create reusable PHP functions with parameters, return values and clear type expectations.

A function is declared with function, a name and parameters. Scalar type declarations and return types document the expected data and can help catch mistakes. PHP supports nullable and union types in modern versions. Use strict_types deliberately when you want stricter scalar type handling for a file.

Return a result when the caller needs to use it elsewhere. Avoid functions that both calculate values and unexpectedly print output. Keep functions focused and use descriptive parameter names.

PRACTICE
Write a function that calculates a total price from a base amount and tax rate, and rejects negative values.''','''<?php
declare(strict_types=1);

function totalWithTax(float $price, float $rate = 0.075): float {
    if ($price < 0 || $rate < 0) {
        throw new InvalidArgumentException("Values cannot be negative");
    }
    return $price * (1 + $rate);
}

echo number_format(totalWithTax(1200), 2);
?>'''),
('Arrays and associative arrays','''LEARNING OBJECTIVE
Store ordered values and key-value data using PHP arrays.

PHP arrays are ordered maps: they can behave like indexed lists or associative maps. Use [] to create an array, append with [], and access values with their keys. foreach is the usual way to visit elements. Array functions such as array_map, array_filter and array_reduce can transform or summarise values.

Remember that arrays may contain mixed types, but consistent data shapes make programs easier to understand. Use null coalescing (??) when a key may be absent, and validate values before calculations.

PRACTICE
Store product prices in an associative array, filter those above a threshold and calculate their sum.''','''<?php
$prices = ["Notebook" => 1200, "Mouse" => 8500, "Pen" => 300];
$expensive = array_filter($prices, fn($price) => $price >= 1000);
$total = array_sum($prices);

foreach ($expensive as $name => $price) {
    echo htmlspecialchars($name) . ": " . $price . "<br>";
}
echo "Total: " . $total;
?>'''),
('Handling errors and exceptions','''LEARNING OBJECTIVE
Validate input and handle failures with exceptions and useful messages.

PHP supports exceptions with try, catch and finally. Throw an exception when a function cannot satisfy its contract. Catch only errors that the current layer can handle. For user-submitted data, validate expected formats and ranges before using the values.

Do not display detailed stack traces or database errors to public visitors. Log technical details on the server and show a brief, helpful message to the user. In production, configure error display off and error logging on.

PRACTICE
Validate a quantity submitted as text, reject negative or non-integer values and display a safe message.''','''<?php
function parseQuantity(string $input): int {
    $value = filter_var($input, FILTER_VALIDATE_INT);
    if ($value === false || $value < 0) {
        throw new InvalidArgumentException("Enter a non-negative whole number");
    }
    return $value;
}

try {
    echo parseQuantity("12");
} catch (InvalidArgumentException $error) {
    echo htmlspecialchars($error->getMessage());
}
?>'''),
('Working with forms and safe output','''LEARNING OBJECTIVE
Receive form data safely and display it without treating user input as trusted HTML.

A PHP page can read submitted values from $_POST or $_GET. Check that required keys exist and validate the data type and range. Never rely only on browser-side validation. Escape output with htmlspecialchars when inserting untrusted text into HTML. This helps prevent a browser from interpreting user input as markup or script.

For database writes, use prepared statements rather than concatenating user input into SQL. Keep secrets and database credentials outside publicly served files.

PRACTICE
Create a form that receives a learner's name and displays a safely escaped greeting.''','''<?php
$name = "";
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $name = trim((string)($_POST["name"] ?? ""));
}
?>
<form method="post">
  <label>Name <input name="name" maxlength="60" required></label>
  <button type="submit">Send</button>
</form>
<?php if ($name !== ""): ?>
  <p>Hello, <?= htmlspecialchars($name, ENT_QUOTES, "UTF-8") ?>!</p>
<?php endif; ?>'''),
('Organising PHP with files, includes and namespaces','''LEARNING OBJECTIVE
Separate reusable PHP code and avoid naming collisions.

include and require load another PHP file. require is appropriate when the application cannot continue without the file; include emits a warning if the file is missing. The _once forms prevent the same file from being included repeatedly. Use them carefully and keep file paths predictable.

Namespaces group classes and functions. Composer provides dependency management and autoloading for modern PHP projects. Keep configuration and secrets outside the public web root, and do not commit local secret files to source control.

PRACTICE
Create a namespaced PriceCalculator class in a separate file and load it using a simple require statement or Composer autoloading.''','''<?php
// src/Academy/PriceCalculator.php
namespace Academy;

class PriceCalculator {
    public function total(float $price, float $rate): float {
        return $price * (1 + $rate);
    }
}

// In a simple script, after loading the file:
// require_once __DIR__ . "/src/Academy/PriceCalculator.php";
// $calculator = new \\Academy\\PriceCalculator();
// echo $calculator->total(100, 0.075);
?>'''),
('Testing PHP functions','''LEARNING OBJECTIVE
Check PHP behaviour with repeatable tests and use errors to guide debugging.

Unit tests check a small function with controlled inputs. PHPUnit is a common testing framework. Include normal values, boundaries, empty input and invalid data. Keep pure calculation logic separate from request handling so it can be tested without a web server.

Use error logs and a debugger when needed. Avoid turning off all error reporting during development; configure errors to be logged rather than displayed to visitors in production.

PRACTICE
Write a test for a percentage calculator that checks ordinary input and rejects values outside its allowed range.''','''<?php
function percentage(float $part, float $whole): float {
    if ($whole <= 0) throw new InvalidArgumentException("Whole must be positive");
    return ($part / $whole) * 100;
}

assert(percentage(25, 100) === 25.0);
assert(percentage(5, 10) === 50.0);
?>'''),
],
'typescript': [
('Conditions, loops and narrowing types','''LEARNING OBJECTIVE
Control program flow while allowing TypeScript to narrow types safely.

TypeScript uses JavaScript control-flow statements, but the compiler also analyses conditions to narrow union types. For example, checking typeof value === "string" lets the compiler treat value as a string inside that branch. This is called control-flow narrowing.

Use strict equality and explicit checks. A for...of loop visits values in an iterable. A for...in loop visits object keys. Type guards, discriminated unions and exhaustive switch statements can make complex decisions safer.

PRACTICE
Write a function that accepts a string or number and returns a readable description after checking the type.''','''function describe(value: string | number): string {
  if (typeof value === "string") {
    return `Text with ${value.length} characters`;
  }
  return `Number: ${value.toFixed(2)}`;
}

for (const item of ["hello", 12.5, "TypeScript"]) {
  console.log(describe(item));
}'''),
('Functions, optional parameters and return types','''LEARNING OBJECTIVE
Define functions whose inputs and outputs are checked by the TypeScript compiler.

Annotate parameters and return values when it improves clarity. TypeScript can infer many local types, so do not add annotations that simply repeat obvious information. Optional parameters use ? and default parameters provide a value when an argument is omitted. A function returning nothing useful can use void.

Use union types when a function genuinely accepts different kinds of values. Prefer overloads only when they provide a clearer public contract. Avoid any because it disables many checks; use unknown and narrow it when the type is not yet known.

PRACTICE
Create a function that formats a learner's name and optional course title.''','''function learnerLabel(name: string, course?: string): string {
  const cleanName = name.trim();
  if (!cleanName) throw new Error("Name is required");
  return course ? `${cleanName} — ${course}` : cleanName;
}

console.log(learnerLabel("Ada", "Python"));
console.log(learnerLabel("Mina"));'''),
('Arrays, tuples, records and typed objects','''LEARNING OBJECTIVE
Describe the shape of structured data and use collection types accurately.

TypeScript arrays use T[] or Array<T>. Tuples describe a fixed sequence of values with known positions. Interfaces and type aliases describe object shapes. Record<K,V> describes an object with keys of type K and values of type V. readonly prevents certain mutations through that reference, though it does not deeply freeze nested objects at runtime.

Use optional properties when a field may be absent and union types when a field has several valid forms. Prefer explicit data models over broad object types.

PRACTICE
Create a typed list of course objects and filter those marked as published.''','''type Course = {
  id: number;
  title: string;
  published: boolean;
  tags: readonly string[];
};

const courses: Course[] = [
  { id: 1, title: "Python", published: true, tags: ["beginner"] },
  { id: 2, title: "Rust", published: false, tags: ["systems"] }
];

const visible = courses.filter(course => course.published);
console.log(visible.map(course => course.title));'''),
('Interfaces, classes and access modifiers','''LEARNING OBJECTIVE
Model contracts and object behaviour with interfaces and classes.

An interface describes the shape a value must have. A class can implement one or more interfaces. Access modifiers such as public, private and protected control how class members can be accessed by TypeScript code. TypeScript's private checking is primarily compile-time; JavaScript private fields written with # provide runtime privacy.

Prefer composition when one object can use another object without inheriting its entire implementation. Keep constructors and methods focused, and use readonly for properties that should not be reassigned after initialisation.

PRACTICE
Define a ProgressTracker interface and implement it with a class that records completed lesson IDs.''','''interface ProgressTracker {
  complete(lessonId: number): void;
  isComplete(lessonId: number): boolean;
}

class MemoryProgress implements ProgressTracker {
  private completed = new Set<number>();
  complete(lessonId: number): void { this.completed.add(lessonId); }
  isComplete(lessonId: number): boolean { return this.completed.has(lessonId); }
}

const tracker = new MemoryProgress();
tracker.complete(12);
console.log(tracker.isComplete(12));'''),
('Generics for reusable typed code','''LEARNING OBJECTIVE
Write functions and types that work with different data types without losing type information.

A generic type parameter represents a type chosen when the function or class is used. For example, identity<T>(value: T): T returns the same kind of value it receives. Constraints such as T extends { id: number } restrict which types are accepted and allow the function to safely access the required property.

Generics are useful for reusable containers, API response wrappers and utility functions. Avoid adding generics when one concrete type is clearer.

PRACTICE
Write a function that returns the first item in an array or undefined when the array is empty.''','''function first<T>(items: readonly T[]): T | undefined {
  return items[0];
}

const firstName = first(["Ada", "Mina"]);
const firstScore = first<number>([90, 82]);
console.log(firstName, firstScore);'''),
('Modules, imports and asynchronous promises','''LEARNING OBJECTIVE
Organise TypeScript files and understand asynchronous operations.

Use export to expose a value from a module and import to use it elsewhere. Modules create file-level scope and make dependencies explicit. Keep modules focused on one responsibility and avoid circular imports where possible.

A Promise represents a result that may be available later. async functions always return a promise; await pauses that function until the promise settles. Use try/catch around awaited operations to handle failures. Add explicit types to public API boundaries when inference is not sufficient.

PRACTICE
Create a module exporting a function that loads course data asynchronously and handle a rejected promise.''','''// courseService.ts
export type Course = { id: number; title: string };

export async function loadCourse(id: number): Promise<Course> {
  const response = await fetch(`/api/courses/${id}`);
  if (!response.ok) throw new Error("Course could not be loaded");
  return response.json() as Promise<Course>;
}

// In another module:
// import { loadCourse } from "./courseService";
// try { console.log(await loadCourse(1)); } catch (error) { console.error(error); }'''),
('Testing TypeScript code','''LEARNING OBJECTIVE
Test typed functions and understand the difference between compile-time checks and runtime validation.

TypeScript catches many mistakes before code runs, but types are removed during compilation. Data received from a network, form or storage is not automatically validated at runtime. Treat external data as unknown, check its shape and only then use it as a trusted type.

Unit tests check behaviour; tools such as Vitest or Jest can run TypeScript tests through suitable configuration. Include normal values, boundaries and malformed external data. Type checking and runtime tests solve different problems and should both be used.

PRACTICE
Write a type guard for an object that may contain an id and title, then test valid and invalid objects.''','''type Course = { id: number; title: string };

function isCourse(value: unknown): value is Course {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Record<string, unknown>;
  return typeof candidate.id === "number" && typeof candidate.title === "string";
}

const data: unknown = { id: 1, title: "Python" };
if (isCourse(data)) console.log(data.title);'''),
],
'go': [
('Conditions, switch and loops in Go','''LEARNING OBJECTIVE
Use Go's if, switch and for constructs to control execution.

Go uses if and switch for decisions. Conditions do not need parentheses, but braces are required. Go has one loop keyword: for. It can act as a counter loop, a condition loop or an infinite loop with an explicit break. A range loop visits elements in arrays, slices, maps, strings and channels.

Go's switch cases do not fall through by default. Short variable declarations using := are common inside functions. Keep loop conditions simple and ensure loops can finish.

PRACTICE
Use range to count passing scores in a slice and print the total.''','''package main
import "fmt"

func main() {
    scores := []int{55, 72, 91, 68}
    passes := 0
    for _, score := range scores {
        if score >= 70 { passes++ }
    }
    fmt.Println("Passes:", passes)
}'''),
('Functions and multiple return values','''LEARNING OBJECTIVE
Write Go functions with explicit types and understand multiple return values.

A function declaration includes parameter types and a return type. Go functions can return more than one value, often a result and an error. Callers should check errors rather than ignore them. Keep functions small and make their inputs and outputs clear.

Go passes arguments by value. A pointer can be used when a function needs to modify the caller's data or avoid copying a large structure. Methods attach behaviour to a defined type.

PRACTICE
Write a function that divides two numbers and returns an error when the divisor is zero.''','''package main
import (
    "errors"
    "fmt"
)

func divide(a, b float64) (float64, error) {
    if b == 0 { return 0, errors.New("cannot divide by zero") }
    return a / b, nil
}

func main() {
    result, err := divide(12, 3)
    if err != nil { fmt.Println("Error:", err); return }
    fmt.Println("Result:", result)
}'''),
('Slices, maps and structs','''LEARNING OBJECTIVE
Represent collections and structured records with Go's built-in types.

An array has a fixed length. A slice is a flexible view over an underlying array and is the common sequence type. append may allocate a new underlying array, so assign its result back to the slice. A map stores key-value pairs; reading a map can return a second Boolean value that tells whether the key exists. A struct groups related fields into a named data type.

Be aware that maps are not ordered. Do not rely on iteration order. Initialise a map before writing to it; writing to a nil map causes a panic.

PRACTICE
Create a slice of course names, count completions in a map and represent one course with a struct.''','''package main
import "fmt"

type Course struct { Title string; Lessons int }

func main() {
    names := []string{"Python", "Go"}
    names = append(names, "Rust")
    completed := map[string]int{"Python": 8, "Go": 3}
    course := Course{Title: "Python", Lessons: 12}
    count, found := completed[course.Title]
    fmt.Println(names, course, count, found)
}'''),
('Methods, pointers and interfaces','''LEARNING OBJECTIVE
Attach methods to types and write code that depends on behaviour rather than a concrete implementation.

A method has a receiver, which may be a value or pointer. A pointer receiver can modify the original value and avoids copying a larger structure. Interfaces describe method sets; a type satisfies an interface implicitly by implementing its methods. Small interfaces are easier to reuse and test.

Use interfaces at boundaries where different implementations are useful, such as storage or notification services. Do not create an interface for every type when no abstraction is needed.

PRACTICE
Create a Notifier interface and two implementations that send a message to different destinations (use simple printed output for the exercise).''','''package main
import "fmt"

type Notifier interface { Notify(message string) }
type ConsoleNotifier struct{}
func (ConsoleNotifier) Notify(message string) { fmt.Println("Notice:", message) }

func announce(n Notifier, message string) { n.Notify(message) }

func main() {
    announce(ConsoleNotifier{}, "A new lesson is available")
}'''),
('Errors, wrapping and defer','''LEARNING OBJECTIVE
Return errors explicitly and clean up resources reliably.

Go commonly represents expected failure with the error interface. A function returns an error value and the caller checks whether it is nil. Use fmt.Errorf with %w to wrap an error while preserving its identity for errors.Is and errors.As. Avoid panics for ordinary recoverable conditions.

The defer statement schedules a call to run when the surrounding function returns. It is often used to close files or unlock resources. Deferred calls run in last-in, first-out order.

PRACTICE
Write a function that validates a positive quantity and returns a descriptive error for invalid input.''','''package main
import (
    "errors"
    "fmt"
)

func validateQuantity(value int) error {
    if value < 0 { return fmt.Errorf("quantity %d: %w", value, errors.New("must not be negative")) }
    return nil
}

func main() {
    if err := validateQuantity(-2); err != nil { fmt.Println("Invalid input:", err) }
}'''),
('Packages, modules and dependency management','''LEARNING OBJECTIVE
Organise Go code into packages and manage dependencies with modules.

A Go package groups source files in one directory. The package name appears at the top of each file. A module is a collection of packages described by go.mod. Use go mod init to create a module and go get to add dependencies. Keep packages focused and avoid import cycles.

Exported identifiers begin with an uppercase letter; unexported identifiers begin with a lowercase letter. This naming rule controls visibility across packages. Prefer the standard library when it meets the need and review third-party dependencies before adding them.

PRACTICE
Create a module with a package named calculator that exports an Add function and call it from main.''','''package main

import "fmt"

// In a multi-package project, move Add into package calculator
// and import that package from main.
func Add(a, b int) int { return a + b }

func main() {
    fmt.Println(Add(4, 6))
}
// Initialise a module in a project with: go mod init example.com/academy'''),
('Testing Go packages','''LEARNING OBJECTIVE
Write automated tests using Go's built-in testing package.

Go tests are usually placed in files ending with _test.go. Test functions begin with Test and accept *testing.T. Use t.Errorf or t.Fatalf to report failures. Table-driven tests let you check many input/output pairs without duplicating test structure.

Test ordinary values, boundaries and error conditions. Keep tests deterministic and avoid depending on network services or current time unless that is what you are testing. Run go test ./... to test packages recursively.

PRACTICE
Write table-driven tests for a function that converts minutes to seconds.''','''package main

import "fmt"

func ToSeconds(minutes int) (int, bool) {
    if minutes < 0 { return 0, false }
    return minutes * 60, true
}

func main() {
    cases := []struct{ input, want int }{{0, 0}, {5, 300}}
    for _, tc := range cases {
        got, ok := ToSeconds(tc.input)
        if !ok || got != tc.want { panic("test failed") }
    }
    fmt.Println("All checks passed")
}
// In a real Go test suite, place TestToSeconds in a file ending in _test.go.'''),
],
'rust': [
('Conditions, loops and pattern matching','''LEARNING OBJECTIVE
Control execution using if expressions, loops and match.

Rust if is an expression, so each branch can produce a value. Conditions must be bool. loop repeats until break; while repeats while a condition is true; for is commonly used to iterate over ranges and collections. match checks a value against patterns and must cover every possible case unless a wildcard handles the remainder.

Pattern matching can destructure tuples, enums and structs. Use match when different variants need different behaviour. Keep loops readable and use iterators when they make a transformation clearer.

PRACTICE
Use match to display a message for each menu option and handle unknown values.''','''fn main() {
    let choice = 2;
    let message = match choice {
        1 => "Open lessons",
        2 => "Start practice",
        3 => "View progress",
        _ => "Unknown option",
    };
    println!("{message}");

    for number in 1..=3 { println!("Attempt {number}"); }
}'''),
('Functions, ownership and borrowing','''LEARNING OBJECTIVE
Write functions and understand how ownership and borrowing affect their parameters.

A function signature lists parameter types and an optional return type. Rust moves values by default when ownership transfers. Types that implement Copy, such as many small numeric types, are copied instead. Borrowing with & lets a function read a value without taking ownership; &mut allows controlled mutation when the caller provides a mutable borrow.

The borrow checker ensures references do not outlive the data they point to and prevents conflicting mutable access. These rules help avoid dangling references and data races.

PRACTICE
Write a function that borrows a string slice and returns its character count without taking ownership of the original String.''','''fn character_count(text: &str) -> usize {
    text.chars().count()
}

fn main() {
    let message = String::from("Learn Rust");
    let count = character_count(&message);
    println!("{count} characters in: {message}");
}'''),
('Structs, enums and methods','''LEARNING OBJECTIVE
Create custom data types that model related values and possible states.

A struct groups named fields. An enum represents one of several variants. impl blocks define methods associated with a type. Use #[derive] to request standard traits such as Debug, Clone, PartialEq or Copy when appropriate. Deriving Clone or Copy has semantic and performance implications, so choose deliberately.

Enums are especially useful for representing states that should not be confused with arbitrary strings. match can then force the program to handle each state.

PRACTICE
Create a Course struct and a CourseStatus enum, then write a method that returns whether the course is open for enrolment.''','''#[derive(Debug)]
enum CourseStatus { Draft, Published, Archived }

struct Course {
    title: String,
    status: CourseStatus,
}

impl Course {
    fn can_enrol(&self) -> bool {
        matches!(self.status, CourseStatus::Published)
    }
}

fn main() {
    let course = Course { title: String::from("Rust"), status: CourseStatus::Published };
    println!("{}: {}", course.title, course.can_enrol());
}'''),
('Vectors, hash maps and iterators','''LEARNING OBJECTIVE
Use standard collections and iterator adapters to process data safely.

Vec<T> is a growable sequence. HashMap<K,V> stores key-value pairs and requires keys to implement appropriate hashing and equality traits. Use get to retrieve an optional reference and entry to insert or update values. Iterators provide methods such as map, filter, fold and collect.

Rust iterators are lazy until consumed. collect builds a collection from an iterator, and the target type may need to be specified. Borrowing rules still apply when iterating over a collection and modifying it.

PRACTICE
Count words in a vector with a HashMap and print each word's frequency.''','''use std::collections::HashMap;

fn main() {
    let words = vec!["code", "learn", "code"];
    let mut counts = HashMap::new();
    for word in words {
        *counts.entry(word).or_insert(0) += 1;
    }
    println!("{counts:?}");
}'''),
('Option, Result and error handling','''LEARNING OBJECTIVE
Represent missing values and failures explicitly without relying on null pointers or unchecked exceptions.

Option<T> represents either Some(value) or None. Result<T,E> represents either Ok(value) or Err(error). These enums force callers to consider the possibility that a value is missing or an operation failed. Use match, if let, map, and_then or the ? operator to work with them.

The ? operator returns early from a function when a Result is an error or an Option is None, depending on the return type. Choose meaningful error types and avoid discarding errors without a reason.

PRACTICE
Write a function that parses a positive integer from text and returns a Result with a helpful error.''','''fn parse_quantity(text: &str) -> Result<u32, String> {
    let value: u32 = text.parse().map_err(|_| "Enter a whole number".to_string())?;
    if value == 0 { return Err("Quantity must be greater than zero".into()); }
    Ok(value)
}

fn main() {
    match parse_quantity("12") {
        Ok(value) => println!("Quantity: {value}"),
        Err(message) => println!("Input error: {message}"),
    }
}'''),
('Modules, crates and Cargo','''LEARNING OBJECTIVE
Organise Rust programs into modules and manage builds with Cargo.

A crate is a compilation unit. A binary crate builds an executable; a library crate exposes reusable code. Modules organise items within a crate. pub controls visibility, and use brings names into scope. Cargo manages project metadata, dependencies, builds and tests through Cargo.toml.

Keep modules focused and avoid making every item public. Use cargo fmt to format code, cargo check for fast compilation checks, and cargo test to run tests. Review dependencies and lockfiles as part of project maintenance.

PRACTICE
Create a library module that exports an add function and call it from a binary crate.''','''// src/lib.rs
pub mod calculator {
    pub fn add(a: i32, b: i32) -> i32 { a + b }
}

// src/main.rs
// fn main() {
//     println!("{}", your_crate_name::calculator::add(4, 6));
// }
// Useful commands: cargo check, cargo fmt, cargo test'''),
('Testing Rust code','''LEARNING OBJECTIVE
Write unit tests and use compiler feedback to improve reliability.

Rust supports unit tests in the same module as the code and integration tests in the tests directory. Mark test functions with #[test] and use assert!, assert_eq! and assert_ne! to check results. Use #[should_panic] only when a panic is truly the expected contract; returning Result is often better for recoverable errors.

The compiler's error messages often suggest how to fix ownership and type issues. Read the full diagnostic, including the location and notes. Test ordinary values, boundaries and error paths.

PRACTICE
Write tests for a function that converts minutes to seconds and rejects negative input.''','''fn to_seconds(minutes: i32) -> Result<i32, &'static str> {
    if minutes < 0 { return Err("minutes cannot be negative"); }
    Ok(minutes * 60)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn converts_minutes() { assert_eq!(to_seconds(5), Ok(300)); }
    #[test] fn rejects_negative() { assert!(to_seconds(-1).is_err()); }
}'''),
],
'ruby': [
('Decisions and loops in Ruby','''LEARNING OBJECTIVE
Use conditional expressions and iteration methods to control Ruby programs.

Ruby supports if, elsif and else. It also has unless for a negative condition, though if is often clearer in complex logic. Ruby treats only false and nil as falsey; zero and empty strings are truthy. This differs from several other languages and is important when checking values.

Ruby iterators such as each, times, upto and while express repetition. Blocks are commonly written with do...end or braces. Use break to leave an iteration and next to skip to the next item.

PRACTICE
Loop through a hash of learners and display those with scores above a threshold.''','''learners = { "Ada" => 92, "Tunde" => 68, "Mina" => 81 }

learners.each do |name, score|
  puts "#{name}: #{score}" if score >= 70
end

3.times { |attempt| puts "Practice #{attempt + 1}" }'''),
('Methods, parameters and blocks','''LEARNING OBJECTIVE
Define reusable methods and understand how blocks pass behaviour.

Use def to define a method and end to close it. The final evaluated expression is returned automatically, though an explicit return can make control flow clear. Parameters can have defaults and keyword names. Blocks are chunks of code passed to methods; yield runs a supplied block, while &block captures it as a Proc.

Keep methods focused and choose names that explain the action. Keyword arguments make calls clearer when a method accepts several options.

PRACTICE
Write a method that accepts a list of scores and returns the average, safely handling an empty list.''','''def average(scores)
  return nil if scores.empty?
  scores.sum.to_f / scores.length
end

scores = [70, 85, 95]
result = average(scores)
puts result ? format("Average: %.1f", result) : "No scores yet"'''),
('Arrays, hashes and enumerable methods','''LEARNING OBJECTIVE
Choose Ruby collections and process them with Enumerable methods.

Array stores ordered values and Hash stores key-value pairs. Set is available through the standard library when unique values are required. Enumerable provides methods such as map, select, reject, find, any?, all? and reduce for processing collections.

Methods such as sort! modify an array, while sort returns a new array. Understand which methods mutate their receiver; the exclamation mark is a naming convention often used for mutating methods, not a strict language rule.

PRACTICE
Store product prices in a hash, select products above a threshold and calculate the total.''','''prices = { "Notebook" => 1200, "Mouse" => 8500, "Pen" => 300 }

expensive = prices.select { |_name, price| price >= 1000 }
total = prices.values.sum

puts expensive
puts "Total: #{total}"'''),
('Classes, objects and encapsulation','''LEARNING OBJECTIVE
Create classes that group state and behaviour and control access to data.

A class defines an object type. initialize is called when an instance is created with new. Instance variables begin with @. attr_reader, attr_writer and attr_accessor create common access methods, but unrestricted writers may allow invalid state. Use private and protected to control method visibility.

Ruby is dynamically typed, so objects respond to methods rather than being restricted to declared interfaces. Duck typing means code can work with different objects when they provide the required behaviour.

PRACTICE
Create a Course class with a title and a method that reports whether the course has a valid title.''','''class Course
  attr_reader :title

  def initialize(title)
    raise ArgumentError, "Title is required" if title.nil? || title.strip.empty?
    @title = title.strip
  end

  def summary
    "Course: #{@title}"
  end
end

puts Course.new("Ruby Basics").summary'''),
('Exceptions and file handling','''LEARNING OBJECTIVE
Handle exceptional conditions and work with files safely.

Ruby uses begin, rescue, else and ensure to handle exceptions. Rescue only the exception classes you expect to handle; rescuing Exception broadly can hide serious problems. Raise a specific error when an operation cannot continue.

Use File.open with a block so the file is closed after the block finishes, even if an exception occurs. Choose the correct file mode and encoding. Validate file paths and do not allow untrusted input to select arbitrary sensitive files.

PRACTICE
Read a text file with a block and display a friendly message if it is missing.''','''begin
  File.open("notes.txt", "r", encoding: "UTF-8") do |file|
    puts file.read
  end
rescue Errno::ENOENT
  puts "The notes file was not found."
rescue IOError
  puts "The file could not be read."
end'''),
('Modules, mixins and gems','''LEARNING OBJECTIVE
Organise Ruby code with modules and understand external libraries.

A module groups constants and methods and can be used as a namespace. A class can include a module to gain its instance methods as a mixin. require loads another Ruby file or library. Gems are packaged Ruby libraries, and Bundler uses a Gemfile to manage project dependencies.

Keep modules cohesive and avoid creating global state. Pin and review dependencies for projects that need repeatable builds. Never commit secrets in a Gemfile or source file.

PRACTICE
Create a module with a formatting method and include it in a class.''','''module LabelFormatter
  def label(text)
    "[Course] #{text.strip}"
  end
end

class CourseCard
  include LabelFormatter
end

puts CourseCard.new.label("Ruby")'''),
('Testing Ruby code','''LEARNING OBJECTIVE
Use automated tests to check expected behaviour and prevent regressions.

Minitest is included with Ruby and RSpec is a popular testing framework. A test should set up data, call the method and assert the result. Include boundary cases, invalid values and empty collections. Keep the core logic separate from terminal input and file operations where possible.

Use puts or a debugger for temporary inspection, but remove noisy debug output before release. Run the full test suite after changing shared methods.

PRACTICE
Write a Minitest test for a function that converts minutes to seconds and rejects negative values.''','''require "minitest/autorun"

def to_seconds(minutes)
  raise ArgumentError, "negative minutes" if minutes < 0
  minutes * 60
end

class TimeTest < Minitest::Test
  def test_conversion
    assert_equal 300, to_seconds(5)
    assert_equal 0, to_seconds(0)
  end

  def test_negative_input
    assert_raises(ArgumentError) { to_seconds(-1) }
  end
end'''),
],
'swift': [
('Conditions, loops and switch in Swift','''LEARNING OBJECTIVE
Control program flow with if, guard, switch and loop statements.

Swift conditions must evaluate to Bool. Use if and else for decisions. guard is useful for exiting early when a required condition is not met. switch matches values and must handle all possible cases; use default when appropriate. for-in iterates over sequences, while repeats while a condition is true, and repeat-while runs its body at least once.

Swift switch can match ranges and patterns. Use let or var deliberately: let creates a constant and var creates a variable. Prefer immutable values unless a change is required.

PRACTICE
Use switch to assign a grade label to a score and handle values outside the expected range.''','''let score = 86
let grade: String

switch score {
case 90...100: grade = "A"
case 80..<90: grade = "B"
case 70..<80: grade = "C"
case 0..<70: grade = "Keep practising"
default: grade = "Invalid score"
}
print("Grade: \\(grade)")'''),
('Functions, parameters and return values','''LEARNING OBJECTIVE
Create functions with clear parameter labels and return types.

A Swift function is declared with func. External parameter labels make calls read naturally; an underscore removes an external label. A function can return a value after ->. Use default parameter values when a common option is appropriate. Functions can return tuples when several related values are needed.

Swift uses value semantics for structs and enums, while classes have reference semantics. Use inout only when a function genuinely needs to modify a caller's variable.

PRACTICE
Write a function that calculates a total price with an optional tax rate and rejects negative values.''','''import Foundation

func totalWithTax(price: Double, rate: Double = 0.075) -> Double? {
    guard price >= 0, rate >= 0 else { return nil }
    return price * (1 + rate)
}

if let total = totalWithTax(price: 1200) {
    print(String(format: "Total: %.2f", total))
}'''),
('Arrays, dictionaries and sets','''LEARNING OBJECTIVE
Choose Swift collection types and understand value semantics.

Array stores ordered values and allows duplicates. Dictionary maps keys to values, and Set stores unique values. These collections are value types: assigning one to another gives value semantics, with copy-on-write optimisation in common implementations. Use let when a collection should not be changed through that binding.

Dictionary lookup returns an optional because a key may not exist. Use optional binding or a default value. Collection methods such as map, filter and reduce help transform data.

PRACTICE
Count unique course tags with Set and use a dictionary to store lesson completion totals.''','''let courses = ["Python", "Swift", "Python", "HTML"]
let uniqueCourses = Set(courses)
let completed = ["Python": 8, "Swift": 3]
let swiftCount = completed["Swift"] ?? 0
let labels = courses.map { $0.uppercased() }

print(uniqueCourses)
print("Swift lessons: \\(swiftCount)")
print(labels)'''),
('Structs, classes and protocols','''LEARNING OBJECTIVE
Model data with structs and classes and define shared behaviour with protocols.

A struct is a value type and is commonly used for data models. A class is a reference type and supports inheritance and identity. Use let and var to control whether a binding can be reassigned or a value can be mutated. A protocol defines requirements that conforming types implement.

Prefer structs for simple value-like models and protocols for capabilities shared by different types. Use classes when reference identity or inheritance is genuinely needed. Keep properties and methods cohesive.

PRACTICE
Define a Course protocol and implement it with a struct that exposes a title and lesson count.''','''protocol LearningCourse {
    var title: String { get }
    var lessonCount: Int { get }
}

struct Course: LearningCourse {
    let title: String
    let lessonCount: Int
}

func describe(_ course: some LearningCourse) {
    print("\\(course.title): \\(course.lessonCount) lessons")
}

describe(Course(title: "Swift", lessonCount: 12))'''),
('Optionals and error handling','''LEARNING OBJECTIVE
Represent missing values safely and handle operations that can fail.

An optional type represents either a value or nil. Use if let or guard let to unwrap an optional safely. Avoid force-unwrapping with ! unless you can prove the value is present. The nil-coalescing operator ?? provides a fallback value.

Swift errors use throws, throw and do/catch. A throwing function declares throws and callers must handle or propagate the error with try. Use Result when an API needs to store success or failure as a value.

PRACTICE
Parse a number from text, handle a missing value and return a clear message for invalid input.''','''enum QuantityError: Error { case invalid }

func parseQuantity(_ text: String) throws -> Int {
    guard let value = Int(text), value >= 0 else {
        throw QuantityError.invalid
    }
    return value
}

do {
    print(try parseQuantity("12"))
} catch {
    print("Enter a valid non-negative whole number.")
}'''),
('Modules, packages and Swift Package Manager','''LEARNING OBJECTIVE
Organise Swift code into reusable files and manage package dependencies.

Swift files in a module can share declarations according to access control. Use import to access another module. Swift Package Manager uses Package.swift to describe targets and dependencies. A target can be a library, executable or test target.

Access levels include private, fileprivate, internal, public and open. Choose the least permissive access level that supports the intended API. Keep implementation details hidden unless other modules need them.

PRACTICE
Create a small Swift package with a library target that exports a simple calculator function and a test target.''','''// Sources/Calculator/Calculator.swift
public enum Calculator {
    public static func add(_ first: Int, _ second: Int) -> Int {
        first + second
    }
}

// In a client target, import Calculator and call Calculator.add(4, 6).
// Create a package with: swift package init --type library'''),
('Testing Swift code','''LEARNING OBJECTIVE
Use XCTest to check expected behaviour and catch regressions.

XCTest is Apple's testing framework. Test methods use assertions such as XCTAssertEqual, XCTAssertTrue and XCTAssertThrowsError. Separate calculations from UI and system dependencies so they can be tested directly. Include normal values, boundaries and error conditions.

Run tests through Xcode or Swift Package Manager. When a test fails, inspect the expected and actual values, then reproduce the issue with the smallest input that demonstrates it.

PRACTICE
Write tests for a function that converts minutes to seconds and rejects negative input.''','''import XCTest

func toSeconds(_ minutes: Int) -> Int? {
    guard minutes >= 0 else { return nil }
    return minutes * 60
}

final class TimeTests: XCTestCase {
    func testConversion() {
        XCTAssertEqual(toSeconds(5), 300)
        XCTAssertEqual(toSeconds(0), 0)
        XCTAssertNil(toSeconds(-1))
    }
}'''),
],
'kotlin': [
('Conditions, when and loops in Kotlin','''LEARNING OBJECTIVE
Control program flow with if, when, for and while.

Kotlin if is an expression and can return a value. when is a flexible alternative to switch and can match values, ranges and types. for iterates over ranges and collections; while and do-while repeat based on conditions. Kotlin conditions must be Boolean.

Use ranges such as 1..5 for inclusive ranges and until when the end should be excluded. Use break and continue to control loops, but keep the normal loop condition understandable.

PRACTICE
Use when to assign a grade label and handle scores outside the expected range.''','''fun main() {
    val score = 86
    val grade = when (score) {
        in 90..100 -> "A"
        in 80..89 -> "B"
        in 70..79 -> "C"
        in 0..69 -> "Keep practising"
        else -> "Invalid score"
    }
    println("Grade: $grade")
    for (attempt in 1..3) println("Attempt $attempt")
}'''),
('Functions, default arguments and named parameters','''LEARNING OBJECTIVE
Write functions with explicit inputs and outputs and use Kotlin's concise syntax.

Use fun to declare a function. Kotlin infers many local types, but explicit return types are useful for public APIs. Default parameter values let callers omit common options. Named arguments make calls easier to understand when several parameters have similar types. A single-expression function can use =.

Kotlin functions can be top-level and do not need to belong to a class. Keep functions focused and prefer returning a value over printing from inside calculation logic.

PRACTICE
Write a function that calculates a total after tax with a default tax rate.''','''fun totalWithTax(price: Double, rate: Double = 0.075): Double {
    require(price >= 0 && rate >= 0) { "Values cannot be negative" }
    return price * (1 + rate)
}

fun main() {
    println("Total: %.2f".format(totalWithTax(price = 1200.0)))
}'''),
('Lists, sets and maps','''LEARNING OBJECTIVE
Choose Kotlin collection types and understand read-only versus mutable interfaces.

List preserves order and can contain duplicates. Set stores unique elements. Map stores key-value pairs. Kotlin distinguishes read-only collection interfaces from mutable interfaces; a val reference cannot be reassigned, but the object it refers to may still be mutable if its type allows changes.

Use map, filter, sortedBy, any and fold to process collections. Be aware that these operations usually return new collections rather than changing the original. Use getOrElse or the Elvis operator ?: when a map lookup may be absent.

PRACTICE
Store scores in a map, filter passing scores and calculate their average.''','''fun main() {
    val scores = mapOf("Ada" to 92, "Tunde" to 68, "Mina" to 81)
    val passes = scores.filterValues { it >= 70 }
    val average = scores.values.average()
    val missing = scores["Favour"] ?: 0
    println(passes)
    println("Average: $average; missing score: $missing")
}'''),
('Classes, data classes and interfaces','''LEARNING OBJECTIVE
Represent objects with classes and use data classes for value-like records.

A class defines properties and behaviour. A primary constructor can declare properties directly. A data class automatically provides useful functions such as equals, hashCode, toString and copy based on its primary-constructor properties. An interface defines behaviour that classes can implement.

Use private setters or controlled methods when state must obey rules. Prefer data classes for simple records and ordinary classes when behaviour or invariants are more complex.

PRACTICE
Create a data class for a course and an interface that describes an object capable of reporting progress.''','''data class Course(val title: String, val lessonCount: Int)

interface ProgressReporter {
    fun report(): String
}

class CourseProgress(private val course: Course, private val completed: Int) : ProgressReporter {
    override fun report(): String = "${course.title}: $completed/${course.lessonCount}"
}

fun main() {
    println(CourseProgress(Course("Kotlin", 12), 5).report())
}'''),
('Null safety and exception handling','''LEARNING OBJECTIVE
Handle absent values and exceptional operations without unsafe assumptions.

Kotlin distinguishes nullable types, such as String?, from non-null types, such as String. Use safe calls ?. to access a value only when it exists, the Elvis operator ?: to provide a fallback, and let or explicit checks to work with a non-null value. The !! operator forces a value to be treated as non-null and can throw, so avoid it unless the invariant is guaranteed.

Use try/catch for exceptions. Kotlin does not require checked exceptions to be declared. Validate external data even when the compiler's type system is strong; types do not automatically validate network responses or user input.

PRACTICE
Parse a quantity from text, reject negative numbers and handle invalid input with a safe message.''','''fun parseQuantity(text: String): Int? {
    val value = text.toIntOrNull() ?: return null
    return value.takeIf { it >= 0 }
}

fun main() {
    val quantity = parseQuantity("12") ?: 0
    println("Quantity: $quantity")
}'''),
('Packages, imports and Gradle basics','''LEARNING OBJECTIVE
Organise Kotlin files and understand how a project manages dependencies.

A package declaration identifies the package a Kotlin file belongs to. import brings names into scope. Keep source files organised by feature or responsibility. Gradle is commonly used to build Kotlin/JVM and Android projects; build scripts declare plugins, repositories, dependencies and tasks.

Do not add dependencies without a reason. Keep versions controlled and review library maintenance and security. Separate application logic from platform-specific UI code so more of the program can be tested.

PRACTICE
Create a package named academy.math with a Calculator object and call its add function from another package.''','''// Calculator.kt
package academy.math

object Calculator {
    fun add(first: Int, second: Int): Int = first + second
}

// In another file:
// import academy.math.Calculator
// println(Calculator.add(4, 6))'''),
('Testing Kotlin code','''LEARNING OBJECTIVE
Write repeatable tests and use assertions to verify Kotlin behaviour.

Kotlin/JVM projects commonly use JUnit. A test should set up values, call the function and assert the result. Test ordinary inputs, boundaries and invalid values. Keep calculations independent from Android views, network services or current time so they can be tested quickly.

Use the IDE debugger to inspect variables and the call stack. Run tests after changing shared code, and treat a passing test suite as useful evidence rather than proof that every possible defect is absent.

PRACTICE
Write tests for a function that converts minutes into seconds and returns null for negative input.''','''import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test

fun toSeconds(minutes: Int): Int? =
    if (minutes < 0) null else minutes * 60

class TimeTests {
    @Test fun convertsMinutes() {
        assertEquals(300, toSeconds(5))
        assertEquals(0, toSeconds(0))
        assertNull(toSeconds(-1))
    }
}'''),
]
}

# Append language-specific lessons to the five existing full curricula and supply
# a complete, useful set for the remaining eleven languages.
ADDITIONAL_LESSONS = {slug: lessons for slug, lessons in LANGUAGE_LESSONS.items()}

CORE_EXTRAS = {
'python': [
('List comprehensions and generator expressions', '''LEARNING OBJECTIVE
Transform and filter data with concise comprehensions, and understand lazy generator expressions.

A list comprehension creates a new list from an iterable. Its basic form is [expression for item in iterable], and an optional if clause filters values. Nested comprehensions are possible, but deeply nested expressions are often clearer as ordinary loops. A generator expression uses parentheses and produces values lazily, which can reduce memory use when processing a large sequence once.

Choose clarity over cleverness. Use a comprehension when the transformation is straightforward and a loop when the logic needs several steps or error handling.

PRACTICE
From a list of scores, create a list of passing scores and a generator that yields their squared values.''','''scores = [55, 72, 91, 68, 84]
passing = [score for score in scores if score >= 70]
squared = (score ** 2 for score in passing)

print("Passing:", passing)
print("Squared values:", list(squared))'''),
('Working with files and paths', '''LEARNING OBJECTIVE
Read and write files while handling encodings, paths and failures safely.

Use open with a context manager so the file is closed automatically. Select a mode such as r for reading, w for replacing a file, a for appending, or x for exclusive creation. Specify an encoding such as UTF-8 for text. pathlib.Path provides an object-oriented way to build and inspect paths.

Do not assume a file exists or that its contents are valid. Catch expected OSError subclasses and validate parsed data. Avoid building paths from untrusted input without checking where they resolve.

PRACTICE
Write a small program that saves a list of course names to a UTF-8 text file and reads it back.''','''from pathlib import Path

path = Path("courses.txt")
courses = ["Python", "JavaScript", "SQL"]

path.write_text("\\n".join(courses), encoding="utf-8")
loaded = path.read_text(encoding="utf-8").splitlines()
print("Saved courses:", loaded)'''),
('Object-oriented programming with classes', '''LEARNING OBJECTIVE
Create classes that represent objects with state and behaviour.

A class defines a new type. __init__ initialises each instance, and self refers to the current instance. Instance attributes belong to an object; class attributes are shared through the class and should not be used as mutable per-instance defaults. Methods describe behaviour. Properties can provide controlled attribute access.

Use composition when one object contains or uses another. Inheritance is useful for a genuine specialised relationship, but deep inheritance hierarchies are difficult to maintain. Dataclasses can reduce boilerplate for simple data containers.

PRACTICE
Create a Course class with a title, lesson count and a method that reports progress percentage.''','''class Course:
    def __init__(self, title, lesson_count):
        if lesson_count < 1:
            raise ValueError("A course must contain at least one lesson")
        self.title = title
        self.lesson_count = lesson_count
        self.completed = 0

    def complete_lesson(self):
        self.completed = min(self.completed + 1, self.lesson_count)

    @property
    def progress(self):
        return self.completed / self.lesson_count * 100

course = Course("Python", 10)
course.complete_lesson()
print(f"{course.title}: {course.progress:.0f}%")'''),
('Working with JSON data', '''LEARNING OBJECTIVE
Exchange structured data using JSON and validate data after parsing.

The json module converts between Python values and JSON text. json.dumps serialises an object to text; json.loads parses text. json.dump and json.load work with file objects. JSON supports objects, arrays, strings, numbers, booleans and null, but it does not represent every Python object directly.

Parsing JSON does not prove that the data has the structure your program expects. Check required keys, value types and ranges before using it. Catch JSONDecodeError for malformed input and OSError for file failures.

PRACTICE
Save a dictionary of learner details as JSON, read it back and verify that the expected keys exist.''','''import json
from pathlib import Path

learner = {"username": "ada", "completed_lessons": 8}
path = Path("learner.json")
path.write_text(json.dumps(learner, indent=2), encoding="utf-8")

loaded = json.loads(path.read_text(encoding="utf-8"))
if isinstance(loaded, dict) and isinstance(loaded.get("completed_lessons"), int):
    print(loaded["username"], loaded["completed_lessons"])'''),
('Virtual environments, packages and pip', '''LEARNING OBJECTIVE
Install third-party packages without mixing project dependencies with the system Python installation.

A virtual environment creates an isolated Python environment for a project. Create it with python -m venv .venv and activate it using the command for your operating system. Install packages with python -m pip install package-name. Record project dependencies in requirements.txt so another developer can reproduce the environment.

Use supported package versions and keep dependencies updated. Do not commit the virtual environment directory or private credentials. A virtual environment isolates Python packages but is not a security sandbox.

PRACTICE
Create a virtual environment, install a small package, record it in requirements.txt and recreate the environment from that file.''','''# Create an environment
# Windows PowerShell:
# py -m venv .venv
# .\\.venv\\Scripts\\Activate.ps1
#
# macOS/Linux:
# python3 -m venv .venv
# source .venv/bin/activate
#
# Install and record dependencies:
# python -m pip install requests
# python -m pip freeze > requirements.txt
# python -m pip install -r requirements.txt'''),
('Asynchronous programming with asyncio', '''LEARNING OBJECTIVE
Understand coroutines and use asyncio for tasks that spend time waiting on I/O.

async def defines a coroutine function. Calling it creates a coroutine object; it does not run to completion until awaited or scheduled. await pauses the current coroutine while the awaited operation is pending, allowing other tasks on the event loop to make progress. asyncio.run starts and manages an event loop for a top-level async program.

Async code is useful for concurrent I/O, not automatically faster for CPU-heavy calculations. Use asyncio.sleep rather than time.sleep inside an async function. Handle exceptions from awaited tasks and avoid creating unbounded numbers of tasks.

PRACTICE
Write two coroutines that simulate independent waits and run them together with asyncio.gather.''','''import asyncio

async def fetch_lesson(name, delay):
    await asyncio.sleep(delay)
    return f"Loaded {name}"

async def main():
    results = await asyncio.gather(
        fetch_lesson("Python", 0.2),
        fetch_lesson("SQL", 0.1),
    )
    for result in results:
        print(result)

asyncio.run(main())'''),
],
'javascript': [
('Event handling and event propagation', '''LEARNING OBJECTIVE
Respond to user actions and understand how browser events travel through the DOM.

Use addEventListener to register a function for an event such as click, input, submit or keydown. The event object contains information about what happened. Events commonly travel through capture, target and bubble phases. Bubbling lets a parent handle events from descendants, a technique called event delegation.

Use event.target to inspect the originating element and event.currentTarget for the element whose listener is currently running. For form submission, prevent the browser's default navigation only when your JavaScript will handle the action. Keep keyboard interaction available and use semantic controls.

PRACTICE
Add one click listener to a list container and use event delegation to identify which course item was clicked.''','''const list = document.querySelector('#course-list');

list?.addEventListener('click', event => {
  const item = event.target.closest('[data-course-id]');
  if (!item || !list.contains(item)) return;
  console.log('Selected course:', item.dataset.courseId);
});'''),
('Forms, validation and user feedback', '''LEARNING OBJECTIVE
Read form values, validate them and display accessible feedback.

Listen for the submit event on a form. Use FormData to collect named controls. Browser constraint validation can be checked with checkValidity and reportValidity, but server-side validation remains essential. Trim text fields, check expected formats and show errors near the relevant controls.

Avoid inserting user-provided strings with innerHTML. Use textContent for messages. Associate help and error text with form controls using labels and aria-describedby. Do not rely on colour alone to communicate success or failure.

PRACTICE
Validate a username field and show a message when it is too short.''','''const form = document.querySelector('#signup-form');
const message = document.querySelector('#form-message');

form?.addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(form);
  const username = String(data.get('username') || '').trim();
  if (username.length < 3) {
    message.textContent = 'Username must contain at least 3 characters.';
    return;
  }
  message.textContent = 'The form passed basic checks.';
});'''),
('DOM creation and efficient updates', '''LEARNING OBJECTIVE
Create, insert, update and remove elements without unsafe HTML insertion.

Use document.createElement to create a node, set safe properties such as textContent, and append it to a parent. Use DocumentFragment when building many nodes before inserting them. classList manages CSS classes. remove deletes a node. For user-provided content, textContent is safer than innerHTML because it treats the value as text.

Avoid repeatedly reading and writing layout properties in a loop because that can cause expensive layout recalculations. Build the new content first, then insert it in one operation when practical.

PRACTICE
Build a list of course titles from an array and append the completed fragment to the page.''','''const courses = ['Python', 'JavaScript', 'SQL'];
const list = document.querySelector('#course-list');
const fragment = document.createDocumentFragment();

for (const title of courses) {
  const item = document.createElement('li');
  item.textContent = title;
  fragment.append(item);
}

list?.replaceChildren(fragment);'''),
('Fetch API and working with HTTP responses', '''LEARNING OBJECTIVE
Request data from a server and handle HTTP and network failures.

fetch returns a Promise that resolves to a Response when a response is received. A 404 or 500 response does not normally reject the promise, so check response.ok or response.status. Parse JSON with response.json(), which is also asynchronous. Handle network errors and invalid response data.

Send JSON by setting the Content-Type header and serialising the request body with JSON.stringify. Do not put private API keys in browser code. The server must authenticate and authorise requests and validate all received data.

PRACTICE
Fetch a list of courses from a same-origin endpoint and show a friendly error if the request fails.''','''async function loadCourses() {
  try {
    const response = await fetch('/api/courses');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const courses = await response.json();
    if (!Array.isArray(courses)) throw new Error('Unexpected response format');
    console.log(courses);
  } catch (error) {
    console.error('Could not load courses:', error);
  }
}

loadCourses();'''),
('Promises and async/await', '''LEARNING OBJECTIVE
Represent work that completes later and coordinate asynchronous operations.

A Promise has pending, fulfilled or rejected state. then handles a fulfilled value, catch handles rejection and finally runs after settlement. async functions return promises, and await makes promise-based code easier to read. A rejected promise throws at the await point and can be handled with try/catch.

Promise.all waits for all supplied promises and rejects if one rejects. Promise.allSettled waits for every promise and reports each outcome. Choose based on whether every task must succeed or partial results are useful.

PRACTICE
Run two independent asynchronous course requests together and handle failures.''','''async function loadDashboard() {
  const tasks = [
    fetch('/api/courses').then(response => {
      if (!response.ok) throw new Error('Courses request failed');
      return response.json();
    }),
    fetch('/api/progress').then(response => {
      if (!response.ok) throw new Error('Progress request failed');
      return response.json();
    })
  ];

  try {
    const [courses, progress] = await Promise.all(tasks);
    console.log({ courses, progress });
  } catch (error) {
    console.error(error);
  }
}'''),
('Browser storage, cookies and security basics', '''LEARNING OBJECTIVE
Understand browser storage choices and avoid placing sensitive data in the wrong place.

localStorage persists string data for an origin. sessionStorage lasts for a tab session. Cookies can be sent automatically with HTTP requests and can carry attributes such as Secure, HttpOnly and SameSite when set by a server. Each storage mechanism has different security and lifetime properties.

Do not store passwords, private API keys or session identifiers in localStorage. HttpOnly cookies cannot be read by page JavaScript, which helps reduce token theft through some script injection scenarios. Still use HTTPS, secure cookie settings, CSRF protection and safe output handling. Browser storage is not a substitute for server-side authorisation.

PRACTICE
Save a non-sensitive theme preference in localStorage and restore it when the page loads.''','''const themeButton = document.querySelector('#theme-toggle');
const savedTheme = localStorage.getItem('site-theme');
if (savedTheme === 'light') document.body.classList.add('light-theme');

themeButton?.addEventListener('click', () => {
  document.body.classList.toggle('light-theme');
  const theme = document.body.classList.contains('light-theme') ? 'light' : 'dark';
  localStorage.setItem('site-theme', theme);
});'''),
],
'html': [
('Metadata, SEO and social sharing basics', '''LEARNING OBJECTIVE
Provide meaningful document metadata that helps browsers, search engines and sharing services understand a page.

The title element names the document and appears in browser tabs and search results. A useful meta description summarises the page. The lang attribute on html identifies the primary language. Viewport metadata helps mobile browsers lay out pages at the device width. Open Graph metadata can influence how a page is previewed when shared, but the preview service decides what it uses.

Metadata should describe the actual page. Do not stuff titles and descriptions with repeated keywords. Keep page titles unique and concise, and ensure the visible page heading matches the page's purpose.

PRACTICE
Write the head section for a course page with a unique title, description, language, viewport and social-sharing title.''','''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Python Beginner Course | FelixForge Academy</title>
  <meta name="description" content="Learn Python fundamentals with examples and exercises.">
  <meta property="og:title" content="Python Beginner Course">
  <meta property="og:description" content="A practical introduction to Python programming.">
</head>
<body><h1>Python Beginner Course</h1></body>
</html>'''),
('Native disclosure, dialog and interactive HTML elements', '''LEARNING OBJECTIVE
Use built-in HTML elements for common interactions before reaching for custom JavaScript.

The details and summary elements create a disclosure widget. The dialog element represents a dialog that can be opened with showModal or show. The dialog's built-in behaviour includes focus handling that custom overlays must otherwise implement carefully. Use button elements for actions and links for navigation.

Native controls generally provide keyboard and accessibility behaviour more reliably than custom elements. Still test them in the browsers and assistive technologies you support, and give every control a clear accessible name.

PRACTICE
Create a details panel for a lesson hint and a dialog that confirms a learner wants to submit an assessment.''','''<details>
  <summary>Show a hint</summary>
  <p>Break the problem into smaller steps before writing code.</p>
</details>

<button type="button" id="open-dialog">Submit assessment</button>
<dialog id="confirm-dialog">
  <p>Are you ready to submit?</p>
  <form method="dialog">
    <button value="cancel">Review answers</button>
    <button value="confirm">Confirm submission</button>
  </form>
</dialog>
<script>
  const dialog = document.querySelector('#confirm-dialog');
  document.querySelector('#open-dialog').addEventListener('click', () => dialog.showModal());
</script>'''),
('Accessible navigation and page landmarks', '''LEARNING OBJECTIVE
Make a page understandable to people navigating visually, by keyboard or with assistive technology.

Use landmark elements such as header, nav, main and footer to describe major page regions. Give multiple navigation regions distinct accessible labels. Use headings in a logical hierarchy and provide a skip link so keyboard users can move past repeated navigation. Keep focus visible and ensure interactive elements can be reached with a keyboard.

ARIA adds semantics when native HTML is not sufficient; it should not replace semantic elements that already provide the needed role. Incorrect ARIA can make an interface less understandable.

PRACTICE
Build a page with a skip link, labelled navigation, main content and a footer. Test it using only the keyboard.''','''<a href="#main-content">Skip to main content</a>
<header><h1>FelixForge Academy</h1></header>
<nav aria-label="Primary navigation">
  <a href="/courses">Courses</a>
  <a href="/projects">Projects</a>
</nav>
<main id="main-content" tabindex="-1">
  <h2>Learning dashboard</h2>
  <p>Your next lesson is ready.</p>
</main>
<footer><p>Learning resources</p></footer>'''),
('Responsive images and performance hints', '''LEARNING OBJECTIVE
Choose image resources and loading behaviour that suit different screen sizes.

The srcset and sizes attributes allow browsers to choose an appropriate image candidate based on device and layout conditions. picture can provide different image sources for formats or art direction. width and height attributes reserve layout space and reduce content movement. loading="lazy" can defer off-screen images, while fetchpriority="high" may be useful for an important above-the-fold image.

Do not lazy-load every image indiscriminately; the main hero image may need to load promptly. Use descriptive alt text and modern compressed formats where appropriate.

PRACTICE
Create a responsive course banner with two image sizes and fixed intrinsic dimensions.''','''<picture>
  <source
    type="image/webp"
    srcset="course-small.webp 480w, course-large.webp 1200w"
    sizes="(max-width: 600px) 100vw, 80vw">
  <img
    src="course-large.jpg"
    alt="Learner practising programming at a laptop"
    width="1200" height="675"
    loading="lazy">
</picture>'''),
('Embedding external content safely', '''LEARNING OBJECTIVE
Embed maps, videos or other external resources while limiting unnecessary permissions.

The iframe element embeds another browsing context. Give it a descriptive title so users understand what it contains. Use loading="lazy" for non-critical embeds and consider sandbox to restrict capabilities. The allow attribute can grant specific features, such as autoplay or fullscreen, so do not grant more permissions than necessary.

An embedded page is a separate document and may have its own privacy and security implications. Use trusted sources, explain when third-party content is loaded and avoid embedding content that asks users for credentials unexpectedly.

PRACTICE
Embed a trusted lesson video with a title, lazy loading and only the permissions it needs.''','''<iframe
  src="https://www.youtube-nocookie.com/embed/VIDEO_ID"
  title="Introduction to HTML lesson video"
  loading="lazy"
  referrerpolicy="strict-origin-when-cross-origin"
  allow="fullscreen; picture-in-picture"
  allowfullscreen>
</iframe>'''),
('HTML validation and browser debugging', '''LEARNING OBJECTIVE
Use validation and developer tools to identify structural and loading problems.

A standards-based validator checks markup against HTML rules. Browser developer tools let you inspect the live DOM, computed styles, console errors, network requests and accessibility information. The Elements panel shows the DOM after browser parsing; it may differ from the source if scripts modify it.

Fix invalid nesting, duplicate ids, missing labels and broken resource paths. Test at multiple viewport sizes and use keyboard navigation. A page that looks correct in one browser width may still have semantic or accessibility problems.

PRACTICE
Create a deliberately malformed form, validate it, inspect the browser's DOM and fix the issues.''','''<!-- Example of a valid, labelled form -->
<form action="/search" method="get">
  <label for="query">Search lessons</label>
  <input id="query" name="q" type="search" required>
  <button type="submit">Search</button>
</form>

<!-- Check the page with an HTML validator and browser developer tools. -->'''),
],
'css': [
('Positioning, stacking contexts and z-index', '''LEARNING OBJECTIVE
Position elements and understand why z-index sometimes appears not to work.

The position property can be static, relative, absolute, fixed or sticky. Absolute positioning uses a containing block, often established by a positioned ancestor. Fixed positioning is normally relative to the viewport, while sticky positioning behaves like relative until a scroll threshold is reached.

z-index controls stacking within stacking contexts. Properties such as transform, opacity below one and certain positioned elements can create a new stacking context. A child with a very large z-index cannot escape its ancestor's stacking context. Prefer a simple layering system rather than assigning arbitrary huge values.

PRACTICE
Create a sticky course header and a notification badge positioned within a card.''','''.course-header {
  position: sticky;
  top: 0;
  z-index: 20;
  background: white;
}

.course-card { position: relative; }
.notification-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  z-index: 1;
}'''),
('Pseudo-classes and pseudo-elements', '''LEARNING OBJECTIVE
Style elements based on state and add decorative content without extra markup.

Pseudo-classes such as :hover, :focus-visible, :checked, :disabled, :first-child and :nth-child select elements based on state or position. Use :focus-visible to provide a clear keyboard focus indicator without necessarily styling every pointer interaction.

Pseudo-elements such as ::before and ::after create generated content associated with an element. They are useful for decoration, not for essential information that should be available to assistive technologies. The content property is required for generated text or symbols.

PRACTICE
Style a button's hover and focus states and add a decorative marker before a lesson title.''','''.button:hover { filter: brightness(0.94); }
.button:focus-visible {
  outline: 3px solid #2563eb;
  outline-offset: 3px;
}

.lesson-title::before {
  content: "›";
  margin-right: 0.5rem;
  color: #2563eb;
}'''),
('Forms and interactive state styling', '''LEARNING OBJECTIVE
Style form controls consistently while preserving usability and focus visibility.

Form controls have browser-specific default appearances. Set font properties explicitly so controls match surrounding text. Use :focus-visible for a visible focus indicator, :disabled for unavailable controls, :checked for selected controls and :invalid for values that fail native constraints. Avoid removing outlines without providing an equally visible replacement.

Do not communicate errors only through colour. Pair invalid styles with text and accessible descriptions. Check contrast for text, borders and focus indicators.

PRACTICE
Style a form input in normal, focus, invalid and disabled states.''','''.field input {
  width: 100%;
  padding: 0.7rem 0.85rem;
  font: inherit;
  border: 1px solid #94a3b8;
  border-radius: 0.5rem;
}
.field input:focus-visible {
  outline: 3px solid #93c5fd;
  outline-offset: 2px;
}
.field input:invalid:not(:placeholder-shown) {
  border-color: #b91c1c;
}
.field input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}'''),
('CSS architecture and component organisation', '''LEARNING OBJECTIVE
Organise stylesheets so that components are predictable and changes do not create unexpected side effects.

A stylesheet can be organised into tokens, base styles, layout rules, components and utilities. Use class selectors for reusable components and avoid selectors that depend on deep document structure. CSS custom properties provide shared design tokens. A naming convention such as block-element-modifier can make component relationships easier to recognise.

Keep specificity low and avoid global selectors that unexpectedly affect unrelated widgets. Use @layer when you want explicit cascade layers and understand how they interact with specificity and importance.

PRACTICE
Create a reusable card component with base, featured and compact variants using classes and custom properties.''','''@layer tokens, base, components, utilities;

@layer tokens {
  :root { --card-radius: 0.8rem; --card-gap: 1rem; }
}

@layer components {
  .card {
    padding: var(--card-gap);
    border-radius: var(--card-radius);
    border: 1px solid #cbd5e1;
  }
  .card--featured { border-width: 2px; }
  .card--compact { --card-gap: 0.5rem; }
}'''),
('Container queries and modern responsive components', '''LEARNING OBJECTIVE
Adapt a component to the width of its container rather than only the viewport.

A container can be established with container-type: inline-size. A @container rule then applies styles when that container reaches a size threshold. This is useful when the same card appears in a wide main column and a narrow sidebar: the component can adapt to the space it actually receives.

Container queries complement media queries. Use media queries for page-level viewport changes and container queries for component-level layout changes. Check browser support for the features you choose and provide a reasonable base layout.

PRACTICE
Create a course card that switches from a horizontal layout to a stacked layout when its container is narrow.''','''.course-list { container-type: inline-size; }

.course-card {
  display: grid;
  grid-template-columns: 7rem 1fr;
  gap: 1rem;
}

@container (max-width: 32rem) {
  .course-card { grid-template-columns: 1fr; }
}'''),
('CSS accessibility and contrast', '''LEARNING OBJECTIVE
Create styles that remain usable for people with different vision, input methods and motion preferences.

Text and interactive states need sufficient contrast against their backgrounds. Do not use colour as the only signal for status; add text, icons with accessible labels or other cues. Provide a visible focus indicator for keyboard users. Respect prefers-reduced-motion and avoid flashing or unnecessarily animated content.

Use relative units so text can be enlarged. Do not lock content into fixed heights that clip when text wraps or zoom increases. Test at narrow widths, with keyboard navigation and with increased text size.

PRACTICE
Review a form's text, error, focus and disabled states and improve contrast and non-colour cues.''','''.status-error {
  color: #991b1b;
  background: #fee2e2;
  border-left: 0.25rem solid currentColor;
  padding: 0.75rem 1rem;
}

:focus-visible {
  outline: 3px solid #1d4ed8;
  outline-offset: 3px;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    scroll-behavior: auto !important;
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}'''),
],
'sql': [
('NULL values and conditional expressions', '''LEARNING OBJECTIVE
Handle missing data correctly and create conditional values in query results.

NULL means a value is missing or unknown. It is not equal to zero, an empty string or another NULL. Use IS NULL and IS NOT NULL to test it. SQL uses three-valued logic: a comparison involving NULL can evaluate to UNKNOWN, which is not selected by a WHERE clause.

COALESCE returns the first non-NULL expression. CASE creates conditional values in a query. Be careful when replacing NULL with a default because doing so may hide the difference between missing information and a real zero value.

PRACTICE
Display each learner's score, substituting the label 'Not assessed' when the score is NULL.''','''SELECT
  username,
  CASE
    WHEN score IS NULL THEN 'Not assessed'
    WHEN score >= 70 THEN 'Pass'
    ELSE 'Needs practice'
  END AS result_label,
  COALESCE(score, 0) AS score_for_display
FROM learners;'''),
('UNION, DISTINCT and set operations', '''LEARNING OBJECTIVE
Combine compatible query results and remove duplicate rows when required.

UNION combines result sets and removes duplicates. UNION ALL keeps duplicates and is often faster because it does not perform duplicate elimination. Both queries must return the same number of columns with compatible data types in corresponding positions. DISTINCT removes duplicate rows from a SELECT result.

Some database systems support INTERSECT and EXCEPT for common and differing rows. Support and exact syntax vary. Use set operations when the task is about combining result sets, and JOIN when the task is about relating columns across tables.

PRACTICE
Combine learner usernames from two course enrolment queries and compare UNION with UNION ALL.''','''SELECT username
FROM python_enrolments
UNION
SELECT username
FROM javascript_enrolments
ORDER BY username;

-- UNION ALL retains repeated usernames:
SELECT username FROM python_enrolments
UNION ALL
SELECT username FROM javascript_enrolments;'''),
('Views and reusable queries', '''LEARNING OBJECTIVE
Create a named database view for a query that is used repeatedly.

A view is a stored query definition that can be queried like a table. It can simplify complex joins and provide a controlled presentation of underlying data. A normal view generally stores the query, not a separate copy of its results; materialized views, where supported, store results and need refreshing.

A view is not automatically a security boundary. Permissions on the view and underlying tables depend on the database system and configuration. Avoid exposing columns that users should not see.

PRACTICE
Create a view that lists published courses with their lesson counts, then query that view.''','''CREATE VIEW published_course_summary AS
SELECT
  courses.id,
  courses.title,
  COUNT(lessons.id) AS lesson_count
FROM courses
LEFT JOIN lessons ON lessons.course_id = courses.id
WHERE courses.is_published = TRUE
GROUP BY courses.id, courses.title;

SELECT title, lesson_count
FROM published_course_summary
ORDER BY title;'''),
('Indexes and query performance', '''LEARNING OBJECTIVE
Understand how indexes support queries and how to inspect query performance.

An index is an additional data structure that helps the database locate rows without scanning every row in a table. Indexes are useful for frequently filtered, joined or sorted columns. Composite index column order matters because a query may benefit most when its conditions use the leading columns.

Indexes consume storage and add work to writes. Too many indexes can slow inserts and updates. Use EXPLAIN or the database's query-plan tool to inspect how a query is executed, and measure with representative data before changing production indexes.

PRACTICE
Inspect a query filtering enrolments by learner_id and decide whether an index would help. Compare the query plan before and after adding one in a test database.''','''-- Inspect the query plan (syntax varies by database):
EXPLAIN
SELECT course_id, enrolled_at
FROM enrolments
WHERE learner_id = 42
ORDER BY enrolled_at DESC;

-- A possible index for this access pattern:
CREATE INDEX idx_enrolments_learner_date
ON enrolments (learner_id, enrolled_at);'''),
('Database constraints and referential integrity', '''LEARNING OBJECTIVE
Use database rules to prevent invalid and inconsistent records.

A primary key uniquely identifies each row. A foreign key ensures a referenced row exists. UNIQUE prevents duplicate values, NOT NULL requires a value, and CHECK enforces a condition supported by the database engine. These constraints protect data even when several different applications write to the same database.

Choose ON DELETE and ON UPDATE actions carefully. CASCADE can be useful when child rows have no meaning without a parent, but it can also remove more data than expected. RESTRICT or NO ACTION can prevent accidental deletion of referenced records.

PRACTICE
Design a table for assessment results with a learner foreign key, a score range check and a unique attempt identifier.''','''CREATE TABLE assessment_results (
  id INTEGER PRIMARY KEY,
  learner_id INTEGER NOT NULL,
  score INTEGER NOT NULL CHECK (score BETWEEN 0 AND 100),
  attempt_code VARCHAR(64) NOT NULL UNIQUE,
  FOREIGN KEY (learner_id) REFERENCES learners(id)
    ON DELETE RESTRICT
);'''),
('Database security and parameterised queries', '''LEARNING OBJECTIVE
Understand how query parameters protect values and why database permissions matter.

Never build SQL by concatenating untrusted input into a query string. Use parameterised queries so the database driver treats values as data rather than SQL syntax. Placeholders differ between database drivers, so follow the API for the library you use.

Use a database account with only the permissions the application needs. Keep credentials out of source control, use secure connection settings and rotate credentials if they are exposed. Do not reveal database errors or sensitive records to ordinary users.

PRACTICE
Rewrite a query that searches for a username using a parameter placeholder rather than string concatenation.''','''-- Parameter placeholder style varies by driver.
-- Example with a named parameter in a database client:
SELECT id, username
FROM learners
WHERE username = :username;

-- Supply the value separately through the database driver's
-- parameter binding API. Do not concatenate it into the SQL text.'''),
],
}

ADDITIONAL_LESSONS.update(CORE_EXTRAS)
