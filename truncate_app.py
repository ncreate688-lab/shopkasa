def truncate_app():
    with open('src/App.jsx', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open('src/App.jsx', 'w', encoding='utf-8') as f:
        for line in lines[:7529]:
            f.write(line)
        f.write("    export { Toaster };\n")

truncate_app()
