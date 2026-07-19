每个命令只负责其中一步：
保存文件：只保存在电脑磁盘；:
    E:\PycharmProjects\Hfss-Agent
git add：选择本次准备提交的文件；
    暂存区
git commit：在本地生成一个版本；
    将暂存区内容保存成正式版本。
git push：把本地版本上传到GitHub。
    把本地新增的提交上传到GitHub私有仓库。

每次更新的标准流程：
    powershell中：
        Set-Location "E:\PycharmProjects\Hfss-Agent"
    确认Git仓库根目录：
        git rev-parse --show-toplevel
    应显示：E:/PycharmProjects/Hfss-Agent
    修改前检查：
        git status
    输出：
        On branch main
        Your branch is up to date with 'origin/main'.

        nothing to commit, working tree clean
    它表示上一次工作已经全部提交并上传。
    如果个人GitHub仓库可能在其他个人设备上发生过更新，可以先运行：
        git pull --ff-only
    查看发生了什么变化：
        git status