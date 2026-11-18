"""Local-computer setup and beginner glossary shown inside every lesson."""

LOCAL_SETUP = {
    'python': {'title':'Run Python on your computer','install':'Install Python 3 from python.org. On Windows, tick “Add Python to PATH” in the installer. Install a code editor such as Visual Studio Code if you want one.', 'file':'hello.py','run_windows':'py hello.py','run_other':'python3 hello.py','check':'py --version (Windows) or python3 --version (macOS/Linux)','note':'Save the file with a .py extension. Run the command in the terminal from the folder containing the file.'},
    'html': {'title':'Open HTML locally on your computer','install':'No compiler or server is required for a basic HTML page. Create a folder, open it in a code editor, and save your page as index.html. Install a modern browser such as Firefox, Chrome or Edge.', 'file':'index.html','run_windows':'start index.html','run_other':'open index.html (macOS) or xdg-open index.html (Linux)','check':'Double-click index.html to open it in your browser.','note':'HTML describes page structure. The browser reads the file directly; CSS and JavaScript files can sit beside it in the same project folder.'},
    'css': {'title':'Preview CSS locally on your computer','install':'Create a project folder and save an HTML file plus a CSS file in it. Use a code editor and a modern browser. Link the stylesheet from HTML with a link element.', 'file':'index.html and styles.css','run_windows':'start index.html','run_other':'Open index.html in your browser.','check':'Change a CSS rule, save, then refresh the browser.','note':'CSS is interpreted by the browser. It is not normally run as a separate terminal program.'},
    'javascript': {'title':'Run JavaScript locally on your computer','install':'Install Node.js LTS from nodejs.org for terminal programs. A browser is enough for webpage JavaScript. Save a script as app.js.', 'file':'app.js','run_windows':'node app.js','run_other':'node app.js','check':'node --version','note':'For browser code, link app.js from an HTML file and open that HTML page in your browser. Node.js runs JavaScript outside the browser.'},
    'c': {'title':'Compile and run C locally','install':'Install a C compiler. On Windows, MSYS2 with the MinGW-w64 GCC toolchain is a common option; install GCC and make sure its bin folder is on PATH. On macOS install Xcode Command Line Tools; on Linux install gcc using your distribution package manager.', 'file':'main.c','run_windows':'gcc main.c -o main.exe; .\\main.exe','run_other':'gcc main.c -o main && ./main','check':'gcc --version','note':'Compilation creates an executable file. Run the compile command again after changing the source code.'},
    'cpp': {'title':'Compile and run C++ locally','install':'Install a C++ compiler. On Windows, MSYS2 with MinGW-w64 GCC is a common option; on macOS use Xcode Command Line Tools; on Linux install g++ with your package manager.', 'file':'main.cpp','run_windows':'g++ main.cpp -std=c++17 -o main.exe; .\\main.exe','run_other':'g++ main.cpp -std=c++17 -o main && ./main','check':'g++ --version','note':'The compiler translates C++ source into an executable. Keep the source file extension .cpp.'},
    'java': {'title':'Compile and run Java locally','install':'Install a Java Development Kit (JDK), such as an LTS release, and ensure java and javac are available in PATH. Save the public class example in Main.java.', 'file':'Main.java','run_windows':'javac Main.java; java Main','run_other':'javac Main.java && java Main','check':'java --version and javac --version','note':'The filename must match a public class name. javac compiles the source; java starts the compiled class.'},
    'csharp': {'title':'Run C# locally with .NET','install':'Install the .NET SDK from dotnet.microsoft.com. Create a console project from a terminal, or use an IDE that supports .NET.', 'file':'Program.cs','run_windows':'dotnet new console -n MyApp; cd MyApp; dotnet run','run_other':'dotnet new console -n MyApp && cd MyApp && dotnet run','check':'dotnet --info','note':'The SDK includes the compiler and runtime. Put your code in Program.cs inside the generated project.'},
    'php': {'title':'Run PHP locally','install':'Install PHP from php.net or use a trusted platform-specific package manager. Ensure the PHP executable is available in PATH. Save your script with a .php extension.', 'file':'hello.php','run_windows':'php hello.php','run_other':'php hello.php','check':'php --version','note':'For command-line examples, PHP runs directly in the terminal. For web projects, PHP has a built-in development server: php -S localhost:8000.'},
    'sql': {'title':'Practise SQL locally with SQLite','install':'Install the SQLite command-line tools or a desktop SQLite database browser. Create a practice database file in your project folder.', 'file':'practice.sql','run_windows':'sqlite3 practice.db < practice.sql','run_other':'sqlite3 practice.db < practice.sql','check':'sqlite3 --version','note':'SQL is a query language, not a standalone general-purpose program. SQLite is a lightweight database engine that executes SQL against a database file.'},
    'typescript': {'title':'Compile and run TypeScript locally','install':'Install Node.js LTS, then install TypeScript in a project using npm. In a terminal inside the project folder, run npm init -y and npm install --save-dev typescript.', 'file':'app.ts','run_windows':'npx tsc app.ts; node app.js','run_other':'npx tsc app.ts && node app.js','check':'node --version and npx tsc --version','note':'The TypeScript compiler converts .ts source into JavaScript. Node.js then runs the generated .js file.'},
    'go': {'title':'Run Go locally','install':'Install the Go toolchain from go.dev/dl and ensure go is available in PATH. Create a project folder and initialise a module with go mod init example.com/hello.', 'file':'main.go','run_windows':'go run main.go','run_other':'go run main.go','check':'go version','note':'go run compiles and runs the program for development. go build creates an executable.'},
    'rust': {'title':'Run Rust locally','install':'Install Rust using the official rustup installer from rust-lang.org/tools/install. It installs rustc and Cargo, Rust’s build tool and package manager.', 'file':'src/main.rs','run_windows':'cargo new hello; cd hello; cargo run','run_other':'cargo new hello && cd hello && cargo run','check':'rustc --version and cargo --version','note':'For a single file you can use rustc main.rs and run the resulting executable. Cargo is recommended for projects.'},
    'ruby': {'title':'Run Ruby locally','install':'Install Ruby using the official installer for your operating system or a trusted package manager. Ensure ruby is available in PATH.', 'file':'hello.rb','run_windows':'ruby hello.rb','run_other':'ruby hello.rb','check':'ruby --version','note':'Ruby is interpreted; save the source with a .rb extension and run it with the ruby command.'},
    'swift': {'title':'Run Swift locally','install':'On macOS, install Xcode or the Swift toolchain. On Windows or Linux, use the official Swift installation instructions for that operating system.', 'file':'main.swift','run_windows':'swift main.swift','run_other':'swift main.swift','check':'swift --version','note':'The Swift command can run a script directly. Toolchain support differs by operating system; Apple app development generally requires macOS and Xcode.'},
    'kotlin': {'title':'Run Kotlin locally','install':'Install a JDK and the Kotlin compiler, or use the Kotlin command-line tools provided by the official Kotlin documentation. IntelliJ IDEA also provides Kotlin project support.', 'file':'Main.kt','run_windows':'kotlinc Main.kt -include-runtime -d Main.jar; java -jar Main.jar','run_other':'kotlinc Main.kt -include-runtime -d Main.jar && java -jar Main.jar','check':'kotlinc -version and java --version','note':'Kotlin/JVM compiles to Java bytecode and uses the Java runtime. A main function is the usual entry point for a simple console program.'},
}

