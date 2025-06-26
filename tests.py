from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def tests():
    # Tests for get_files_info.py
    # output = get_files_info("calculator", ".")
    # print("Result for current directory:")
    # print(output)
    # print("\n")

    # output = get_files_info("calculator", "pkg")
    # print("Result for 'pkg' directory:")
    # print(output)
    # print("\n")

    # output = get_files_info("calculator", "/bin")
    # print("Result for '/bin' directory:")
    # print(output)
    # print("\n")

    # output = get_files_info("calculator", "../")
    # print("Result for '../' directory:")
    # print(output)
    # print("\n")

    # Tests for get_file_content.py
    # output = get_file_content("calculator", "main.py")
    # print("Result for current directory:")
    # print(output)
    # print("\n")

    # output = get_file_content("calculator", "pkg/calculator.py")
    # print("Result for current directory:")
    # print(output)
    # print("\n")

    # output = get_file_content("calculator", "/bin/cat")
    # print("Result for current directory:")
    # print(output)
    # print("\n")

    # Tests for write_file.py
    # output = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # print("Result for lorem.txt filepath")
    # print(f"{output}\n")

    # output = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # print("Result for pkg/morelorem.txt filepath")
    # print(f"{output}\n")

    # output = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    # print("Result for /tmp/temp.txt filepath")
    # print(f"{output}\n")
    
    # Tests for run_python.py
    output = run_python_file("calculator", "main.py")
    print("Result for main.py filepath")
    print(f"{output}\n")

    output = run_python_file("calculator", "tests.py")
    print("Result for tests.py filepath")
    print(f"{output}\n")

    output = run_python_file("calculator", "../main.py")
    print("Result for ../main.py filepath")
    print(f"{output}\n")

    output = run_python_file("calculator", "nonexistent.py")
    print("Result for nonexistent.py filepath")
    print(f"{output}\n")

if __name__ == "__main__":
    tests()