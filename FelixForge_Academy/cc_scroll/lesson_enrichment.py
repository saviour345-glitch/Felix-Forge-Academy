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
    # Positions change when new foundations are inserted, so maintained lessons
    # are classified by their title wherever possible.
    t = (title or '').lower()
    if slug == 'javascript':
        if any(word in t for word in ('async', 'promise', 'fetch', 'http', 'module')):
            return 'javascript_async'
        return 'javascript_dom'
    if slug == 'python':
        if any(word in t for word in ('file', 'path', 'exception', 'debug', 'error', 'json', 'package', 'pip')):
            return 'python_files_errors'
        if any(word in t for word in ('variable', 'type', 'expression')):
            return 'variables'
        if any(word in t for word in ('loop', 'decision', 'condition')):
            return 'control_flow'
        if any(word in t for word in ('function', 'parameter')):
            return 'functions'
        if any(word in t for word in ('list', 'dictionary', 'collection', 'array', 'generator')):
            return 'collections'
        return 'program_start'
    if slug in ('html', 'css', 'sql'):
        return slug
    if any(word in t for word in ('variable', 'type', 'value', 'expression')):
        return 'variables'
    if any(word in t for word in ('function', 'method', 'parameter', 'return')):
        return 'functions'
    if any(word in t for word in ('loop', 'decision', 'condition', 'branch', 'repetition')):
        return 'control_flow'
    if any(word in t for word in ('array', 'list', 'collection', 'vector', 'slice', 'map', 'dictionary', 'object', 'class', 'struct')):
        return 'collections'
    if any(word in t for word in ('first program', 'program structure', 'output')):
        return 'program_start'
    # Fallback only for user-created lessons without a recognisable topic.
    if position == 1: return 'program_start'
    if position == 2: return 'variables'
    if position == 3: return 'control_flow'
    if position == 4: return 'functions'
    return 'collections'


def deep_dive(slug, position, title):
    # New beginner lessons are inserted before the original curriculum. Select
    # their teaching guide by topic title, not by the shifted lesson position.
    t = title.lower()
    beginner_guides = [
        (('from zero', 'first program', 'how a webpage is structured', 'styling your first webpage', 'databases, tables'),
         'Start with the smallest working example',
         'Run the example first, then change one small part and run it again. Learning to connect a line of code with the result is more useful than memorising punctuation without context.',
         ['Identify where the program or document begins.','Find the instruction that produces the visible result.','Change a word or value and predict what will happen before running it.'],
         ['Copying code without saving or running it.','Changing several things at once, making it difficult to find the cause of an error.'],
         'Re-create the example from a blank file, then personalise its output or content.'),
        (('variables', 'values and data types', 'attributes, paths'),
         'Names, values and types',
         'A variable name gives a value a useful label. Types describe what kind of value is stored and which operations are appropriate. Keep names descriptive and check whether the language allows reassignment.',
         ['Text and numbers are different kinds of values.','A Boolean represents true or false.','Use clear names such as learnerName, score and total.'],
         ['Confusing a number with text containing digits.','Changing a constant or using a name with the wrong capitalisation.'],
         'Create four clearly named values and explain the type and purpose of each.'),
        (('operators and expressions', 'colours, text and the box model', 'where: filtering'),
         'Expressions and rules',
         'Operators combine values to produce a result. In a style sheet, declarations apply a property value to selected elements; in SQL, a WHERE condition decides which rows match.',
         ['Read an expression from its inputs to its result.','Use parentheses to make complicated calculations easier to follow.','Test comparisons with more than one sample value.'],
         ['Confusing assignment with comparison.','Ignoring operator order or combining conditions without checking their meaning.'],
         'Change the sample values and write down the expected result before running the example.'),
        (('decisions', 'if, else', 'selectors, classes', 'responsive design'),
         'Making decisions with conditions',
         'A condition is a question whose result determines what happens next. Check each possible path, including boundary values. For styling, selectors choose which elements receive a rule and media queries apply rules only under stated screen conditions.',
         ['Identify the condition being checked.','Follow the true branch and the false branch.','Test values exactly at the boundary as well as above and below it.'],
         ['Putting a broad condition before a more specific one.','Testing only one possible outcome.'],
         'Test at least three different inputs or screen sizes and explain why each path is selected.'),
        (('loops', 'repeating instructions'),
         'Repeating work safely',
         'A loop repeats instructions. It needs a start, a continuation condition and a way to make progress toward stopping. Trace the counter or current item through each repetition.',
         ['Know whether the loop counts a fixed number of times or runs while a condition is true.','Check the first and last values.','Make sure the stopping condition can eventually become false.'],
         ['Creating an infinite loop.','Off-by-one errors that repeat one time too many or too few.'],
         'Trace a loop by hand in a small table showing the counter and output on each pass.'),
        (('functions', 'reusable blocks', 'methods and return'),
         'Breaking a program into reusable functions',
         'A function gives a task a name. Parameters receive information, the function body performs the work, and a return value sends a result back when needed. Keep one function focused on one clear responsibility.',
         ['Separate the function definition from the function call.','Match arguments with parameters.','Distinguish returning a value from displaying it.'],
         ['Forgetting required arguments.','Expecting printed output to behave like a returned value.'],
         'Write a small function, call it with two different sets of values and compare the results.'),
        (('collections', 'arrays, lists', 'lists, tables and grouping', 'headings, paragraphs'),
         'Working with collections and repeated information',
         'Collections group related items. Ordered collections use positions, often starting at zero; key-value collections use descriptive keys. In HTML and SQL, choose the structure that matches the meaning of the content or records.',
         ['Check the collection length before accessing an index.','Use a loop to process each item.','Use named keys or columns when they make the data easier to understand.'],
         ['Reading an item beyond the end of a collection.','Mixing up a key, an index and the value stored there.'],
         'Create a small collection, add an item, retrieve one value and display the number of items.'),
        (('objects', 'structured data', 'relationships and join'),
         'Grouping related data',
         'A structured value keeps related information together. A class or type describes the shape and behaviour; an instance is one particular value. In a relational database, keys connect records across tables.',
         ['Identify the fields that belong together.','Distinguish a type definition from an instance.','Use a relationship key to connect related records.'],
         ['Confusing the description with an actual object.','Joining tables using unrelated columns.'],
         'Model a learner or robot with at least two fields and describe one instance.'),
        (('input, output', 'forms and input', 'error checking'),
         'Input, output and validation',
         'Input comes from a person, file, form or another system. Check it before using it. Output should explain the result clearly. Browser-side checks improve the experience, but data sent to a server must be validated again there.',
         ['Check for missing or empty values.','Convert text to a number only after checking it.','Give a useful message that explains how to correct invalid input.'],
         ['Assuming all input is valid.','Displaying untrusted input as HTML.'],
         'Test one valid value, one missing value and one invalid value. Explain the message the learner should see.'),
    ]
    for needles, heading, overview, points, mistakes, challenge in beginner_guides:
        if any(needle in t for needle in needles):
            return {'heading':heading, 'overview':overview, 'points':points,
                    'mistakes':mistakes, 'challenge':challenge}
    key=topic_key(slug,position,title)
    guide=GUIDES[key]
    return {'heading':guide['heading'],'overview':guide['overview'],'points':guide['points'],'mistakes':guide['mistakes'],'challenge':guide['challenge']}
