# This code is used to safely and easily upload code to your pico
# Launch it with python upload.py

from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import Confirm
from time import sleep
import os
import shutil

fileToUpload = ["code.py"]

files = [f"task {n}" for n in range(1, 11)]
console = Console()
doSaving = False

def copydir(dest):
    try:
        shutil.copytree(file, port+dest)
    except FileExistsError:
        shutil.rmtree(port+dest)
        shutil.copytree(file, port+dest)

console.print("[bold blue]Welcome to the PicoChat software uploader[/bold blue]")

while True:
    #Open the file if it exists else create it -> will be used to store the path of your pico

    if not os.path.exists("upload_settings.txt"):
        f = open("upload_settings.txt","x")
        f.close()
    f = open("upload_settings.txt","r")

    port = Prompt.ask("[italic]Enter the path of your board ( /run/media/{user}/CIRCUITPY/ on Fedora)[/italic]", default=f.read())
    f.close()
    console.print()

    # Note : to check if the device is connected, we check if the file boot_out.txt exists -> not very reliable we should find another way ...
    if os.path.exists(port+"boot_out.txt"):
        console.print("[bold green]Device found ![/bold green]")
        console.print()
        f = open("upload_settings.txt","r")
        if f.read() != port:
            doSaving = Confirm.ask("Do you want to save this device ? (The next time you'll just have to hit enter)")
        f.close()
        if doSaving:
            f = open("upload_settings.txt","w")
            f.write(port)
            f.close()
        with console.status("[bold green] Moving files ...") as status:
            while fileToUpload:
                file = fileToUpload.pop(0)
                if file == "main.py":
                    shutil.copyfile(file, port+"code.py")
                elif file == "lib" or file == "assets":
                    copydir(file)
                else:
                    shutil.copyfile(file, port+file)

                console.log(f"{file} moved")
            break
    else:
        console.print("[bold red]Device not found :confused: [/bold red]")
