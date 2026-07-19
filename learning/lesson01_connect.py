import win32com.client
# Com:Component Object Model 

def connect_hfss(prog_id = "Ansoft.ElectronicsDesktop"):
    try:
        app = win32com.client.Dispatch(prog_id)
        #Dispatch()的作用是根据COM标识找到对应软件，并创建一个Python可以控制的COM代理对象。
        #Ansoft.ElectronicsDesktop是HFSS的COM标识，表示我们要连接的是HFSS软件。

        desktop = app.GetAppDesktop()

        desktop.RestoreWindow()
        #如果AEDT窗口最小化，就恢复；如果AEDT正在后台运行，就将窗口显示出来；方便当前调试时观察建模过程。
        return desktop

    except Exception as error:
        raise RuntimeError(
        f"无法连接HFSS，ProgID={prog_id}"
        ) from error



def main():
    try:
        desktop = connect_hfss()

        print("HFSS连接成功")
        print("Desktop对象：", desktop)
    except RuntimeError as error:
        print("HFSS连接失败")
        print(error)


if __name__ == "__main__":
    main()