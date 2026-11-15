"""Additional guided examples shown alongside each lesson's main example."""

# Each entry is a list of (title, explanation, code). Generic language courses
# follow the five curriculum units: structure, values, decisions/loops,
# functions, and collections.
GENERIC = {
'c': [
('A small reusable output','A program starts in main. printf writes text to the terminal.','#include <stdio.h>\n\nint main(void) {\n    printf("My first C program\\n");\n    printf("I am learning step by step.\\n");\n    return 0;\n}'),
('Calculate a total','An integer stores a whole number. The expression is evaluated before printf displays the answer.','#include <stdio.h>\n\nint main(void) {\n    int notebooks = 3;\n    int price = 500;\n    int total = notebooks * price;\n    printf("Total: %d naira\\n", total);\n    return 0;\n}'),
('Check a score','The if/else statement chooses one branch based on whether the condition is true.','#include <stdio.h>\nint main(void) {\n    int score = 76;\n    if (score >= 50) {\n        printf("Pass\\n");\n    } else {\n        printf("Try again\\n");\n    }\n    return 0;\n}'),
('Return a calculated value','A function can receive an argument and return a result to its caller.','#include <stdio.h>\nint square(int number) { return number * number; }\nint main(void) {\n    printf("%d\\n", square(6));\n    return 0;\n}'),
('Read values from an array','Array indexes start at zero. The loop visits each of the four stored values.','#include <stdio.h>\nint main(void) {\n    int scores[] = {65, 72, 88, 91};\n    for (int i = 0; i < 4; i++) {\n        printf("Score %d: %d\\n", i + 1, scores[i]);\n    }\n    return 0;\n}')],
'cpp': [
('A small reusable output','main is where this program begins, and cout sends text to the terminal.','#include <iostream>\nusing namespace std;\nint main() {\n    cout << "My first C++ program" << endl;\n    cout << "Learning by building." << endl;\n    return 0;\n}'),
('Calculate a total','Variables store values, and multiplication calculates the total cost.','#include <iostream>\nusing namespace std;\nint main() {\n    int notebooks = 3, price = 500;\n    int total = notebooks * price;\n    cout << "Total: " << total << " naira" << endl;\n}'),
('Check a score','The condition decides which message is printed.','#include <iostream>\nusing namespace std;\nint main() {\n    int score = 76;\n    if (score >= 50) cout << "Pass";\n    else cout << "Try again";\n}'),
('Return a calculated value','The square function returns number multiplied by itself.','#include <iostream>\nusing namespace std;\nint square(int number) { return number * number; }\nint main() { cout << square(6) << endl; }'),
('Read values from a vector','A vector stores a resizable collection. A range-based loop visits each value.','#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    vector<int> scores{65, 72, 88, 91};\n    for (int score : scores) cout << score << endl;\n}')],
'java': [
('A small reusable output','Java code is placed inside a class, and execution begins in main.','public class Main {\n    public static void main(String[] args) {\n        System.out.println("My first Java program");\n        System.out.println("Learning by building.");\n    }\n}'),
('Calculate a total','int stores whole numbers; multiplication produces the total cost.','public class Main {\n    public static void main(String[] args) {\n        int notebooks = 3;\n        int price = 500;\n        int total = notebooks * price;\n        System.out.println("Total: " + total);\n    }\n}'),
('Check a score','An if/else statement selects a result according to a condition.','public class Main {\n    public static void main(String[] args) {\n        int score = 76;\n        if (score >= 50) System.out.println("Pass");\n        else System.out.println("Try again");\n    }\n}'),
('Return a calculated value','A static method can be called from main and return an integer.','public class Main {\n    static int square(int number) { return number * number; }\n    public static void main(String[] args) {\n        System.out.println(square(6));\n    }\n}'),
('Read values from an array','The for loop uses an index to visit each array element.','public class Main {\n    public static void main(String[] args) {\n        int[] scores = {65, 72, 88, 91};\n        for (int i = 0; i < scores.length; i++) {\n            System.out.println(scores[i]);\n        }\n    }\n}')],
'csharp': [
('A small reusable output','Console.WriteLine displays a line of text in a C# console program.','using System;\nclass Program {\n    static void Main() {\n        Console.WriteLine("My first C# program");\n        Console.WriteLine("Learning by building.");\n    }\n}'),
('Calculate a total','The int variables hold whole numbers, and the multiplication result is stored in total.','using System;\nclass Program {\n    static void Main() {\n        int notebooks = 3, price = 500;\n        int total = notebooks * price;\n        Console.WriteLine($"Total: {total}");\n    }\n}'),
('Check a score','The condition controls which branch runs.','int score = 76;\nif (score >= 50) {\n    Console.WriteLine("Pass");\n} else {\n    Console.WriteLine("Try again");\n}'),
('Return a calculated value','A method receives an integer and returns its square.','static int Square(int number) {\n    return number * number;\n}\nConsole.WriteLine(Square(6));'),
('Read values from a list','A foreach loop visits every item in the collection.','using System;\nusing System.Collections.Generic;\nvar scores = new List<int> { 65, 72, 88, 91 };\nforeach (int score in scores) {\n    Console.WriteLine(score);\n}')],
'php': [
('A small reusable output','PHP statements are commonly placed between PHP opening and closing tags.','<?php\necho "My first PHP program\\n";\necho "Learning by building.\\n";'),
('Calculate a total','Variables begin with $. Multiplication calculates the total cost.','<?php\n$notebooks = 3;\n$price = 500;\n$total = $notebooks * $price;\necho "Total: ₦" . $total;'),
('Check a score','if/else chooses a message based on the score.','<?php\n$score = 76;\nif ($score >= 50) {\n    echo "Pass";\n} else {\n    echo "Try again";\n}'),
('Return a calculated value','A function can accept a parameter and return a result.','<?php\nfunction square($number) {\n    return $number * $number;\n}\necho square(6);'),
('Read values from an array','foreach visits each value in the array without manually tracking an index.','<?php\n$scores = [65, 72, 88, 91];\nforeach ($scores as $score) {\n    echo $score . PHP_EOL;\n}')],
'go': [
('A small reusable output','The main function is the entry point of a Go executable.','package main\nimport "fmt"\nfunc main() {\n    fmt.Println("My first Go program")\n    fmt.Println("Learning by building.")\n}'),
('Calculate a total','Short variable declarations create values whose types are inferred.','package main\nimport "fmt"\nfunc main() {\n    notebooks, price := 3, 500\n    total := notebooks * price\n    fmt.Println("Total:", total)\n}'),
('Check a score','Go uses if and else blocks to select a path.','package main\nimport "fmt"\nfunc main() {\n    score := 76\n    if score >= 50 { fmt.Println("Pass") } else { fmt.Println("Try again") }\n}'),
('Return a calculated value','A function declares the type of value it returns.','package main\nimport "fmt"\nfunc square(n int) int { return n * n }\nfunc main() { fmt.Println(square(6)) }'),
('Read values from a slice','A slice is a flexible view of a sequence. range provides each value.','package main\nimport "fmt"\nfunc main() {\n    scores := []int{65, 72, 88, 91}\n    for _, score := range scores { fmt.Println(score) }\n}')],
'rust': [
('A small reusable output','Rust starts this executable at fn main, and println! prints a line.','fn main() {\n    println!("My first Rust program");\n    println!("Learning by building.");\n}'),
('Calculate a total','let binds values. The compiler infers the integer type in this example.','fn main() {\n    let notebooks = 3;\n    let price = 500;\n    let total = notebooks * price;\n    println!("Total: {total}");\n}'),
('Check a score','An if expression selects a branch when its condition is true or false.','fn main() {\n    let score = 76;\n    if score >= 50 { println!("Pass"); }\n    else { println!("Try again"); }\n}'),
('Return a calculated value','The -> i32 annotation says the function returns a 32-bit integer.','fn square(number: i32) -> i32 { number * number }\nfn main() { println!("{}", square(6)); }'),
('Read values from a vector','A vector stores multiple values. A for loop borrows each item in turn.','fn main() {\n    let scores = vec![65, 72, 88, 91];\n    for score in &scores { println!("{score}"); }\n}')],
'ruby': [
('A small reusable output','puts writes a line of text to the terminal.','puts "My first Ruby program"\nputs "Learning by building."'),
('Calculate a total','Ruby variables do not need a type declaration. The result is stored in total.','notebooks = 3\nprice = 500\ntotal = notebooks * price\nputs "Total: #{total}"'),
('Check a score','if and else choose which message is displayed.','score = 76\nif score >= 50\n  puts "Pass"\nelse\n  puts "Try again"\nend'),
('Return a calculated value','The final expression in a Ruby method is returned automatically.','def square(number)\n  number * number\nend\nputs square(6)'),
('Read values from an array','each runs a block once for every array item.','scores = [65, 72, 88, 91]\nscores.each do |score|\n  puts score\nend')],
'swift': [
('A small reusable output','Swift uses print to display text. The program begins with its top-level statements.','print("My first Swift program")\nprint("Learning by building.")'),
('Calculate a total','let creates a constant. Use it when the value should not be reassigned.','let notebooks = 3\nlet price = 500\nlet total = notebooks * price\nprint("Total: \\(total)")'),
('Check a score','if/else selects a branch based on a Boolean condition.','let score = 76\nif score >= 50 {\n    print("Pass")\n} else {\n    print("Try again")\n}'),
('Return a calculated value','The arrow marks the return type of a Swift function.','func square(_ number: Int) -> Int {\n    return number * number\n}\nprint(square(6))'),
('Read values from an array','for-in loops through every element in an array.','let scores = [65, 72, 88, 91]\nfor score in scores {\n    print(score)\n}')],
'kotlin': [
('A small reusable output','The main function is the entry point, and println displays a line.','fun main() {\n    println("My first Kotlin program")\n    println("Learning by building.")\n}'),
('Calculate a total','val creates a read-only variable, and Kotlin infers its type.','fun main() {\n    val notebooks = 3\n    val price = 500\n    val total = notebooks * price\n    println("Total: $total")\n}'),
('Check a score','if and else select which statement is executed.','fun main() {\n    val score = 76\n    if (score >= 50) println("Pass")\n    else println("Try again")\n}'),
('Return a calculated value','A function declares its return type after a colon.','fun square(number: Int): Int {\n    return number * number\n}\nfun main() { println(square(6)) }'),
('Read values from a list','A for loop visits every item in the list.','fun main() {\n    val scores = listOf(65, 72, 88, 91)\n    for (score in scores) println(score)\n}')],
}


