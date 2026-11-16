"""Small teaching helpers used by the lesson page."""
import re

RULES = [
    (r'^\s*#', 'This is a comment or preprocessor directive. Comments explain intent and are not ordinary executable statements; preprocessor lines are handled before compilation.'),
    (r'^\s*//|^\s*/\*|^\s*\*|^\s*<!--', 'This is a comment. It documents the code for people reading it; it is not displayed as program output.'),
    (r'\b(import|from|using|package)\b', 'This line makes a library, module, namespace or package available, or identifies the package this source file belongs to.'),
    (r'\b(class|struct|interface|enum)\b', 'This declares a type. A class or structure groups data and behaviour so related parts of a program can be modelled together.'),
    (r'\b(def|function|func|fn)\b|\bfun\s+', 'This defines a function. A function gives a named, reusable block of instructions; parameters receive inputs and a return value can send a result back.'),
    (r'\b(if|else|elif|switch|case)\b', 'This is conditional logic. The program evaluates a condition or matching case and selects which branch should execute.'),
    (r'\b(for|while|foreach|each)\b', 'This begins or participates in repetition. The loop repeats a block for a sequence of values or while a condition remains true; check its stopping condition to avoid an infinite loop.'),
    (r'\b(return|yield)\b', 'This sends a value back to the caller or pauses a generator. A return may also end the current function immediately.'),
    (r'\b(print|println|printf|console\.log|echo|cout)\b', 'This sends information to an output destination such as the terminal or browser console. It helps a learner observe the program while testing.'),
    (r'\b(input|readline|Scanner|prompt\s*\()', 'This reads input from a user or input stream. Check and convert the input before using it in calculations.'),
    (r'\btry\b|\bcatch\b|\bexcept\b|\bfinally\b', 'This participates in exception handling. It lets a program respond to an operation that fails instead of allowing an unhandled error to stop the normal flow.'),
    (r'\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bCREATE\b|\bJOIN\b', 'This is an SQL statement. It asks the database to retrieve, add, change, remove or combine structured records. Always use parameterised queries for values supplied by users.'),
    (r'\b(querySelector|addEventListener|textContent|classList|document\.)', 'This interacts with the browser DOM. It selects an element or responds to an event / changes the live page. Check that selected elements exist before using them.'),
    (r'\b(const|let|var|int|float|double|string|bool|boolean|char|val|var)\b', 'This declares or introduces a variable. The name identifies stored data; its type or inferred type determines which values and operations are valid.'),
    (r'\b(True|False|true|false|null|None|nil|undefined)\b', 'This uses a Boolean or special empty-value literal. Be precise about the difference between false, zero, an empty string and a missing value.'),
    (r'\b(open|with)\s*\(', 'This opens or manages a resource such as a file. Close resources reliably; context managers or structured resource APIs help avoid leaks.'),
    (r'\b(append|push|add|insert|remove|pop)\s*\(', 'This calls a collection operation. Check whether it changes the original collection, returns a new collection, or returns the removed item.'),
    (r'=>|->', 'This uses an arrow or return-type syntax. Depending on the language, it may define a concise function, lambda expression or function return type.'),
    (r'\{|\}', 'These braces delimit a block or structure in this language, such as a function, class, conditional, loop, object or CSS rule.'),
    (r'=', 'This line contains an assignment or initialisation. The expression on the right is evaluated and its value is stored in the name on the left; in some languages, a single equals sign has a different meaning in a condition.'),
]

def explain_line(line, language=''):
    stripped=line.strip()
    if not stripped:
        return 'Blank line: used to separate logical sections and make the program easier to read.'
    if stripped.startswith(('</','<','<!')):
        return 'This is an HTML element or tag. The tag name describes the content or control; attributes configure it, and nesting determines the document structure.'
    if stripped.startswith('.') and '{' in stripped:
        return 'This is a CSS selector. It identifies the elements that receive the declarations inside the rule block.'
    if ':' in stripped and ('color' in stripped or 'display' in stripped or 'margin' in stripped or 'padding' in stripped or 'grid-' in stripped or 'font-' in stripped):
        return 'This is a CSS declaration: the property before the colon selects what to style, and the value after it controls how that property appears.'
    for pattern, explanation in RULES:
        if re.search(pattern, stripped, re.I):
            return explanation
    if stripped.endswith(';'):
        return 'This completes a statement. Read the expression from left to right, identify the values it uses, and note what state or output it changes.'
    if stripped.startswith((')',']',')', '}', 'else', 'end')):
        return 'This closes or continues a previously opened structure. Match it with the corresponding opening block to understand the program flow.'
    return 'Read this statement as one step in the program: identify the names it uses, the operation being performed, and how its result affects the next statement.'

def code_walkthrough(code, language=''):
    """Return concise, useful explanations for non-empty source lines."""
    result=[]
    for number, line in enumerate(code.splitlines(), 1):
        if not line.strip():
            continue
        result.append({'number':number,'code':line,'explanation':explain_line(line, language)})
        if len(result)>=28:
            result.append({'number':'…','code':'Additional lines omitted from this quick guide.','explanation':'Read the remaining lines using the same method: identify inputs, operations, control flow and outputs.'})
            break
    return result

def expected_behaviour(example, language=''):
    title=(example.get('title') or '').lower()
    code=example.get('code','')
    if 'total' in title:
        return 'The program calculates the cost by multiplying the quantity by the unit price. With the sample values 3 and 500, the total is 1,500.'
    if 'score' in title or 'condition' in title:
        return 'The condition is evaluated first. With a sample score of 76 and a pass mark of 50, the passing branch is selected.'
    if 'square' in title or 'calculated value' in title:
        return 'The function multiplies its input by itself. For the sample input 6, the returned result is 36.'
    if 'array' in title or 'list' in title or 'vector' in title or 'slice' in title:
        return 'The program visits the stored items in order. The values shown in the collection are processed one at a time.'
    if 'output' in title or 'message' in title:
        return 'The text statements run in sequence and display their messages in the output area or terminal.'
    if 'dom' in title or 'element' in title or 'class' in title or 'click' in title or 'event' in title:
        return 'The visible page changes or a browser event is handled when the required HTML elements are present. Open the browser console and inspect the page to verify the behaviour.'
    if 'sql' in language.lower() or any(k in code.upper() for k in ('SELECT ', 'INSERT ', 'CREATE TABLE')):
        return 'The database processes the statement. A SELECT displays matching rows; INSERT or CREATE changes the database structure or contents. Run it against a practice database first.'
    if language.lower() in ('html','css'):
        return 'The browser interprets the markup or style rules. View the page in a browser and inspect the element to confirm the structure, spacing and responsive behaviour.'
    return 'The exact output depends on the sample values and the environment. Trace the statements in order, then run the example and compare the actual result with your prediction.'
