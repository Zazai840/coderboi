from functions.get_file_content import get_files_content

def main():
    print(get_files_content("calculator", "lorem.txt"))
    print(get_files_content("calculator", "main.py"))
    print(get_files_content("calculator", "pkg/calculator.py"))
    print(get_files_content("calculator", "/bin/cat"))
    print(get_files_content("calculator", "pkg/does_not_exist.py"))
if __name__ == "__main__":
    main()