SPECIAL = {
'python': [
('Format a useful message','f-strings insert variable values directly into a string.','student = "Ada"\nscore = 92\nprint(f"{student} scored {score}%")'),
('Convert input before calculating','input returns text. Convert it to int before doing arithmetic.','quantity = int(input("How many items? "))\nprice = 250\ntotal = quantity * price\nprint(f"Total: {total}")'),
('Combine conditions','and requires both conditions to be true.','age = 16\nhas_permission = True\nif age >= 15 and has_permission:\n    print("You may join the school club")\nelse:\n    print("Check the requirements")'),
('Use range to count','range(1, 6) produces 1, 2, 3, 4 and 5; the final value is excluded.','for number in range(1, 6):\n    print(number, "squared is", number ** 2)'),
('Reuse a function with different inputs','The same function can process several arguments without repeating its logic.','def rectangle_area(width, height):\n    return width * height\n\nprint(rectangle_area(4, 7))\nprint(rectangle_area(3, 9))'),
('Count values in a dictionary','A dictionary maps keys to values. Update a count when a word appears.','votes = {"Ada": 0, "Tomi": 0}\nvotes["Ada"] += 1\nvotes["Tomi"] += 2\nprint(votes)'),
('Handle a conversion error','try/except prevents an invalid conversion from crashing this small program.','text = "42x"\ntry:\n    number = int(text)\n    print(number)\nexcept ValueError:\n    print("Please enter a whole number")')],
'javascript': [
('Read a value from the DOM','querySelector finds the element, and textContent reads its visible text.','<p id="status">Ready</p>\n<script>\nconst status = document.querySelector("#status");\nconsole.log(status.textContent);\n</script>'),
('Select by class and count','querySelectorAll returns all matching elements in a NodeList.','const cards = document.querySelectorAll(".course-card");\nconsole.log(`There are ${cards.length} course cards.`);'),
('Toggle a class on click','classList.toggle adds the class if absent and removes it if present.','const panel = document.querySelector("#panel");\nconst toggle = document.querySelector("#toggle");\ntoggle.addEventListener("click", () => {\n  panel.classList.toggle("is-open");\n});'),
('React to a keyboard form submission','Listen on the form submit event so mouse and keyboard submission are both handled.','const form = document.querySelector("#search-form");\nform.addEventListener("submit", (event) => {\n  event.preventDefault();\n  console.log("Search submitted");\n});'),
('Calculate a total from form values','Number converts input text into a numeric value before addition.','const quantity = Number(document.querySelector("#quantity").value);\nconst price = Number(document.querySelector("#price").value);\nconst total = quantity * price;\nconsole.log(total);'),
('Transform an array with map','map creates a new array containing the result of each callback.','const prices = [100, 250, 400];\nconst withTax = prices.map(price => price * 1.075);\nconsole.log(withTax);'),
('Find a record in an array','find returns the first item whose callback condition is true.','const learners = [{name: "Ada", score: 82}, {name: "Tomi", score: 74}];\nconst ada = learners.find(learner => learner.name === "Ada");\nconsole.log(ada.score);'),
('Save a preference locally','localStorage stores strings in the browser for later visits on that same origin.','localStorage.setItem("theme", "dark");\nconst savedTheme = localStorage.getItem("theme");\nconsole.log(savedTheme);'),
('Wait for an asynchronous result','await pauses this async function until the promise settles.','async function loadMessage() {\n  const message = await Promise.resolve("Data loaded");\n  console.log(message);\n}\nloadMessage();'),
('Check a response before using data','fetch returns a promise. Check response.ok before reading the body.','async function loadUsers() {\n  const response = await fetch("/api/users");\n  if (!response.ok) throw new Error("Request failed");\n  const users = await response.json();\n  console.log(users);\n}'),
('Export and import a helper','Modules let you keep reusable functions in separate files.','// math.js\nexport function double(value) { return value * 2; }\n\n// app.js\nimport { double } from "./math.js";\nconsole.log(double(8));')],
'html': [
('Build a semantic page skeleton','header, main and footer describe the purpose of page regions to browsers and assistive technology.','<header><h1>Study Hub</h1></header>\n<main>\n  <section aria-labelledby="news-title">\n    <h2 id="news-title">Latest updates</h2>\n    <p>New lessons are available.</p>\n  </section>\n</main>\n<footer>FelixForge Academy</footer>'),
('Create a useful link and image','Use descriptive link text and meaningful alternative text for informative images.','<a href="/courses">Explore the courses</a>\n<img src="robot.jpg" alt="A small educational robot on a desk">'),
('Label form controls','The label for attribute connects a text label to the input id.','<form>\n  <label for="email">Email address</label>\n  <input id="email" name="email" type="email" required>\n  <button type="submit">Join</button>\n</form>'),
('Add a table with headings','Use th for header cells and scope to describe which cells they label.','<table>\n  <caption>Weekly study hours</caption>\n  <tr><th scope="col">Subject</th><th scope="col">Hours</th></tr>\n  <tr><th scope="row">Physics</th><td>4</td></tr>\n</table>'),
('Make a page easier to navigate','A skip link lets keyboard users jump directly to the main content.','<a href="#main-content">Skip to main content</a>\n<nav aria-label="Main navigation"><a href="/">Home</a></nav>\n<main id="main-content"><h1>Welcome</h1></main>')],
'css': [
('Style a component with a class','A class selector applies a rule to every element carrying that class.','.notice {\n  padding: 1rem;\n  border: 1px solid #9ca3af;\n  border-radius: 0.5rem;\n  background: #f8fafc;\n}'),
('Understand which rule wins','A class selector is more specific than an element selector. Later rules of equal specificity can override earlier ones.','p { color: #334155; }\n.article p { color: #1d4ed8; }\n/* Paragraphs inside .article use blue. */'),
('Control the box size','With border-box, padding and border are included inside the declared width.','* { box-sizing: border-box; }\n.card {\n  width: 280px;\n  padding: 20px;\n  border: 2px solid #64748b;\n}'),
('Align items with Flexbox','display:flex places children along a main axis. gap adds consistent space between them.','.toolbar {\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  gap: 1rem;\n}'),
('Create a responsive card grid','repeat and minmax let the browser fit as many columns as the available width allows.','.cards {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));\n  gap: 1rem;\n}'),
('Change layout on smaller screens','A media query applies its rules only when the viewport matches the condition.','@media (max-width: 600px) {\n  .sidebar { display: none; }\n  .page { padding: 1rem; }\n}')],
'sql': [
('Create a table with constraints','A primary key uniquely identifies each learner. NOT NULL requires a value.','CREATE TABLE learners (\n  id INTEGER PRIMARY KEY,\n  full_name TEXT NOT NULL,\n  email TEXT UNIQUE\n);'),
('Filter and sort a result','WHERE filters rows before ORDER BY sorts the remaining rows.','SELECT full_name, score\nFROM results\nWHERE score >= 50\nORDER BY score DESC;'),
('Add a row safely','Specify the target columns so the values are clear and independent of table column order.','INSERT INTO learners (id, full_name, email)\nVALUES (1, \'Ada Okafor\', \'ada@example.test\');'),
('Join matching records','An INNER JOIN returns rows where the learner IDs match in both tables.','SELECT learners.full_name, results.score\nFROM learners\nINNER JOIN results\n  ON learners.id = results.learner_id;'),
('Count and group records','GROUP BY creates one result row per subject; COUNT counts records in each group.','SELECT subject, COUNT(*) AS attempts\nFROM results\nGROUP BY subject\nORDER BY attempts DESC;')]
}

