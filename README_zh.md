# 概述

English README: [README.md](./README.md)

禅道是中国研发团队的头号团队协作工具，拥有140万用户。它有许多用户，如Twitter、联想等。以下是它的官方网站：

* [中文官网](https://www.zentao.net/)
* [英文官网](https://www.zentao.pm/)

新版禅道存在后台RCE漏洞。

# 影响版本

18.0 <= versions <= 最新(18.10)

# 漏洞成因

访问repo-create可以知道$clientVersionFile的值，关键代码位于`/app/zentao/module/repo/model.php`的`checkClient`函数：

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

通过upgrade-moveExtFiles可以创建路径为$clientVersionFile的目录，关键代码位于`/app/zentao/module/upgrade/model.php`的`moveExtFiles`函数：

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

然后可以通过repo-create执行受限的命令，命令执行的关键代码位于`/app/zentao/module/repo/model.php`的`checkConnection`函数：

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

对命令过滤的关键代码位于`/app/zentao/module/repo/model.php`的`checkClient`函数：

```php
if(preg_match('/[ #&;`,\|*?~<>^()\[\]{}$]/', $this->post->client))
{
    dao::$errors['client'] = $this->lang->repo->error->clientPath;
    return false;
}
```

可以执行命令将`/app/htdocs/index.php`拷贝到`/app/zentao/www/y.php`，将该目录下的`x.php`重命名为`x.php.bak`，将`y.php`重命名为`x.php`，并通过替换`x.php`中的“isset”为“system”。

然后可以直接访问`x.php`传入参数`mode`实现命令执行。

# 演示

见本仓库Demonstrate.mp4文件。

# exp

见本仓库zentao18-rce-exp.py文件。

# 免责声明

本仓库仅用于学习，请勿用于实际场景，一切后果由使用者自负。