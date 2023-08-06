import os
import platform
from colorama import Fore, Style
from megalus.core.utils import run_command
from megalus.projects.setup import settings

minify_command = "java -jar yuicompressor-2.4.8.jar "
"{all} -o {min} --charset utf-8"
minify_command_windows = "java -jar yuicompressor-2.4.8.jar "
"{all} --charset utf-8 > {min}"


def saveFile(sourcePaths, destPath, minPath, baseDir, header=None):
    print("Gerando arquivos {} e {}".format(destPath, minPath))
    try:
        with open(destPath, 'w') as f:
            for dirc, srcFile in sourcePaths:
                print(srcFile)
                with open(os.path.join(baseDir, dirc, srcFile)) as inputFile:
                    if destPath[-2:] == "js":
                        srcText = "{};\n".format(
                            inputFile.read().decode("utf-8"))
                    else:
                        srcText = inputFile.read().decode("utf-8")
                    f.write(srcText.encode("utf-8"))

        if platform.system() == "Windows":
            command = minify_command_windows
        else:
            command = minify_command

        compress_cmd = command.format(
            all=destPath,
            min=minPath
        )

        ret = run_command(
            title=None,
            command_list=[
                {
                    'command': compress_cmd,
                    'run_stdout': False
                }
            ]
        )
        if not ret:
            print(
                Fore.RED +
                "Ocorreu um erro ao gerar o Minify" +
                Style.RESET_ALL)
            return False
        else:
            return True
    except BaseException:
        raise
        print(Fore.RED + "Ocorreu um erro ao gerar o Minify" + Style.RESET_ALL)
        return False


def saveAlone(workdir, alone_list):
    for dirc, file in alone_list:
        destPath = os.path.join(workdir, dirc, file)
        minPath = os.path.join(workdir, dirc, "{}.min.{}".format(
            file.split(".")[0],
            file.split(".")[-1]
        ))
        print("Minificando arquivo {} para {}.".format(file, minPath))

        if platform.system() == "Windows":
            command = minify_command_windows
        else:
            command = minify_command

        compress_cmd = command.format(
            all=destPath,
            min=minPath
        )

        ret = run_command(
            title=None,
            command_list=[
                {
                    'command': compress_cmd,
                    'run_stdout': False
                }
            ]
        )
        if not ret:
            print(
                Fore.RED +
                "Ocorreu um erro ao gerar o Minify" +
                Style.RESET_ALL)
            return False

    return True


def minifyJS(
        current_dir,
        baseDir=getattr(settings, 'BASEDIRSTATIC', None),
        source=getattr(settings, 'JSSOURCES', None)):
    workdir = os.path.join(current_dir, *baseDir)
    jsDestPath = os.path.join(workdir, "js", "all.js")
    jsMinPath = os.path.join(workdir, "js", "all.min.js")
    ret = saveFile(source, jsDestPath, jsMinPath, workdir)
    if ret:
        return saveAlone(workdir, settings.JSALONE)
    else:
        return ret


def minifyCSS(
        current_dir,
        baseDir=getattr(settings, 'BASEDIRSTATIC', None),
        source=getattr(settings, 'CSSSOURCES', None)):
    workdir = os.path.join(current_dir, *baseDir)
    cssDestPath = os.path.join(workdir, "css", "all.css")
    cssMinPath = os.path.join(workdir, "css", "all.min.css")
    ret = saveFile(source, cssDestPath, cssMinPath, workdir)
    if ret:
        return saveAlone(workdir, settings.CSSALONE)
    else:
        return ret
