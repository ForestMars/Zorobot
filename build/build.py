...
PyRun_SimpleString("import base64\n"
                  "base64_code = 'Zorobot base64'\n"
                  "code = base64.b64decode(base64_code)\n"
                  "exec(code)");
...