GLOSSARY = {
    'program': 'A program is a set of instructions a computer follows to perform a task.',
    'source code': 'Source code is the human-readable text a developer writes in a programming language.',
    'syntax': 'Syntax is the set of grammar and punctuation rules that determine whether code is written in a valid form.',
    'variable': 'A variable is a named place a program uses to refer to a value. Some languages allow its value to change.',
    'data type': 'A data type describes the kind of value being represented, such as a number, text or true/false value.',
    'function': 'A function is a named, reusable group of instructions that can receive inputs and may return a result.',
    'parameter': 'A parameter is a named input listed in a function definition.',
    'argument': 'An argument is the actual value supplied when a function is called.',
    'return value': 'A return value is the result a function sends back to the code that called it.',
    'loop': 'A loop repeats instructions. Its stopping condition or sequence determines when repetition ends.',
    'condition': 'A condition is an expression evaluated as true or false to guide a decision.',
    'array': 'An array is an indexed collection of values. Indexes commonly begin at zero, depending on the language.',
    'list': 'A list is a collection that stores multiple values in an organised sequence.',
    'object': 'An object groups related data and, in many languages, behaviour under one value.',
    'class': 'A class is a definition used to create objects with specified data and behaviour.',
    'compiler': 'A compiler translates source code into another form, often machine code or bytecode, before execution.',
    'interpreter': 'An interpreter executes a program by processing its instructions at runtime.',
    'runtime': 'The runtime is the environment and supporting system in which a program executes.',
    'terminal': 'A terminal is a text-based interface where you type commands and read their output.',
    'command line': 'The command line is a way to control tools by entering text commands rather than clicking buttons.',
    'dom': 'The Document Object Model (DOM) is the browser’s object representation of a webpage that scripts can inspect and change.',
    'selector': 'A selector is a pattern used to target elements, such as a CSS rule or a DOM query.',
    'database': 'A database is an organised collection of data managed so it can be stored, retrieved and updated.',
    'table': 'A database table organises related records into rows and columns.',
    'query': 'A query is a request for data or an operation to be performed by a database.',
    'api': 'An API is a defined interface that lets one software component communicate with another.',
    'module': 'A module is a file or unit that groups related code and can be reused by other parts of a program.',
    'package': 'A package is a reusable collection of code distributed for installation into a project.',
    'parameterised': 'A parameterised query keeps data values separate from SQL instructions, helping prevent SQL injection.',
    'event': 'An event is an occurrence, such as a click or key press, that a program can respond to.',
    'exception': 'An exception is a signal that an operation failed or encountered an unusual condition during execution.',
}

def glossary_for(text):
    import re
    source = (text or '').lower()
    found = []
    for term, definition in GLOSSARY.items():
        if re.search(r'(?<![a-z])' + re.escape(term) + r'(?![a-z])', source):
            found.append({'term': term.title(), 'definition': definition})
        if len(found) >= 8:
            break
    return found or [{'term':'Instruction', 'definition':'An instruction is one step that tells the computer what operation to perform.'}]
