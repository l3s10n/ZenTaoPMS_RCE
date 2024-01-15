# Overview

中文README: [README_zh.md](./README_zh.md)

ZenTao is the #1 Team Collaborative Tool for R&D teams in China with 1.4 Million Users. It has many users, such as Twitter, Lenovo, etc. Here is its official website:

* [Chinese Official Website](https://www.zentao.net/)
* [English Official Website](https://www.zentao.pm/)

The new version of ZenTao has a backend RCE vulnerability.

# Version affected

18.0 <= versions <= newest(18.10)

# Cause of the Vulnerability.

By accessing repo-create, you can learn the value of $clientVersionFile, and the key code is located in the `checkClient` method of `/app/zentao/module/repo/model.php`：

```php
$clientVersionFile = $this->session->clientVersionFile;
if(empty($clientVersionFile))
{
    $clientVersionFile = $this->app->getLogRoot() . uniqid('version_') . '.log';

    session_start();
    $this->session->set('clientVersionFile', $clientVersionFile);
    session_write_close();
}

if(file_exists($clientVersionFile)) return true;

$cmd = $this->post->client . " --version > $clientVersionFile";
dao::$errors['client'] = sprintf($this->lang->repo->error->safe, $clientVersionFile, $cmd);
```

A directory with the path $clientVersionFile can be created through upgrade-moveExtFiles, and the key code is located at the `moveExtFiles` method of `/app/zentao/module/upgrade/model.php`：

```php
$data = fixer::input('post')->get();
$customRoot = $this->app->appRoot . 'extension' . DS . 'custom';
$response   = array('result' => 'success');

foreach($data->files as $file)
{
    $dirRoot  = $customRoot . DS . dirname($file);
    $fileName = basename($file);
    $fromPath = $this->app->getModuleRoot() . $file;
    $toPath   = $dirRoot . DS . $fileName;
    if(!is_dir($dirRoot))
    {
        if(!mkdir($dirRoot, 0777, true))
        ...
```

Then, restricted commands can be executed through repo-create. Key code for command execution located at the `checkConnection` method of `/app/zentao/module/repo/model.php`：

```php
$scm      = $this->post->SCM;
$client   = $this->post->client;
$account  = $this->post->account;
$password = $this->post->password;
$encoding = strtoupper($this->post->encoding);
$path     = $this->post->path;
if($encoding != 'UTF8' and $encoding != 'UTF-8') $path = helper::convertEncoding($path, 'utf-8', $encoding);

if($scm == 'Subversion')
{
    /* Get svn version. */
    $versionCommand = "$client --version --quiet 2>&1";
    exec($versionCommand, $versionOutput, $versionResult);
```

The key code for command filtering is located at the `checkClient` method of `/app/zentao/module/repo/model.php`：

```php
if(preg_match('/[ #&;`,\|*?~<>^()\[\]{}$]/', $this->post->client))
{
    dao::$errors['client'] = $this->lang->repo->error->clientPath;
    return false;
}
```

Commands can be executed to copy `/app/htdocs/index.php` to `/app/zentao/www/y.php`, rename `x.php` in that directory to `x.php.bak`, rename `y.php` to `x.php`, and replace “isset” with “system” in `x.php`.

Then, by directly accessing `x.php` and passing the parameter `mode`, we can execute command.

# Demonstrate

You can see it at Demonstrate.mp4 of this repository.

# Exp

You can get it at zentao18-rce-exp.py of this repository.

# Disclaimer

This repository is for learning purposes only, do not use it in real-world scenarios, and all consequences are the responsibility of the user.