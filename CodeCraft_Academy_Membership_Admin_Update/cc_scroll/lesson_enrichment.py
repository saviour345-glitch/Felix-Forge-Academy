"""Deeper topic notes for FelixForge Academy lessons."""

GUIDES = {
'program_start': {
 'heading':'How a program is organised',
 'overview':'A program is a sequence of instructions interpreted or executed by a runtime. Before the computer can perform the task, the source must follow the language grammar. Compiled languages commonly translate source into an executable or intermediate form; interpreted and virtual-machine languages use a runtime to execute the program. In either case, execution begins at a language-defined entry point or at the first top-level statement. A useful program separates setup, input, processing and output so each stage can be understood and tested.',
 'points':['Source file: the human-readable instructions saved in a file. File extensions often help tools recognise the language.','Entry point: the function or first statement where execution begins, such as main in C, C++, Java, C#, Go, Rust and Kotlin.','Statements and expressions: a statement performs an action; an expression produces a value that can be used by another operation.','Libraries and imports: reusable code supplied by the language or other packages. Import only what the program needs.','Build and run: compilation, interpretation and runtime execution are different stages. A syntax error may stop a build before the program starts.','Output and diagnostics: normal output communicates results; errors and logs help locate faults.'],
 'mistakes':['Saving a file with the wrong extension or running a different file from the one being edited.','Missing punctuation, braces, indentation or required entry-point structure.','Confusing a compiler error with a runtime error or an incorrect result.'],
 'challenge':'Create a program with a clear entry point, two output statements and a short comment. Change one statement, run it again and describe which stage of the program changed.'},
'variables': {
 'heading':'Variables, data types and expressions in depth',
 'overview':'A variable is a named place to refer to a value while a program runs. A data type describes what kind of value is stored and which operations are meaningful. Languages differ in how explicitly types are written: some require declarations, some infer types, and some allow a variable to refer to values of different types. Choosing the correct type prevents invalid operations and makes the intention of the program clearer.',
 'points':['Common types: integers for whole numbers, floating-point values for approximate decimals, strings for text, characters for single symbols and Booleans for true/false conditions.','Constants and mutability: use a constant when reassignment is not required. Languages use different keywords and rules for this.','Operators: arithmetic (+, -, *, /, remainder), comparison (==, !=, <, >) and logical operators combine or compare values.','Conversion: input often arrives as text. Convert it deliberately and handle invalid input rather than assuming conversion always succeeds.','Scope and lifetime: a local variable is available only inside its block or function; broader scope makes data accessible in more places and can make programs harder to reason about.','Precision: floating-point values are approximations. For money, use integer minor units or a decimal type designed for exact decimal arithmetic.'],
 'mistakes':['Adding strings when numeric addition was intended, or performing arithmetic on unconverted input.','Using a value before initialising it, or changing a constant.','Using == and = interchangeably; assignment and comparison are different operations.'],
 'challenge':'Create a small receipt calculator. Store quantity, unit price and discount separately, validate that the values are sensible, calculate a total and print a clearly formatted result.'},
'control_flow': {
 'heading':'Decisions, loops and program flow',
 'overview':'Control flow determines which instructions run and how often. A conditional evaluates a Boolean expression and selects a branch. A loop repeats a block while a condition remains true or for each item in a collection. The key to reliable control flow is understanding the condition, the state it reads, and how that state changes on each pass.',
 'points':['Comparison operators test equality or ordering. Use the language-appropriate equality operator rather than assignment.','Logical AND requires all included conditions to be true; OR requires at least one; NOT reverses a Boolean value.','if/else handles two-way or multi-way decisions. switch, match or case constructs can make many fixed alternatives clearer.','A counted loop is useful when the number of repetitions is known. A condition-controlled loop is useful when repetition depends on changing state.','break exits a loop; continue skips to the next iteration. Use both carefully so the flow remains readable.','Nested loops are loops inside loops. Their work can grow quickly because each outer iteration runs the inner loop.'],
 'mistakes':['Off-by-one errors caused by misunderstanding whether the final loop value is included.','A loop condition that never becomes false, producing an infinite loop.','Testing the wrong condition or forgetting to update the variable used by the condition.'],
 'challenge':'Write a program that examines a list of scores, counts passes and failures, and reports the highest score. Test an empty list and scores exactly on the pass boundary.'},
'functions': {
 'heading':'Functions, parameters and reusable design',
 'overview':'A function gives a meaningful name to a group of instructions. It allows a program to be divided into smaller units that can be understood, tested and reused. A parameter is a named input in the function definition; an argument is the actual value supplied when the function is called. A return value sends a result back to the caller. Some functions perform an action and return no useful value.',
 'points':['Keep one function focused on one responsibility. Small functions are easier to test and combine.','Choose clear names that describe the action or result, such as calculate_total or find_student.','Distinguish printing a value from returning it. Printed text is output; a returned value can be stored, compared or passed to another function.','Understand parameter rules in the language: positional, named, optional, default, reference or value parameters.','Local variables belong to a function or block. Avoid unnecessary global state because it makes dependencies harder to see.','Recursion is when a function calls itself. It needs a base case and a step that moves towards that base case.'],
 'mistakes':['Calling a function with the wrong number or type of arguments.','Forgetting to return a value or expecting print/output to behave like return.','Writing one very large function that mixes input, calculations, storage and display.'],
 'challenge':'Refactor a calculator into separate functions for input validation, calculation and result formatting. Test each function with several inputs.'},
'collections': {
 'heading':'Collections and working with groups of data',
 'overview':'Collections let a program store and process multiple related values. Arrays and lists commonly store ordered items, maps or dictionaries associate keys with values, and sets store unique values. The collection type affects how data is accessed, changed, searched and traversed. Select a collection based on the operations your program performs most often.',
 'points':['Indexing: many ordered collections use zero-based indexes, so the first item is at index 0. Check bounds before accessing an index.','Iteration: loops can visit each item directly or use an index when the position is important.','Mutability: some collections can be changed in place; others are immutable or return a new collection after an operation.','Maps and dictionaries are useful for looking up a value by a meaningful key rather than searching by position.','Sets are useful for uniqueness and membership checks. They generally do not promise the same ordering as lists.','Nested collections can model structured data, such as a list of student records where each record is an object or map.'],
 'mistakes':['Accessing an index that does not exist or changing a collection while iterating over it.','Assuming a map or set has the same ordering guarantees as an array.','Using a list for repeated key-based lookups when a map would make the intention clearer.'],
 'challenge':'Store learner names and scores. Calculate the class average, find the highest score, and build a separate collection containing only learners who passed.'},
'html': {
 'heading':'HTML structure, semantics and accessibility',
 'overview':'HTML describes the meaning and structure of web content. Browsers parse elements into a document tree, while assistive technologies use semantic information to help people navigate. A good document has a clear hierarchy: metadata in head, visible content in body, meaningful headings, landmarks and labels. HTML is not a programming language; it marks up content that CSS styles and JavaScript can enhance.',
 'points':['Use a doctype, a language attribute on html, a descriptive title, character encoding and a responsive viewport declaration.','Use header, nav, main, section, article and footer according to the meaning of the content, not merely their default appearance.','Use headings in a logical hierarchy. A heading level should describe the section structure.','Give images useful alt text when they communicate information; use empty alt text for purely decorative images.','Connect labels to form controls. Group related controls with fieldset and legend when appropriate.','Use buttons for actions and links for navigation. This improves keyboard and assistive-technology behaviour.'],
 'mistakes':['Choosing elements only because they look the way you want rather than because they describe the content.','Using placeholder text as the only label for an input.','Leaving informative images without alternative text or creating links with vague text such as “click here”.'],
 'challenge':'Build a semantic article page with a header, navigation, main article, image with alt text, labelled feedback form and footer. Navigate it using only the keyboard.'},
'css': {
 'heading':'CSS cascade, layout and responsive styling',
 'overview':'CSS controls how HTML elements are presented. A browser combines declarations from stylesheets, the cascade, specificity, inheritance and source order to determine the final style. Layout systems such as normal flow, Flexbox and Grid position content. Responsive design uses flexible sizes and media queries so a page adapts to different viewport sizes.',
 'points':['A selector identifies elements; a declaration is a property-value pair. Rules can target elements, classes, IDs, attributes and relationships.','The cascade resolves competing declarations using origin, importance, specificity and source order. Avoid solving every conflict by adding !important.','The box model contains content, padding, border and margin. box-sizing:border-box makes declared dimensions easier to reason about.','Use Flexbox for arranging items along one main axis and Grid for rows and columns. Both can adapt to available space.','Use relative units such as rem, %, fr, minmax and viewport units where they support flexible layouts.','Media queries apply styles at conditions such as viewport width, while mobile-first rules begin with the smallest layout.'],
 'mistakes':['Overusing absolute positioning for layouts that should flow naturally.','Using fixed widths that cause horizontal scrolling on small screens.','Writing highly specific selectors that make later changes difficult.'],
 'challenge':'Create a responsive course-card layout using Grid, then use Flexbox inside each card. Test a narrow phone width, tablet width and desktop width.'},
'javascript_dom': {
 'heading':'The DOM as a live programming interface',
 'overview':'The browser converts HTML into a live Document Object Model tree. JavaScript can select nodes, read their properties, change text, update attributes, modify classes and respond to events. DOM code depends on the page structure being available, so scripts should run after the relevant elements have been parsed. Treat text received from users as text rather than injecting it as HTML.',
 'points':['querySelector returns the first matching element; querySelectorAll returns a collection of matches. A missing single match returns null.','textContent is a safe default for text. innerHTML parses markup and must not receive untrusted strings.','classList provides add, remove, contains and toggle for reusable CSS states.','Events such as click, input, change, submit and keydown connect user actions to JavaScript functions.','Event bubbling makes event delegation possible: a parent can handle events from matching descendants.','Update only the part of the page that needs to change, and keep data separate from presentation where practical.'],
 'mistakes':['Selecting an element before it exists or forgetting to check for null.','Using innerHTML with user-controlled content, which can introduce cross-site scripting.','Attaching repeated listeners every time a component is rendered.'],
 'challenge':'Build a task list that adds items, marks them complete and removes them. Use textContent to display typed text and event delegation for the item controls.'},
'javascript_async': {
 'heading':'Asynchronous JavaScript and network requests',
 'overview':'JavaScript runs much of its code on a single main thread, so long-running work must not block the interface. Promises represent work that may finish later. async functions always return a promise, and await pauses that function until the promise settles while allowing the rest of the event loop to continue. Network requests can fail, return an unsuccessful HTTP status or contain data that is not shaped as expected.',
 'points':['A promise can be pending, fulfilled or rejected. Handle rejection with try/catch or a catch handler.','fetch sends a request and resolves to a Response; it does not automatically reject for HTTP 404 or 500 responses. Check response.ok.','Read response bodies with methods such as json() or text(); these are asynchronous too.','Show loading, success and error states so users know what is happening.','Avoid starting duplicate requests when a user clicks repeatedly. Consider cancellation for searches that become outdated.','Never place private API keys in front-end JavaScript. Secrets belong on a protected server.'],
 'mistakes':['Forgetting await when reading a promise result.','Assuming fetch rejects for every unsuccessful HTTP status.','Ignoring network errors or displaying raw server errors to users.'],
 'challenge':'Fetch a public test API, display a loading message, render the returned records and show a helpful error if the request fails.'},
'python_files_errors': {
 'heading':'Reliable Python programs: errors, files and debugging',
 'overview':'Programs interact with unpredictable inputs and external resources. Exceptions represent errors that occur while a program runs. A try block contains operations that may fail; except handles specific failures; finally is used for cleanup that must happen whether an error occurred or not. Files should be opened with a context manager so they are closed reliably.',
 'points':['Read a traceback from the bottom upward to find the exception type and the line where it occurred. Then inspect the values used on that line.','Catch specific exceptions such as ValueError or FileNotFoundError rather than catching every possible error without a reason.','Use with open(path, encoding="utf-8") as file so the file is closed automatically.','Validate external input at the boundary of a program before using it in calculations or database operations.','Use print for quick inspection and a debugger or logging for more systematic diagnosis.','Do not hide errors with a blank except block. Report what failed and give the user a useful next step.'],
 'mistakes':['Catching Exception and silently ignoring the problem.','Assuming a file exists or that its contents have the expected format.','Using a relative file path without understanding the program working directory.'],
 'challenge':'Write a program that reads a small text file of scores, handles a missing file, validates each score and prints the average.'},
'sql': {
 'heading':'Relational databases and reliable SQL queries',
 'overview':'A relational database organises information into tables. Rows represent records and columns represent attributes. A primary key identifies a row; a foreign key links related records. SQL statements define structures, read data and change records. Queries should be designed around the data relationships and should return only the columns and rows required.',
 'points':['SELECT chooses columns; FROM identifies the table; WHERE filters rows; ORDER BY sorts the result; LIMIT can restrict the number of rows.','INSERT adds records. UPDATE changes selected records and DELETE removes selected records; use a precise WHERE clause when changing data.','A primary key should be unique and non-null. Foreign keys help preserve valid relationships between tables.','INNER JOIN returns matching records from both sides; LEFT JOIN keeps all rows from the left table and fills missing matches with NULL.','COUNT, SUM, AVG, MIN and MAX calculate summaries. GROUP BY forms groups and HAVING filters groups after aggregation.','Use parameterised queries for values from users. Never build SQL by concatenating untrusted input.'],
 'mistakes':['Running UPDATE or DELETE without checking the WHERE condition.','Joining tables on the wrong columns and multiplying rows unexpectedly.','Using WHERE for aggregate conditions that belong in HAVING.'],
 'challenge':'Create learners and results tables, insert sample records, join them, calculate each learner average and find learners whose average is at least 70.'},
}


def topic_key(slug, position, title):
    t=title.lower()
    if slug=='javascript':
        if position<=3: return 'javascript_dom'
        if position in (4,5,6,7,8): return 'javascript_dom'
        return 'javascript_async'
    if slug=='python' and position>=7: return 'python_files_errors'
    if slug=='html': return 'html'
    if slug=='css': return 'css'
    if slug=='sql': return 'sql'
    if position==1: return 'program_start'
    if position==2: return 'variables'
    if position==3: return 'control_flow'
    if position==4: return 'functions'
    if position>=5: return 'collections'
    if 'variable' in t or 'type' in t: return 'variables'
    if 'function' in t: return 'functions'
    if 'loop' in t or 'decision' in t: return 'control_flow'
    return 'program_start'


def deep_dive(slug, position, title):
    key=topic_key(slug,position,title)
    guide=GUIDES[key]
    return {'heading':guide['heading'],'overview':guide['overview'],'points':guide['points'],'mistakes':guide['mistakes'],'challenge':guide['challenge']}
