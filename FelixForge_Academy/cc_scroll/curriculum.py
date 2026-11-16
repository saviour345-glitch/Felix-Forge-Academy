"""Expanded, teacher-written FelixForge Academy curriculum.
Each lesson contains an objective, explanation, worked example, code walkthrough,
common mistakes and a practice task. Examples are intentionally small and runnable.
"""

CURRICULUM = {
'javascript': [
('How the DOM represents a webpage', '''LEARNING OBJECTIVE
Understand what the Document Object Model (DOM) is and how JavaScript uses it to work with a webpage.

THE IDEA
When a browser loads HTML, it reads the markup and builds an in-memory tree of objects. This tree is called the DOM. Each element becomes a node: the html element contains head and body; body may contain headings, paragraphs, buttons and other elements. JavaScript does not normally edit the original HTML file. It asks the browser for DOM objects and changes those objects while the page is open.

WHY THIS MATTERS
The DOM is what makes a page interactive. A button can change a heading, a form can display a message, and a menu can open without loading a new page. The browser updates what the visitor sees after JavaScript changes the relevant DOM property.

WORKED EXAMPLE
Imagine the page contains <h1 id="title">Welcome</h1>. JavaScript can find that heading and change its text. The id is an identifier that lets the script target that particular element.

COMMON MISTAKES
• Confusing the DOM with the HTML source file. The DOM is the browser's live object representation.
• Running a script before the HTML element exists. Put the script near the end of body or wait for DOMContentLoaded.

PRACTICE
In a small HTML file, create a heading and a paragraph. Open the page, then use the browser console to inspect document.title and document.body.''', '''// HTML
<h1 id="title">Welcome</h1>
<p>We are learning the DOM.</p>

// JavaScript
const heading = document.querySelector('#title');
heading.textContent = 'Hello from JavaScript!';'''),
('Selecting elements safely', '''LEARNING OBJECTIVE
Select one or more page elements and understand what each selection method returns.

THE IDEA
Use document.querySelector(cssSelector) to return the first element matching a CSS selector. The selector follows familiar CSS rules: '#notice' selects an id, '.card' selects a class, and 'button' selects button elements. Use document.querySelectorAll(selector) when you need every match; it returns a NodeList that you can loop over.

STEP BY STEP
1. Choose a selector that identifies the element.
2. Ask the document for the element.
3. Check that the result exists before using it. A missing element produces null from querySelector.
4. For multiple matches, loop through the returned NodeList.

WHEN TO USE EACH
querySelector is convenient when an id or selector should identify one element. querySelectorAll is useful for lists of buttons, cards or navigation links. getElementById('name') is also available when selecting by id only; do not include the # in its argument.

COMMON MISTAKES
• Writing querySelector('title') when you meant '#title'. The first selects a title tag; the second selects an element whose id is title.
• Calling .textContent on null. Check the result first.

PRACTICE
Create three elements with class="topic" and use querySelectorAll to count them.''', '''const heading = document.querySelector('#page-title');
const topics = document.querySelectorAll('.topic');

if (heading) {
  heading.textContent = 'DOM selectors';
}

console.log(`Found ${topics.length} topics`);

topics.forEach((topic, index) => {
  console.log(index + 1, topic.textContent);
});'''),
('Changing text, HTML and styles', '''LEARNING OBJECTIVE
Update an element's content and appearance while choosing safe DOM properties.

TEXT CONTENT
textContent reads or replaces the text inside an element. It treats the supplied value as text, so characters such as < and > are displayed rather than interpreted as markup. This makes it a good default for text received from a user.

HTML CONTENT
innerHTML reads or replaces markup inside an element. It is useful when you intentionally need to create a small HTML structure, but inserting untrusted text with innerHTML can create a cross-site scripting (XSS) vulnerability. Prefer textContent for ordinary text.

STYLES AND CLASSES
You can set element.style.color for a one-off inline style. For reusable appearance changes, add or remove CSS classes with classList.add(), remove() and toggle(). Keep most design rules in CSS rather than writing many inline styles in JavaScript.

COMMON MISTAKES
• Using innerHTML for user-provided text.
• Replacing className and accidentally deleting classes that were already present. classList is usually safer.
• Forgetting CSS property names in JavaScript style objects use camelCase, such as backgroundColor.

PRACTICE
Make a button that toggles a 'highlight' class on a paragraph. Define the class in your CSS.''', '''const message = document.querySelector('#message');
const button = document.querySelector('#highlight-button');

message.textContent = 'Ready to learn';

button.addEventListener('click', () => {
  message.classList.toggle('highlight');
});

/* CSS */
.highlight {
  background: #fff3a3;
  padding: 0.5rem;
}'''),
('Events and event listeners', '''LEARNING OBJECTIVE
Respond to user actions such as clicks, typing, keyboard input and form submission.

THE IDEA
An event is something that happens in the browser. Examples include click, input, change, submit, keydown and mouseenter. addEventListener(eventName, callback) tells the browser which function to run when that event occurs. This is generally clearer and more flexible than writing onclick directly in HTML.

THE EVENT OBJECT
The callback can receive an event object. It contains useful information about the event. For a click, event.target is the element that originated the event. For a form submission, event.preventDefault() stops the browser's normal navigation or reload so JavaScript can validate or process the form.

EVENT FLOW
Events can travel through capture and bubbling phases. In bubbling, an event moves from the target element up through its ancestors. This enables event delegation: one listener on a parent can handle events from many child buttons.

COMMON MISTAKES
• Calling the function immediately: addEventListener('click', save()) runs save immediately. Pass save, not save().
• Adding the same listener repeatedly every time a page section is rendered.
• Forgetting preventDefault when handling a form entirely in JavaScript.

PRACTICE
Add a click listener to a counter button. Each click should increase a number displayed on the page.''', '''const button = document.querySelector('#count-button');
const output = document.querySelector('#count');
let count = 0;

button.addEventListener('click', (event) => {
  count += 1;
  output.textContent = count;
  console.log('Clicked:', event.type);
});'''),
('Forms, input and validation', '''LEARNING OBJECTIVE
Read form values, validate them and show helpful feedback without refreshing the page.

HOW FORMS WORK
A form groups controls such as input, select and textarea. Give each control a label. The input event fires as a value is edited; change generally fires when a value is committed. The submit event fires when the user submits the form. Listen for submit on the form rather than only the button, because users can submit with the keyboard too.

VALIDATION
HTML provides useful built-in constraints such as required, type="email", minlength and min/max. JavaScript can add rules that depend on your application. Validation should explain what needs correcting, not merely say 'invalid'. Always validate on the server too when data is sent to a backend; browser checks can be bypassed.

STEP BY STEP
1. Select the form and the fields.
2. Listen for submit.
3. Prevent the default page reload if handling it in JavaScript.
4. Read values from .value and trim unnecessary surrounding spaces.
5. Check the rules and display a message.

COMMON MISTAKES
• Reading input.value before the user has typed.
• Forgetting to trim whitespace.
• Treating front-end validation as security. Server-side validation is still required.

PRACTICE
Build a sign-up form that checks a username is at least three characters and displays a clear message.''', '''const form = document.querySelector('#signup-form');
const username = document.querySelector('#username');
const feedback = document.querySelector('#feedback');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const name = username.value.trim();

  if (name.length < 3) {
    feedback.textContent = 'Use at least 3 characters.';
    return;
  }

  feedback.textContent = `Welcome, ${name}!`;
});'''),
('Arrays and array methods', '''LEARNING OBJECTIVE
Store collections of values and transform them with common array methods.

THE IDEA
An array stores values in an ordered list. Its first index is 0, and its length property tells you how many items it contains. Arrays are useful for lists of lessons, products, scores or messages.

IMPORTANT METHODS
forEach runs a callback for each item and is useful for an action such as displaying or logging. map creates a new array by transforming every item. filter creates a new array containing items that pass a test. find returns the first matching item or undefined. includes checks whether a value exists. push adds an item to the end of the original array.

CHOOSING A METHOD
Use map when you need a transformed list, filter when you need a subset, and find when you need one matching item. Avoid changing an array while looping over it unless you understand how that affects the indexes.

COMMON MISTAKES
• Expecting map to change the original array. It returns a new array.
• Forgetting to return a value inside a map callback.
• Using forEach when you actually need the new array returned by map.

PRACTICE
Given an array of scores, create a new array containing only scores of 50 or higher, then create another array with 5 bonus points added.''', '''const scores = [42, 68, 91, 37, 75];

const passes = scores.filter(score => score >= 50);
const improved = passes.map(score => score + 5);

console.log(passes);   // [68, 91, 75]
console.log(improved); // [73, 96, 80]'''),
('Objects and working with data', '''LEARNING OBJECTIVE
Represent related information with objects and safely read, update and loop through properties.

THE IDEA
An object stores related data as key-value pairs. For example, a learner object can contain a name, course and completed lesson count. Read a property with dot notation when the property name is known, or bracket notation when it is stored in a variable or contains special characters.

UPDATING OBJECTS
Assigning to an existing property changes its value. You can add a property by assigning a new key. Object.keys returns an array of property names; Object.values returns values; Object.entries returns key-value pairs. These methods help inspect data received from an API.

NESTED DATA
An object can contain another object or an array. Read nested values carefully because an intermediate property may be missing. Optional chaining (?.) lets you safely access a nested property and returns undefined if the left side is null or undefined.

COMMON MISTAKES
• Using learner.name when learner may be null.
• Assuming every object has the same optional fields.
• Confusing an object property with a variable that has the same name.

PRACTICE
Create an object for a course with title, level and lessons. Add a completed property and print each key and value.''', '''const course = {
  title: 'JavaScript Foundations',
  level: 'Beginner',
  lessons: 12
};

course.completed = 4;
console.log(course.title);

for (const [key, value] of Object.entries(course)) {
  console.log(`${key}: ${value}`);
}'''),
('Local storage and saving preferences', '''LEARNING OBJECTIVE
Save small pieces of data in the browser so they remain after a page refresh.

WHAT LOCAL STORAGE IS
localStorage is a browser feature that stores key-value pairs as strings for a particular website origin. Data usually remains after the browser is closed and reopened. It is useful for preferences such as a theme or a small draft. It is not a database and should not be used for passwords, access tokens or sensitive personal information.

THE THREE MAIN OPERATIONS
setItem(key, value) saves a string. getItem(key) reads a string or returns null if the key does not exist. removeItem(key) deletes a key. To store an array or object, convert it to JSON with JSON.stringify and parse it with JSON.parse when reading.

ROBUSTNESS
Stored values may be missing or malformed. Provide a default and handle parsing errors. Browsers may also restrict storage in some privacy modes, so production applications should not assume it is guaranteed.

COMMON MISTAKES
• Expecting localStorage to store JavaScript objects directly. It stores strings.
• Forgetting JSON.parse when reading structured data.
• Storing confidential information in browser storage.

PRACTICE
Save a user's preferred theme and restore it when the page loads.''', '''// Save a preference
localStorage.setItem('theme', 'dark');

// Read it, with a fallback
const savedTheme = localStorage.getItem('theme') ?? 'light';
document.documentElement.dataset.theme = savedTheme;

// Remove it when needed
// localStorage.removeItem('theme');'''),
('Asynchronous JavaScript and promises', '''LEARNING OBJECTIVE
Explain why some operations finish later and use promises with async and await.

SYNCHRONOUS VS ASYNCHRONOUS
Normal synchronous statements run in order. Some tasks, such as requesting data from a server or waiting for a timer, take time. The browser allows other work to continue instead of freezing the page while waiting. A promise represents a value that may become available later. It can be pending, fulfilled or rejected.

ASYNC AND AWAIT
An async function always returns a promise. Inside it, await pauses that function until a promise settles; it does not freeze the entire browser. Use try/catch to handle failures. This style often makes asynchronous code easier to read than long chains of callbacks.

ERROR HANDLING
A request can fail because of a network problem, a missing resource or a server error. Handle these cases and give the user a useful message. Do not assume a promise always succeeds.

COMMON MISTAKES
• Forgetting await and trying to use a promise as if it were the final data.
• Forgetting try/catch around an awaited operation.
• Thinking await blocks every other task in the browser.

PRACTICE
Write an async function that waits for a promise and displays either its result or an error message.''', '''function waitForMessage() {
  return new Promise(resolve => {
    setTimeout(() => resolve('Finished waiting!'), 1000);
  });
}

async function showMessage() {
  try {
    const message = await waitForMessage();
    console.log(message);
  } catch (error) {
    console.error('Something went wrong:', error);
  }
}

showMessage();'''),
('Fetch API: requesting data', '''LEARNING OBJECTIVE
Request data from an HTTP endpoint, check the response and convert JSON into JavaScript values.

THE FETCH PROCESS
fetch(url) starts an HTTP request and returns a promise. When the response arrives, check response.ok because HTTP errors such as 404 do not automatically reject the fetch promise. Then call response.json() to parse a JSON response; that operation is asynchronous too, so await it.

DISPLAYING RESULTS
After receiving data, update the DOM using textContent or create elements safely. If the response contains a list, loop over it and build a list of visible results. Always show a loading state and a helpful error state so the page does not appear broken while waiting.

SECURITY AND PRIVACY
Only request data from services you are authorised to use. Do not place private API keys in front-end JavaScript; browser code is visible to visitors. A trusted backend should hold secrets and make protected requests.

COMMON MISTAKES
• Not checking response.ok.
• Forgetting that response.json() returns a promise.
• Inserting untrusted API text with innerHTML.

PRACTICE
Use a public demo API to fetch a list of posts and display their titles. Add a message for loading and failure.''', '''async function loadPosts() {
  const output = document.querySelector('#posts');
  output.textContent = 'Loading posts...';

  try {
    const response = await fetch('https://jsonplaceholder.typicode.com/posts');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const posts = await response.json();
    output.textContent = posts.slice(0, 5)
      .map(post => post.title)
      .join('\\n');
  } catch (error) {
    output.textContent = 'Could not load posts. Please try again.';
    console.error(error);
  }
}

loadPosts();'''),
('Modules and organising a project', '''LEARNING OBJECTIVE
Split JavaScript into reusable files with export and import.

WHY MODULES HELP
A small experiment can live in one file. As an application grows, one file becomes difficult to navigate and test. Modules let you group related functions and values into separate files. Each module has its own scope, which reduces accidental global variables.

EXPORTING
Use export before a declaration to make it available to other modules. A module can have named exports and one default export. Named imports use the exact exported name inside braces. A default import can choose a local name.

IMPORTING IN THE BROWSER
Load the entry file with <script type="module" src="main.js"></script>. Module scripts are deferred automatically and use strict mode. When testing locally, use a development server rather than opening the HTML file directly, because browsers restrict module loading from file URLs.

COMMON MISTAKES
• Forgetting type="module" on the script element.
• Using the wrong relative path in an import.
• Mixing up named and default exports.

PRACTICE
Move a calculateTotal function into a separate file, export it, then import and call it from main.js.''', '''// math.js
export function calculateTotal(price, quantity) {
  return price * quantity;
}

// main.js
import { calculateTotal } from './math.js';
console.log(calculateTotal(250, 3));

// index.html
// <script type="module" src="main.js"></script>'''),
],
'python': [
('How Python runs a program', '''LEARNING OBJECTIVE
Understand what a Python program is, how statements execute and how to display output.

THE IDEA
Python is a general-purpose programming language. A Python source file usually ends in .py. The Python interpreter reads and executes the statements in that file. Most simple statements run from top to bottom, although functions, conditions and loops can change the flow.

OUTPUT WITH PRINT
print() displays information in the terminal. You can pass text, numbers and multiple values. Text is written inside quotation marks. A string is a sequence of characters; an integer is a whole number; a float represents a number with a decimal part.

READING AN ERROR
If Python cannot understand a statement, it may raise a SyntaxError. If the syntax is valid but an operation cannot be completed, it may raise another exception such as NameError or TypeError. Read the final line of a traceback first, then use the line number to inspect the code.

COMMON MISTAKES
• Missing quotation marks around text.
• Using print = ... and accidentally replacing the built-in print name.
• Expecting print to save data permanently; it only displays output.

PRACTICE
Create a file named introduction.py that prints your chosen display name, a subject you are studying and one goal for learning programming.''', '''print("Welcome to FelixForge Academy")
print("Python is a programming language")

name = "Ada"
subject = "Computer Science"
print("Learner:", name)
print("Subject:", subject)'''),
('Variables, types and conversion', '''LEARNING OBJECTIVE
Store values in variables, identify common built-in types and convert between types safely.

VARIABLES
A variable is a name that refers to a value. Assignment uses =. Python does not require you to declare a variable's type first. The type belongs to the value, and you can inspect it with type(). Choose meaningful names such as total_price rather than vague names such as x when the meaning matters.

COMMON TYPES
str stores text, int stores whole numbers, float stores decimal numbers, and bool stores True or False. A list stores an ordered, changeable collection. A dictionary stores key-value pairs.

CONVERSION
input() always returns text. If you need a number, convert it with int() or float(). Conversion can fail when the input is not a valid number, so real programs should handle ValueError.

COMMON MISTAKES
• Adding a string to an integer without conversion.
• Naming variables with spaces or starting a name with a number.
• Using a variable before assigning it.

PRACTICE
Ask for the price and quantity of an item, convert both to numbers and calculate the total.''', '''item = "Notebook"
price = 850.50
quantity = 3
in_stock = True

total = price * quantity
print(f"{quantity} {item}(s) cost ₦{total:,.2f}")
print(type(price))'''),
('Decisions with if, elif and else', '''LEARNING OBJECTIVE
Make a program choose different actions based on conditions.

BOOLEAN CONDITIONS
A condition is an expression that evaluates to True or False. Comparison operators include ==, !=, <, >, <= and >=. The equality operator is ==; a single = assigns a value. Combine conditions with and, or and not.

BRANCHING
An if block runs when its condition is true. elif checks another condition if earlier conditions were false. else runs when none of the earlier conditions matched. Indentation is part of Python syntax: statements belonging to a block must be indented consistently.

ORDER MATTERS
Python checks conditions from top to bottom and executes the first matching branch. Put more specific conditions before broader ones. For example, test for a distinction before testing for a general pass.

COMMON MISTAKES
• Writing if score = 50 instead of if score == 50.
• Forgetting the colon at the end of if, elif or else.
• Using inconsistent indentation.

PRACTICE
Ask for a test score and print a grade category. Decide how your program should handle values below 0 or above 100.''', '''score = 76

if score < 0 or score > 100:
    print("Score must be between 0 and 100")
elif score >= 70:
    print("Excellent")
elif score >= 50:
    print("Pass")
else:
    print("Needs more practice")'''),
('Loops: for and while', '''LEARNING OBJECTIVE
Repeat instructions with for and while loops and avoid infinite loops.

FOR LOOPS
A for loop visits each item in an iterable such as a list, string or range. range(1, 6) produces 1, 2, 3, 4 and 5; the stop value is excluded. A loop variable receives the next item on each iteration.

WHILE LOOPS
A while loop repeats as long as its condition remains true. It is useful when the number of repetitions is not known in advance, such as repeatedly asking until the user enters a valid response. Something inside the loop should eventually make the condition false.

CONTROL STATEMENTS
break exits the nearest loop. continue skips the rest of the current iteration and proceeds to the next one. Use these carefully so the loop remains understandable.

COMMON MISTAKES
• Creating an infinite while loop by never changing the condition.
• Expecting range(1, 5) to include 5.
• Accidentally changing the loop variable in a way that skips items.

PRACTICE
Use a for loop to add numbers from 1 to 100. Then use a while loop to ask for a password until a non-empty response is entered; do not use a real password.''', '''total = 0
for number in range(1, 101):
    total += number
print("Sum:", total)

attempts = 0
while attempts < 3:
    answer = input("Enter a practice word: ").strip()
    if answer:
        print("You entered:", answer)
        break
    attempts += 1'''),
('Functions, parameters and return values', '''LEARNING OBJECTIVE
Write reusable functions, pass information into them and return results.

WHY FUNCTIONS MATTER
A function gives a name to a reusable block of code. It helps divide a larger problem into smaller tasks, reduces repetition and makes code easier to test. Define a function with def, followed by its name, parentheses and a colon.

PARAMETERS AND ARGUMENTS
A parameter is a name in the function definition. An argument is the actual value supplied when calling the function. A function can have multiple parameters and default values. Use return to send a result back to the caller. print displays a value; return makes it available to the rest of the program.

SCOPE
A variable created inside a function is normally local to that function. Pass required information through parameters instead of depending on many global variables. This makes functions easier to understand.

COMMON MISTAKES
• Printing a result when the caller needs a returned value.
• Forgetting to call the function after defining it.
• Using a variable that only exists inside another function.

PRACTICE
Write a function that accepts a unit price and quantity and returns the total. Test it with at least three different inputs.''', '''def calculate_total(unit_price, quantity):
    """Return the cost of a given quantity."""
    return unit_price * quantity

bill = calculate_total(850, 3)
print(f"Total: ₦{bill:,.2f}")'''),
('Lists and dictionaries', '''LEARNING OBJECTIVE
Choose between lists and dictionaries to organise related information.

LISTS
A list stores items in order and can be changed. Access items by index, starting at zero. append adds one item, remove deletes a matching value, and len returns the number of items. A list can contain values of different types, though keeping a consistent type often makes programs easier to reason about.

DICTIONARIES
A dictionary maps keys to values. Use it when each value has a label, such as a student's name and score. Read a value with dictionary[key] or use get(key, default) when the key may be missing. Keys must be hashable and are commonly strings or numbers.

NESTED STRUCTURES
A list can contain dictionaries, which is useful for representing a collection of records. You can loop through each record and read its fields.

COMMON MISTAKES
• Using an index that is outside the list's range.
• Accessing a missing dictionary key without checking.
• Confusing append (one item) with extend (items from another iterable).

PRACTICE
Create a list of three learners, each represented by a dictionary containing name and score. Print learners whose score is at least 50.''', '''learners = [
    {"name": "Ada", "score": 84},
    {"name": "Sam", "score": 46},
    {"name": "Tomi", "score": 72},
]

for learner in learners:
    if learner["score"] >= 50:
        print(learner["name"], "passed")'''),
('Errors, exceptions and debugging', '''LEARNING OBJECTIVE
Recognise common Python errors and handle expected failures without hiding bugs.

ERROR CATEGORIES
Syntax errors mean Python cannot parse the code. Runtime exceptions happen while the program is running. Logic errors happen when the program runs but produces the wrong result. Debugging means finding the cause, not merely changing code until the error disappears.

TRY AND EXCEPT
Use try around an operation that may reasonably fail, such as converting user input to a number. Use except to handle a specific exception and explain what the user can do next. Avoid a bare except that catches everything; it can hide programming mistakes. An optional else block runs when no exception occurs, and finally runs whether an exception happened or not.

A DEBUGGING ROUTINE
Read the traceback, identify the file and line, inspect the values involved, reproduce the problem with a small input, and test the fix. Temporary print statements can help reveal what a variable contains.

COMMON MISTAKES
• Catching Exception everywhere and silently continuing.
• Showing technical tracebacks to ordinary users.
• Fixing the symptom without checking the cause.

PRACTICE
Ask for a number and handle the case where the user enters letters instead.''', '''try:
    age = int(input("Enter a practice age: "))
except ValueError:
    print("Please enter a whole number, such as 16.")
else:
    print("Next year you will be", age + 1)
finally:
    print("Program finished.")'''),
],
'html': [
('HTML document structure and semantics', '''LEARNING OBJECTIVE
Build a valid HTML document and choose elements according to their meaning.

WHAT HTML DOES
HTML (HyperText Markup Language) describes the structure and meaning of webpage content. It is not a programming language: it marks content such as headings, paragraphs, navigation, images and forms. The browser parses the elements and builds the DOM.

DOCUMENT PARTS
<!doctype html> tells the browser to use modern standards mode. The html element is the root; lang identifies the page language. head contains metadata, the title and links to stylesheets. body contains the visible page content. UTF-8 supports a wide range of characters.

SEMANTIC ELEMENTS
Use header for introductory content, nav for major navigation, main for the page's primary content, section for a thematic group, article for a self-contained item and footer for closing information. Use headings in a logical hierarchy. Semantic HTML helps assistive technology and makes code easier to maintain.

COMMON MISTAKES
• Putting visible page content inside head.
• Using headings only because of their default size.
• Forgetting lang or the viewport metadata needed for mobile layouts.

PRACTICE
Create a personal learning page with a header, navigation, main section containing two articles, and a footer.''', '''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Learning Page</title>
</head>
<body>
  <header><h1>My Learning Page</h1></header>
  <nav><a href="#topics">Topics</a></nav>
  <main id="topics">
    <article><h2>HTML</h2><p>Page structure.</p></article>
    <article><h2>CSS</h2><p>Page presentation.</p></article>
  </main>
  <footer>Keep learning.</footer>
</body>
</html>'''),
('Text, links, images and lists', '''LEARNING OBJECTIVE
Present readable text, create links, describe images and organise related items.

TEXT ELEMENTS
Use h1–h6 for headings according to document structure, not merely visual size. Use p for paragraphs, strong for important emphasis and em for stress emphasis. Browsers provide default styles, but CSS controls presentation.

LINKS
The a element creates a hyperlink. href gives its destination. Use meaningful link text such as 'Read the HTML guide' instead of 'click here'. For links that open a new tab, consider rel="noopener" when using target="_blank".

IMAGES
The img element embeds an image. src identifies the file or URL. alt provides a text alternative: describe the information the image contributes. If an image is purely decorative, use alt="". Do not write 'image of' automatically; describe the useful content.

LISTS
Use ul for an unordered list and ol when order matters. Each item belongs in li. Do not use repeated br elements to imitate a list.

PRACTICE
Create a list of three learning goals, add a link to a documentation page and include an image with useful alternative text.''', '''<h2>Learning goals</h2>
<ul>
  <li>Understand semantic HTML</li>
  <li>Practise CSS layouts</li>
  <li>Build an interactive page</li>
</ul>

<p><a href="https://developer.mozilla.org/en-US/docs/Web/HTML">
  Read the HTML documentation
</a></p>

<img src="classroom.jpg" alt="Learners working together at a computer">'''),
('Forms and accessible labels', '''LEARNING OBJECTIVE
Create forms with correctly labelled controls and appropriate input types.

FORM BASICS
A form groups controls for collecting information. label associates text with a control. The for attribute must match the control's id. This association makes the control easier to use with a mouse, keyboard and assistive technology. A placeholder is a hint, not a replacement for a label.

INPUT TYPES
Use email for email addresses, number for numeric values, password for secret entry, date for dates and checkbox for independent choices. Choose the most suitable type so browsers can provide appropriate keyboards and basic validation.

NAME AND SUBMISSION
The name attribute identifies a field in submitted form data. A submit button submits the form. required marks a field as mandatory, but server-side validation is still necessary. The browser's built-in validation improves usability; it does not prove that submitted data is trustworthy.

COMMON MISTAKES
• Using placeholder as the only label.
• Reusing the same id on multiple elements.
• Assuming required prevents all invalid or malicious requests.

PRACTICE
Build a contact form with name, email, message and a submit button. Label every control.''', '''<form action="/contact" method="post">
  <label for="name">Your name</label>
  <input id="name" name="name" required minlength="2">

  <label for="email">Email address</label>
  <input id="email" name="email" type="email" required>

  <label for="message">Message</label>
  <textarea id="message" name="message" required></textarea>

  <button type="submit">Send message</button>
</form>'''),
('Tables and data relationships', '''LEARNING OBJECTIVE
Use HTML tables for genuine tabular data and make their structure understandable.

WHEN TO USE A TABLE
Tables are appropriate when information has row-and-column relationships, such as a timetable, price list or results sheet. They should not be used to arrange the overall layout of a webpage; CSS Grid and Flexbox are designed for that.

TABLE STRUCTURE
Use table as the container, caption to describe the table, thead for headings, tbody for data rows and tfoot for a summary when needed. Use th for header cells and td for data cells. The scope attribute can identify whether a header applies to a row or column.

ACCESSIBILITY
A clear caption and correctly marked headers help people understand the relationship between cells. Keep tables simple where possible. On narrow screens, place a wide table in a horizontally scrollable wrapper rather than forcing text to become unreadable.

COMMON MISTAKES
• Using td for every cell, including headings.
• Using a table for page layout.
• Leaving out context that explains what the numbers mean.

PRACTICE
Create a table showing three courses, their duration and difficulty. Add a caption and column headings.''', '''<table>
  <caption>Course overview</caption>
  <thead>
    <tr><th scope="col">Course</th><th scope="col">Weeks</th><th scope="col">Level</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">HTML</th><td>3</td><td>Beginner</td></tr>
    <tr><th scope="row">CSS</th><td>4</td><td>Beginner</td></tr>
    <tr><th scope="row">JavaScript</th><td>8</td><td>Beginner</td></tr>
  </tbody>
</table>'''),
('Accessibility foundations', '''LEARNING OBJECTIVE
Make pages easier to use with keyboards, screen readers and different viewing needs.

ACCESSIBILITY IS PART OF GOOD HTML
Accessibility means people with different abilities can perceive, understand and operate your website. Start with semantic HTML: headings, buttons, links, labels and landmarks already communicate meaning to browsers and assistive technology.

KEYBOARD SUPPORT
Every interactive feature should be usable without a mouse. Native buttons and links are keyboard accessible by default. Avoid clickable div elements when a button is the correct control. Keep focus visible so users can tell which element is active.

IMAGES AND FORMS
Write useful alt text for informative images. Associate labels with form controls. Give buttons names that explain their action. Do not rely on colour alone to communicate success or error; include text or another cue.

TESTING
Try navigating with Tab and Shift+Tab. Check heading order and labels. Test at different zoom levels. Automated tools can find some problems, but they cannot judge every real user experience.

PRACTICE
Review a page you built and make sure every control has a clear name and can be reached with the keyboard.''', '''<button type="button" aria-expanded="false" aria-controls="details">
  Show details
</button>
<div id="details" hidden>
  More information appears here.
</div>

<!-- Use a real button for an action.
     JavaScript should update aria-expanded
     and the hidden state when toggled. -->'''),
],
'css': [
('How CSS rules work', '''LEARNING OBJECTIVE
Understand the structure of a CSS rule and connect a stylesheet to an HTML document.

THE IDEA
CSS (Cascading Style Sheets) controls how HTML content is presented. A rule contains a selector and a declaration block. The selector chooses elements; declarations contain a property and value. For example, color is a property and navy is its value.

ADDING CSS
External stylesheets are usually best for real projects. Save rules in a .css file and connect it with a link element in head. Internal styles can be placed in a style element, while inline styles belong on individual elements. External files make it easier to reuse and maintain design rules.

THE CASCADE
When multiple rules target the same element, the browser resolves conflicts using origin, importance, specificity and source order. A more specific selector can override a less specific one. Avoid solving every conflict with !important; that makes future changes harder.

COMMON MISTAKES
• Missing a semicolon between declarations.
• Writing a property that does not exist.
• Linking the stylesheet with an incorrect path.

PRACTICE
Create an external stylesheet that sets the page font, background colour and heading colour.''', '''/* styles.css */
body {
  font-family: Arial, sans-serif;
  background-color: #f4f6fb;
  color: #202638;
}

h1 {
  color: #2457c5;
}

/* In HTML head:
<link rel="stylesheet" href="styles.css">
*/'''),
('Selectors, specificity and inheritance', '''LEARNING OBJECTIVE
Target elements precisely and predict which CSS declaration wins.

COMMON SELECTORS
A type selector targets elements by tag name, such as p. A class selector begins with a dot, such as .card. An id selector begins with #. A descendant selector such as .menu a selects links inside an element with class menu. Attribute selectors can target elements based on attributes, for example input[type="email"].

SPECIFICITY
When competing declarations have the same origin and importance, specificity helps determine the winner. An id selector is more specific than a class selector, which is more specific than a type selector. If specificity is equal, the later rule generally wins. Prefer simple, reusable classes instead of deeply nested selectors.

INHERITANCE
Some properties, such as color and font-family, are inherited by descendants. Others, such as margin and border, are not inherited by default. The inherit, initial and unset keywords can influence this behaviour.

COMMON MISTAKES
• Using IDs for every style, making overrides difficult.
• Assuming all CSS properties inherit.
• Adding long selector chains unnecessarily.

PRACTICE
Style cards using a class, then style links inside a card without changing links elsewhere.''', '''.card {
  color: #253047;
  border: 1px solid #d9deea;
}

.card a {
  color: #2457c5;
}

input[type="email"] {
  border-color: #7b8aa8;
}'''),
('The box model and sizing', '''LEARNING OBJECTIVE
Calculate how content, padding, borders and margins affect an element's size.

THE FOUR LAYERS
The content box contains text or other content. Padding adds space between the content and border. The border surrounds padding and content. Margin creates space outside the border between neighbouring elements.

WIDTH CALCULATION
With the default content-box model, a declared width applies only to the content. The rendered outer width is content width plus left and right padding plus borders; margins add external spacing. This can make layouts wider than expected.

BOX-SIZING
The common rule box-sizing: border-box makes the declared width include content, padding and border. Applying it to all elements makes layout calculations more predictable. Margin remains outside the declared width.

COMMON MISTAKES
• Forgetting that padding adds to width under content-box.
• Using large margins to fix a problem caused by incorrect sizing.
• Confusing padding (inside) with margin (outside).

PRACTICE
Create two cards with the same declared width. Give one content-box and one border-box, then compare their rendered sizes in browser developer tools.''', '''* {
  box-sizing: border-box;
}

.card {
  width: 320px;
  padding: 20px;
  border: 2px solid #334155;
  margin: 16px;
}'''),
('Flexbox for one-dimensional layouts', '''LEARNING OBJECTIVE
Arrange items in a row or column and control alignment and spacing with Flexbox.

WHEN FLEXBOX HELPS
Flexbox is designed for arranging items along one main axis. It is useful for navigation bars, button groups, toolbars and card rows. Set display: flex on the parent; its direct children become flex items.

MAIN AXIS AND CROSS AXIS
flex-direction chooses the main axis: row or column. justify-content distributes items along the main axis. align-items aligns them on the cross axis. gap adds space between items without needing margins on each child. flex-wrap allows items to move onto another line when space is limited.

FLEXIBLE SIZING
flex-grow controls how extra space is distributed. flex-shrink controls how items shrink when space is tight. flex-basis sets an initial main size. The shorthand flex combines these ideas; start with simple values before using complex combinations.

COMMON MISTAKES
• Applying display:flex to the child instead of the parent.
• Mixing up justify-content and align-items after changing flex-direction.
• Expecting gap to add space around the outside of the container.

PRACTICE
Build a responsive navigation row that wraps on narrow screens and keeps equal spacing between links.''', '''.navigation {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.navigation a {
  padding: 0.5rem 0.75rem;
}'''),
('CSS Grid for two-dimensional layouts', '''LEARNING OBJECTIVE
Create rows and columns for page layouts using CSS Grid.

GRID CONCEPTS
Grid is designed for two-dimensional layouts where rows and columns work together. Apply display: grid to a container. grid-template-columns defines the columns; grid-template-rows defines rows. gap creates spacing between tracks.

RESPONSIVE COLUMNS
The repeat() function avoids repeating the same track definition. minmax() defines a minimum and maximum track size. The auto-fit keyword can create as many columns as fit in the available space. This is useful for responsive card galleries.

PLACING ITEMS
Grid items can span multiple columns or rows. Start with automatic placement and add explicit placement only when the design needs it. Use meaningful class names so the layout remains readable.

WHEN TO USE GRID OR FLEXBOX
Use Grid when you need rows and columns together. Use Flexbox when arranging items along one axis. They can be combined: a grid page layout may contain a flex navigation bar.

PRACTICE
Build a card gallery that automatically changes from several columns to fewer columns as the viewport narrows.''', '''.card-grid {
  display: grid;
  grid-template-columns: repeat(
    auto-fit,
    minmax(220px, 1fr)
  );
  gap: 1rem;
}

.card {
  padding: 1.25rem;
  border-radius: 12px;
  border: 1px solid #d8deea;
}'''),
('Responsive design and media queries', '''LEARNING OBJECTIVE
Make layouts adapt to different screen widths without building a separate site for every device.

RESPONSIVE THINKING
A responsive page adjusts its layout to the available space. Start with a flexible layout and content that can wrap. Use relative units such as %, rem and fr where appropriate. Images should usually have max-width: 100% so they do not overflow their containers.

MEDIA QUERIES
A media query applies CSS only when a condition matches, such as a minimum or maximum viewport width. Choose breakpoints based on where your content becomes cramped, not because a particular phone model exists. Mobile-first CSS starts with the simplest narrow layout and adds enhancements for wider screens.

VIEWPORT META
Include the viewport meta element in HTML so mobile browsers use the device width. Without it, a page may be laid out as though it were much wider than the actual screen.

COMMON MISTAKES
• Using fixed widths that force horizontal scrolling.
• Setting breakpoints for device names instead of content needs.
• Forgetting to test keyboard navigation and zoom after changing layout.

PRACTICE
Make a two-column page become one column on narrow screens. Test by resizing the browser.''', '''.page {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

img {
  max-width: 100%;
  height: auto;
}

@media (max-width: 700px) {
  .page {
    grid-template-columns: 1fr;
  }
}'''),
],
'sql': [
('Tables, rows and data types', '''LEARNING OBJECTIVE
Understand how relational databases organise information into tables.

THE RELATIONAL MODEL
A relational database stores data in tables. A table has columns that describe attributes and rows that represent records. Each column has a data type, such as integer, text, date or decimal. A primary key uniquely identifies a row. A foreign key refers to a key in another table and helps represent relationships.

DESIGN BASICS
Choose a primary key that is stable and unique. Avoid storing several unrelated values in one column. For example, keep a learner's profile in a learners table and individual quiz attempts in a quiz_results table. A learner can have many results, so quiz_results can store learner_id as a foreign key.

NULL
NULL means a value is missing or unknown; it is not the same as zero or an empty string. Use IS NULL to test for it, not = NULL.

PRACTICE
Design two related tables for courses and lessons. Identify a primary key for each and a foreign key connecting lessons to courses.''', '''CREATE TABLE courses (
  id INTEGER PRIMARY KEY,
  title VARCHAR(100) NOT NULL
);

CREATE TABLE lessons (
  id INTEGER PRIMARY KEY,
  course_id INTEGER NOT NULL,
  title VARCHAR(120) NOT NULL,
  FOREIGN KEY (course_id) REFERENCES courses(id)
);'''),
('SELECT, WHERE and sorting', '''LEARNING OBJECTIVE
Retrieve selected columns, filter rows and sort query results.

SELECT
SELECT names the columns you want to retrieve. FROM identifies the table. Use * to request every column while exploring, but list the columns explicitly in application queries so the result is predictable.

FILTERING
WHERE keeps rows that satisfy a condition. Comparison operators include =, <>, <, >, <= and >=. Combine conditions with AND and OR. Use IN for a list of possible values, BETWEEN for a range and LIKE for a pattern. In many SQL systems, % represents any sequence of characters in a LIKE pattern.

SORTING AND LIMITING
ORDER BY sorts results. ASC is ascending and DESC is descending. LIMIT restricts how many rows are returned in databases that support it. Without ORDER BY, row order is not guaranteed.

COMMON MISTAKES
• Using = NULL instead of IS NULL.
• Forgetting quotes around text values.
• Assuming records are returned in insertion order.

PRACTICE
Write a query that selects learner names and scores for scores of 70 or above, ordered from highest score to lowest.''', '''SELECT name, score
FROM learners
WHERE score >= 70
ORDER BY score DESC;

-- Find names that begin with A
SELECT name
FROM learners
WHERE name LIKE 'A%';'''),
('INSERT, UPDATE and DELETE', '''LEARNING OBJECTIVE
Add, change and remove records while understanding how to avoid accidental data loss.

INSERT
INSERT INTO adds a new row. You should name the columns you are inserting into; this makes the statement clearer and less fragile if the table changes. Values must match the columns' data types and constraints.

UPDATE
UPDATE changes existing rows. SET lists the new values. WHERE chooses which rows to change. Without a WHERE clause, every row in the table may be updated.

DELETE
DELETE removes rows. It also uses WHERE to identify which records should be removed. Before running a destructive statement, write and test a SELECT with the same WHERE condition to confirm the target rows.

SAFER WORKFLOW
For important changes, use a transaction where supported: begin, inspect, make the change, verify, then commit. If something is wrong before commit, roll back. Use parameterised queries from application code rather than building SQL by concatenating user input.

PRACTICE
Insert a learner, update that learner's score using a unique id, then write (but do not run) a DELETE statement that would remove only that learner.''', '''INSERT INTO learners (id, name, score)
VALUES (101, 'Ada', 84);

UPDATE learners
SET score = 90
WHERE id = 101;

-- Check the target first:
SELECT * FROM learners WHERE id = 101;

-- Then, only if appropriate:
-- DELETE FROM learners WHERE id = 101;'''),
('JOIN: combining related tables', '''LEARNING OBJECTIVE
Combine information from related tables using primary and foreign keys.

WHY JOIN EXISTS
Related information is often stored in separate tables to avoid unnecessary duplication. A lessons table may store course_id rather than repeating the course title in every lesson row. JOIN combines rows using a relationship between columns.

INNER JOIN
INNER JOIN returns rows where the join condition matches in both tables. LEFT JOIN returns every row from the left table and matching rows from the right; missing matches appear as NULL. Choose the join type according to whether unmatched records should remain in the result.

ALIASES
Short aliases make queries easier to read. If both tables have a column named id, qualify it with the table alias to avoid ambiguity. Always write the join condition carefully; a missing or incorrect condition can create many unintended row combinations.

PRACTICE
Given learners(id, name) and results(learner_id, score), write a query that lists each learner's name and their score.''', '''SELECT
  l.name,
  r.score
FROM learners AS l
INNER JOIN results AS r
  ON r.learner_id = l.id
ORDER BY l.name;'''),
('Aggregate functions and grouping', '''LEARNING OBJECTIVE
Summarise rows with COUNT, SUM, AVG, MIN and MAX, then group results.

AGGREGATES
COUNT counts rows or non-NULL values, depending on the expression. SUM adds numeric values. AVG calculates an average. MIN and MAX return the smallest and largest values. These functions turn many records into a summary.

GROUP BY
GROUP BY creates one result group for each distinct value or combination of values. For example, group quiz results by course to calculate the average score for each course. Columns in the SELECT list generally need to be grouped or aggregated, subject to the database system's rules.

HAVING VS WHERE
WHERE filters individual rows before grouping. HAVING filters groups after aggregation. Use WHERE to exclude rows before calculating a group summary and HAVING to keep only groups whose aggregate meets a condition.

PRACTICE
Calculate the average score for each course and show only courses with at least five results.''', '''SELECT
  course_id,
  COUNT(*) AS result_count,
  AVG(score) AS average_score
FROM quiz_results
GROUP BY course_id
HAVING COUNT(*) >= 5
ORDER BY average_score DESC;'''),
],
}

