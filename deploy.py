import asyncio
import os
import runpy
import shutil
import sys
import zipfile
import argparse
from argparse import ArgumentParser
from asyncio import sleep

arg_parse = argparse.ArgumentParser()
arg_parse.add_argument("--generate", action="store_true")
arg_parse.add_argument("--client",  action="store_true")
group = arg_parse.add_mutually_exclusive_group()
group.add_argument("--server",  action="store_true")
group.add_argument("--webserver", action="store_true")
args = arg_parse.parse_args()
sys.argv = sys.argv[:1]

# get args

async def main():
    if args.generate:
        # delete previous run

        for file in os.listdir("output"):
            if os.path.isdir(os.path.join("output", file)):
                shutil.rmtree(os.path.join("output", file))
            else:
                os.remove(os.path.join("output", file))

        # generate new data
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            "Generate.py"
        )
        await process.wait()

        # extract and rename
        zip_file = zipfile.ZipFile(os.path.join("output", os.listdir("output")[0]))
        for zip_contents in zip_file.namelist():
            if zip_contents.endswith(".applat"):
                out_client_file = zip_file.extract(zip_contents, os.path.join("output"))
                os.rename(out_client_file, "output/client.applat")

        zip_file.close()
        os.rename(zip_file.filename, os.path.join("output", "server.zip"))
        print("\n")
    if args.server:
        await asyncio.create_subprocess_exec(
            sys.executable,
            "Launcher.py",
            "output/server.zip"
        )
    elif args.webserver:
        await asyncio.create_subprocess_exec(
            sys.executable,
            "WebHost.py",
            "output/server.zip",
        )
    await sleep(3)
    if args.client:
        # run client
        print(os.path.abspath("Launcher.py"))
        await asyncio.create_subprocess_exec(
            sys.executable,
            "Launcher.py",
            "output/client.applat",
            "--",
            "--connect=22122"
            "--name=nathan"
        )

    while True:
        pass

if __name__ == "__main__":
    asyncio.run(main())
