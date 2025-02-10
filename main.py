# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from app.application import app

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("-------------------------")
    print("| AFFINITY - ASSESSMENT |")
    print("-------------------------")
    app.run(host='0.0.0.0', port=8094, debug=True)
