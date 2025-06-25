from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def tests():
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
    output = get_file_content("calculator", "main.py")
    print("Result for current directory:")
    print(output)
    print("\n")

    output = get_file_content("calculator", "pkg/calculator.py")
    print("Result for current directory:")
    print(output)
    print("\n")

    output = get_file_content("calculator", "/bin/cat")
    print("Result for current directory:")
    print(output)
    print("\n")

if __name__ == "__main__":
    tests()