# Additional tracks receive real language-specific foundations rather than a shared placeholder.
EXTRA_TRACKS = {
'c': ('C', 'int main(void) {\n    printf("Hello, world!\\n");\n    return 0;\n}', 'stdio.h', 'C uses explicit types, compiled source files and manual control over memory. Compile with a C compiler such as GCC.'),
'cpp': ('C++', '#include <iostream>\nint main() {\n    std::cout << "Hello, world!\\n";\n}', 'iostream', 'C++ supports procedural, object-oriented and generic programming. Modern C++ encourages standard-library containers and resource-safe design.'),
'java': ('Java', 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, world!");\n    }\n}', 'Main', 'Java is a statically typed, class-based language. The Java compiler produces bytecode that runs on the Java Virtual Machine.'),
'csharp': ('C#', 'Console.WriteLine("Hello, world!");', 'Console', 'C# is a statically typed language commonly used with .NET for desktop, web, cloud and game development.'),
'php': ('PHP', '<?php\n$name = "Ada";\necho "Hello, $name!";\n?>', 'PHP', 'PHP commonly runs on a server to generate responses and work with databases. Keep validation and secrets on the server.'),
'typescript': ('TypeScript', 'type Learner = { name: string; score: number };\nconst learner: Learner = { name: "Ada", score: 84 };\nconsole.log(learner.name);', 'Learner', 'TypeScript adds a static type system to JavaScript and is compiled to JavaScript for execution.'),
'go': ('Go', 'package main\nimport "fmt"\nfunc main() {\n    fmt.Println("Hello, world!")\n}', 'fmt', 'Go is a compiled language with built-in support for concurrency and a deliberately small core language.'),
'rust': ('Rust', 'fn main() {\n    let message = String::from("Hello, world!");\n    println!("{}", message);\n}', 'String', 'Rust uses ownership and borrowing rules to help prevent memory-safety errors without a garbage collector.'),
'ruby': ('Ruby', 'name = "Ada"\nputs "Hello, #{name}!"', 'puts', 'Ruby is a dynamically typed language with expressive syntax and a strong tradition of readable code.'),
'swift': ('Swift', 'let name = "Ada"\nprint("Hello, \\(name)!")', 'let', 'Swift is a strongly typed language used across Apple platforms and supports optionals for values that may be absent.'),
'kotlin': ('Kotlin', 'fun main() {\n    val name = "Ada"\n    println("Hello, $name!")\n}', 'fun', 'Kotlin is a statically typed language with concise syntax and strong interoperability with Java.'),
}

EXTRA_LESSON_TITLES = ['Program structure and first output', 'Variables, types and expressions', 'Decisions and repetition', 'Functions and reusable code', 'Collections and practical problem solving']

def build_extra_lessons(slug):
    language, code, concept, overview = EXTRA_TRACKS[slug]
    snippets = [
        code,
        f'// {language} values and types\n// Create a value, inspect its type, and use it in an expression.\n// Example concept: {concept}',
        f'// {language} control flow\n// Write a condition that checks a value, then repeat a task\n// with the language\'s loop construct.',
        f'// {language} functions\n// Define a function that accepts two values and returns a result.\n// Call it with at least two different argument sets.',
        f'// {language} collections\n// Store several values, loop through them, and calculate a summary.'
    ]
    bodies = [
        f'''LEARNING OBJECTIVE\nRun a minimal {language} program and identify its entry point.\n\nTHE IDEA\n{overview} A program is a sequence of instructions. Source code is written in a text file using the language's syntax, then interpreted or compiled according to its runtime. The first example displays a short message so you can confirm that the environment is working.\n\nHOW TO STUDY THIS EXAMPLE\nRead the code from top to bottom. Identify imports or declarations, the entry point, the output statement and the end of the program. Change the message and run it again. Small controlled changes help you connect syntax to behaviour.\n\nCOMMON MISTAKES\nCheck file names, capitalization, punctuation and the compiler or interpreter command. Many languages treat uppercase and lowercase names as different identifiers.\n\nPRACTICE\nChange the output to display two separate lines: the language name and one reason you want to learn it.''',
        f'''LEARNING OBJECTIVE\nCreate named values and understand the types of data your program uses.\n\nTHE IDEA\nA variable is a named place or binding used to refer to a value. Types describe what kind of value is stored and which operations make sense. {language} has rules for declaring and using values; follow the type and declaration syntax rather than assuming all languages behave like JavaScript or Python.\n\nSTEP BY STEP\nChoose a descriptive name, create a value using the language's declaration syntax, assign a suitable type and use the value in an expression. When input arrives as text, convert or validate it before doing numeric calculations.\n\nCOMMON MISTAKES\nAvoid unclear names, using a value before it is initialised, and mixing incompatible types without an explicit conversion.\n\nPRACTICE\nCreate values for a product name, unit price and quantity. Calculate and display the total.''',
        f'''LEARNING OBJECTIVE\nControl which instructions run and repeat a task when appropriate.\n\nTHE IDEA\nPrograms use conditional statements to choose between paths. A condition evaluates to true or false. Loops repeat instructions while a condition holds or for each item in a collection. These ideas appear in almost every programming language, although their exact syntax differs.\n\nSTEP BY STEP\nStart with a value. Write a condition that handles one case and an alternative case. Then use a loop to process a small range or collection. Trace the value of the loop variable on each repetition.\n\nCOMMON MISTAKES\nWatch for incorrect comparison operators, off-by-one errors and loops that never reach their stopping condition.\n\nPRACTICE\nWrite a program that classifies a score as pass or not-yet-pass, then prints the numbers from 1 to 5.''',
        f'''LEARNING OBJECTIVE\nBreak a problem into a function with inputs and an output.\n\nTHE IDEA\nA function gives a reusable name to a block of logic. Parameters describe the information it needs; arguments are the values supplied when it is called. A return value sends a result back to the caller. Some languages require explicit return types, while others infer or use dynamic types.\n\nDESIGN\nA good function should have a clear purpose and a name that describes its job. Prefer passing required values as parameters instead of relying on hidden global state. Test a function with normal, boundary and invalid inputs.\n\nCOMMON MISTAKES\nDo not confuse displaying a result with returning it. Check the language's rules for parameter types, return types and scope.\n\nPRACTICE\nCreate a function that calculates the total cost from a unit price and quantity. Test at least three cases.''',
        f'''LEARNING OBJECTIVE\nStore multiple values and process them systematically.\n\nTHE IDEA\nCollections help a program work with groups of related values. Depending on the language, common structures include arrays, lists, slices, vectors, maps or dictionaries. Choose a structure based on whether you need ordering, unique keys, fast lookup or the ability to change its size.\n\nSTEP BY STEP\nCreate a collection with at least three values, loop through each item, and calculate a count or total. Pay attention to indexing rules and whether the collection can be modified while you iterate over it.\n\nCOMMON MISTAKES\nCheck index boundaries, understand whether an operation changes the original collection, and use a map or dictionary when each value needs a meaningful key.\n\nPRACTICE\nStore five scores, calculate their average and count how many meet a pass mark you choose.'''
    ]
    return list(zip(EXTRA_LESSON_TITLES, bodies, snippets))

for _slug in EXTRA_TRACKS:
    CURRICULUM[_slug] = build_extra_lessons(_slug)