GENERIC_SLUGS = set(GENERIC)

def extra_examples(slug, position, title):
    """Return three distinct, language-specific examples for the lesson."""
    if slug in GENERIC:
        items = GENERIC[slug]
    elif slug in SPECIAL:
        items = SPECIAL[slug]
    else:
        return []
    index = min(max(position - 1, 0), len(items) - 1)
    selected = [items[(index + offset) % len(items)] for offset in range(min(3, len(items)))]
    return [
        {'title': item[0], 'explanation': item[1], 'code': item[2]}
        for item in selected
    ]

GENERIC['typescript'] = [
('A small typed program','TypeScript adds type annotations and compiles to JavaScript.','function main(): void {\n  console.log("My first TypeScript program");\n  console.log("Learning by building.");\n}\nmain();'),
('Calculate a total','The number annotation documents and checks the expected value type.','const notebooks: number = 3;\nconst price: number = 500;\nconst total: number = notebooks * price;\nconsole.log(`Total: ${total}`);'),
('Check a score','A Boolean condition controls which branch runs.','const score: number = 76;\nif (score >= 50) {\n  console.log("Pass");\n} else {\n  console.log("Try again");\n}'),
('Return a calculated value','The return type after the parameter list tells TypeScript what the function returns.','function square(number: number): number {\n  return number * number;\n}\nconsole.log(square(6));'),
('Work with a typed array','number[] describes an array containing numbers.','const scores: number[] = [65, 72, 88, 91];\nfor (const score of scores) {\n  console.log(score);\n}')]
