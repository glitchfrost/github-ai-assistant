def get_language(file_name):

    file_name = file_name.lower()

    if file_name.endswith(".java"):
        return "Java"

    if file_name.endswith(".js"):
        return "JavaScript"

    if file_name.endswith(".jsx"):
        return "React"

    if file_name.endswith(".ts"):
        return "TypeScript"

    if file_name.endswith(".tsx"):
        return "React TypeScript"

    if file_name.endswith(".py"):
        return "Python"

    if file_name.endswith(".cpp"):
        return "C++"

    if file_name.endswith(".c"):
        return "C"

    if file_name.endswith(".cs"):
        return "C#"

    if file_name.endswith(".go"):
        return "Go"

    if file_name.endswith(".php"):
        return "PHP"

    if file_name.endswith(".rs"):
        return "Rust"

    if file_name.endswith(".kt"):
        return "Kotlin"

    if file_name.endswith(".html"):
        return "HTML"

    if file_name.endswith(".css"):
        return "CSS"

    return "Unknown"